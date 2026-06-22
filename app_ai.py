#!/usr/bin/env python3
"""
PanelPulse AI Web Application
Flask backend for the AI-powered mock interview system using the local wrapper service.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import secrets
from datetime import datetime

os.environ["BOB_WRAPPER_URL"] = os.getenv("BOB_WRAPPER_URL", "http://127.0.0.1:5001")

from panelpulse_ai import (
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
    """Initialize a new AI-powered interview session"""
    try:
        data = request.json
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()

        if not resume or not job_description:
            return jsonify({
                'success': False,
                'error': 'Resume and job description are required'
            }), 400

        session_id = secrets.token_urlsafe(16)
        orchestrator = InterviewOrchestrator()
        orchestrator.context.resume = resume
        orchestrator.context.job_description = job_description

        active_sessions[session_id] = {
            'orchestrator': orchestrator,
            'started_at': datetime.now().isoformat(),
            'transcript': []
        }

        print(f"🤖 Generating first question for session {session_id}...")
        orchestrator._ask_next_question()
        question = orchestrator.last_question

        return jsonify({
            'success': True,
            'session_id': session_id,
            'question': question,
            'question_number': 1,
            'total_questions': orchestrator.context.max_total_questions,
            'current_panelist': orchestrator.context.current_panelist.value,
            'ai_powered': True
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Process user's answer with AI evaluation and get next question"""
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

        session_data['transcript'].append({
            'question': orchestrator.last_question,
            'answer': answer,
            'panelist': orchestrator.context.current_panelist.value,
            'timestamp': datetime.now().isoformat()
        })

        print(f"🤖 Evaluating answer for session {session_id}...")
        orchestrator.process_answer(answer)

        if orchestrator.context.total_questions >= orchestrator.context.max_total_questions:
            print(f"🤖 Generating AI dashboard for session {session_id}...")
            dashboard = orchestrator.health_monitor.generate_dashboard(orchestrator.context)

            del active_sessions[session_id]

            return jsonify({
                'success': True,
                'completed': True,
                'dashboard': dashboard,
                'transcript': session_data['transcript'],
                'ai_powered': True
            })

        print(f"🤖 Generating next question for session {session_id}...")
        orchestrator._ask_next_question()
        next_question = orchestrator.last_question

        return jsonify({
            'success': True,
            'completed': False,
            'question': next_question,
            'question_number': orchestrator.context.total_questions + 1,
            'total_questions': orchestrator.context.max_total_questions,
            'current_panelist': orchestrator.context.current_panelist.value if orchestrator.context.current_panelist else None,
            'ai_powered': True
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
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
        'transcript_length': len(session_data['transcript']),
        'ai_powered': True
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
    except Exception:
        return jsonify({
            'success': False,
            'error': 'Example files not found'
        }), 404


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'ai_powered': True,
        'active_sessions': len(active_sessions)
    })


if __name__ == '__main__':
    import os

    print("\n" + "=" * 80)
    print("🚀 PanelPulse AI Web Application Starting...")
    print("=" * 80)
    print("\n📱 Access the application at: http://localhost:5000")
    print("🤖 AI-Powered via /root/bob-shell-wrapper-main")
    print("🎯 Intelligent question generation and evaluation")
    print("\n" + "=" * 80 + "\n")

    wrapper_url = os.getenv('BOB_WRAPPER_URL', 'http://127.0.0.1:5001')
    print(f"🔌 Wrapper endpoint: {wrapper_url}")

    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

# Made with Bob