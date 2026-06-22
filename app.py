#!/usr/bin/env python3
"""
PanelPulse Web Application
Flask backend for the mock interview system with beautiful UI
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import secrets
import json
from datetime import datetime
from panelpulse import (
    InterviewOrchestrator,
    InterviewContext,
    PanelistRole
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Store active interview sessions
active_sessions = {}


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Initialize a new interview session"""
    try:
        data = request.json
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        
        if not resume or not job_description:
            return jsonify({
                'success': False,
                'error': 'Resume and job description are required'
            }), 400
        
        # Create new session
        session_id = secrets.token_urlsafe(16)
        orchestrator = InterviewOrchestrator()
        orchestrator.context.resume = resume
        orchestrator.context.job_description = job_description
        
        # Store session
        active_sessions[session_id] = {
            'orchestrator': orchestrator,
            'started_at': datetime.now().isoformat(),
            'transcript': []
        }
        
        # Get first question
        orchestrator._ask_next_question()
        question = orchestrator.last_question
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'question': question,
            'question_number': 1,
            'total_questions': orchestrator.context.max_total_questions,
            'current_panelist': orchestrator.context.current_panelist.value
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Process user's answer and get next question"""
    try:
        data = request.json
        session_id = data.get('session_id')
        answer = data.get('answer', '').strip()
        
        if not session_id or session_id not in active_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session'
            }), 400
        
        if not answer:
            return jsonify({
                'success': False,
                'error': 'Answer is required'
            }), 400
        
        session_data = active_sessions[session_id]
        orchestrator = session_data['orchestrator']
        
        # Store the answer in transcript
        session_data['transcript'].append({
            'question': orchestrator.last_question,
            'answer': answer,
            'panelist': orchestrator.context.current_panelist.value,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process answer
        orchestrator.process_answer(answer)
        
        # Check if interview is complete
        if orchestrator.context.total_questions >= orchestrator.context.max_total_questions:
            # Generate dashboard
            dashboard = orchestrator.health_monitor.generate_dashboard(orchestrator.context)
            
            # Clean up session
            del active_sessions[session_id]
            
            return jsonify({
                'success': True,
                'completed': True,
                'dashboard': dashboard,
                'transcript': session_data['transcript']
            })
        
        # Ask next question
        orchestrator._ask_next_question()
        next_question = orchestrator.last_question
        
        return jsonify({
            'success': True,
            'completed': False,
            'question': next_question,
            'question_number': orchestrator.context.total_questions + 1,
            'total_questions': orchestrator.context.max_total_questions,
            'current_panelist': orchestrator.context.current_panelist.value if orchestrator.context.current_panelist else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session-status/<session_id>', methods=['GET'])
def session_status(session_id):
    """Get current session status"""
    if session_id not in active_sessions:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
    
    session_data = active_sessions[session_id]
    orchestrator = session_data['orchestrator']
    
    return jsonify({
        'success': True,
        'question_number': orchestrator.context.total_questions,
        'total_questions': orchestrator.context.max_total_questions,
        'current_panelist': orchestrator.context.current_panelist.value if orchestrator.context.current_panelist else None,
        'transcript_length': len(session_data['transcript'])
    })


@app.route('/api/example-data', methods=['GET'])
def example_data():
    """Get example resume and job description"""
    try:
        with open('example_resume.txt', 'r') as f:
            resume = f.read()
        with open('example_job_description.txt', 'r') as f:
            job_description = f.read()
        
        return jsonify({
            'success': True,
            'resume': resume,
            'job_description': job_description
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Example files not found'
        }), 404


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 PanelPulse Web Application Starting...")
    print("="*80)
    print("\n📱 Access the application at: http://localhost:5000")
    print("🎯 Beautiful UI with real-time interview experience")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
