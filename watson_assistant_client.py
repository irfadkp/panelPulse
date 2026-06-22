#!/usr/bin/env python3
"""
Watson Assistant Client for PanelPulse
Handles all interactions with IBM Watson Assistant
"""

import os
import json
from typing import Dict, List, Optional
import requests


class WatsonAssistantClient:
    """Client for IBM Watson Assistant API"""
    
    def __init__(self, api_key: Optional[str] = None, url: Optional[str] = None):
        """
        Initialize Watson Assistant client
        
        Args:
            api_key: IBM Cloud API key for Watson Assistant
            url: Watson Assistant instance URL
        """
        self.api_key = api_key or os.getenv('WATSON_ASSISTANT_API_KEY', 'eE7oUiS2MZraJsXvSO-nq4qNmh5k8yLvk02pJj86R3Qy')
        self.url = url or os.getenv('WATSON_ASSISTANT_URL', 'https://api.au-syd.assistant.watson.cloud.ibm.com/instances/fabe1946-6373-45e7-bc88-883e2af57cb4')
        
        # Extract instance ID from URL
        self.instance_id = self.url.split('/instances/')[-1] if '/instances/' in self.url else None
        
        # Session management
        self.session_id = None
        self.assistant_id = os.getenv('WATSON_ASSISTANT_ID', '')  # Will be set dynamically
        
    def _get_headers(self) -> Dict:
        """Get request headers with authentication"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_auth(self) -> tuple:
        """Get authentication tuple for requests"""
        return ('apikey', self.api_key)
    
    def create_session(self, assistant_id: str) -> str:
        """Create a new session with Watson Assistant"""
        if not assistant_id:
            raise ValueError("Assistant ID is required")
        
        self.assistant_id = assistant_id
        session_url = f"{self.url}/v2/assistants/{assistant_id}/sessions?version=2021-11-27"
        
        try:
            response = requests.post(
                session_url,
                headers=self._get_headers(),
                auth=self._get_auth()
            )
            response.raise_for_status()
            self.session_id = response.json()['session_id']
            return self.session_id
        except Exception as e:
            raise RuntimeError(f"❌ Failed to create Watson Assistant session: {e}\n"
                             f"   Check your WATSON_ASSISTANT_API_KEY and URL\n"
                             f"   URL: {self.url}")
    
    def send_message(self, text: str, context: Dict = None) -> Dict:
        """
        Send a message to Watson Assistant
        
        Args:
            text: User message text
            context: Optional context to maintain conversation state
            
        Returns:
            Assistant response with text and context
        """
        if not self.session_id or not self.assistant_id:
            raise RuntimeError("Session not initialized. Call create_session() first.")
        
        message_url = f"{self.url}/v2/assistants/{self.assistant_id}/sessions/{self.session_id}/message?version=2021-11-27"
        
        payload = {
            "input": {
                "message_type": "text",
                "text": text
            }
        }
        
        if context:
            payload["context"] = context
        
        try:
            response = requests.post(
                message_url,
                headers=self._get_headers(),
                auth=self._get_auth(),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"❌ Watson Assistant API error: {e}\n"
                             f"   Check your assistant configuration")
    
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate text using Watson Assistant (compatibility wrapper)
        
        Args:
            prompt: Input prompt
            max_tokens: Not used (Watson Assistant manages response length)
            temperature: Not used (Watson Assistant manages creativity)
            
        Returns:
            Generated text
        """
        # For compatibility with watsonx client interface
        # We'll use a simple message-response pattern
        
        if not self.session_id:
            # Try to get assistant ID from environment or use default
            assistant_id = os.getenv('WATSON_ASSISTANT_ID')
            if not assistant_id:
                raise RuntimeError("❌ WATSON_ASSISTANT_ID not configured\n"
                                 "   Set it in .env file or environment variable")
            self.create_session(assistant_id)
        
        response = self.send_message(prompt)
        
        # Extract text from response
        if 'output' in response and 'generic' in response['output']:
            texts = [item['text'] for item in response['output']['generic'] if item.get('response_type') == 'text']
            return ' '.join(texts) if texts else ""
        
        return ""
    
    def generate_question(
        self,
        role: str,
        resume: str,
        job_description: str,
        previous_questions: List[str] = None,
        focus_area: str = ""
    ) -> str:
        """
        Generate an interview question using Watson Assistant
        
        Args:
            role: Interviewer role
            resume: Candidate's resume
            job_description: Job requirements
            previous_questions: Already asked questions
            focus_area: Specific focus area
            
        Returns:
            Generated interview question
        """
        previous_q = "\n".join(previous_questions) if previous_questions else "None"
        
        prompt = f"""You are an expert {role} conducting a technical interview.

Resume Summary: {resume[:500]}...
Job Requirements: {job_description[:500]}...
Previous Questions: {previous_q}
Focus Area: {focus_area or 'General assessment'}

Generate ONE specific, insightful interview question that:
1. Is relevant to the candidate's experience and job requirements
2. Is different from previous questions
3. Encourages detailed, specific answers
4. Follows best practices for {role} interviews

Question:"""

        return self.generate(prompt, max_tokens=200)
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        role: str,
        resume: str,
        job_description: str
    ) -> Dict:
        """
        Evaluate an interview answer using Watson Assistant
        
        Args:
            question: The question asked
            answer: Candidate's answer
            role: Interviewer role
            resume: Candidate's resume
            job_description: Job requirements
            
        Returns:
            Evaluation metrics dictionary
        """
        prompt = f"""You are an expert {role} evaluating an interview answer.

Question: {question}
Candidate's Answer: {answer}
Resume Context: {resume[:300]}...
Job Requirements: {job_description[:300]}...

Evaluate this answer on a scale of 0-100 and provide:
1. Overall score (0-100)
2. Strengths (2-3 points)
3. Weaknesses (2-3 points)
4. Specific improvement suggestions

Respond in JSON format:
{{
  "score": <number>,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "has_specific_examples": <boolean>,
  "technical_depth": <number 0-10>
}}

JSON Response:"""

        response = self.generate(prompt, max_tokens=400)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in response")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to parse evaluation: {e}\n"
                             f"   Response: {response[:200]}...")
    
    def generate_dashboard(
        self,
        evaluations: List[Dict],
        resume: str,
        job_description: str
    ) -> Dict:
        """
        Generate final interview dashboard using Watson Assistant
        
        Args:
            evaluations: List of answer evaluations
            resume: Candidate's resume
            job_description: Job requirements
            
        Returns:
            Dashboard data with overall assessment
        """
        avg_score = sum(e.get('score', 0) for e in evaluations) / max(len(evaluations), 1)
        
        all_strengths = []
        all_weaknesses = []
        for e in evaluations:
            all_strengths.extend(e.get('strengths', []))
            all_weaknesses.extend(e.get('weaknesses', []))
        
        prompt = f"""You are an expert interview panel synthesizing feedback.

Candidate Resume: {resume[:400]}...
Job Requirements: {job_description[:400]}...
Individual Question Scores: {[e.get('score', 0) for e in evaluations]}
Average Score: {avg_score:.1f}
All Strengths: {', '.join(all_strengths[:10])}
All Weaknesses: {', '.join(all_weaknesses[:10])}

Provide a comprehensive interview assessment in JSON format:
{{
  "overall_score": <number 0-100>,
  "strengths": ["top 3 strengths"],
  "critical_gaps": [
    {{
      "topic": "area name",
      "panelist_flagged": "role",
      "what_went_wrong": "specific issue",
      "how_to_fix": "actionable advice"
    }}
  ],
  "behavioral_feedback": "2-3 sentence summary",
  "hire_recommendation": <boolean>
}}

JSON Response:"""

        response = self.generate(prompt, max_tokens=600)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                dashboard = json.loads(json_str)
                dashboard['overall_score'] = int(avg_score)
                return dashboard
            else:
                raise ValueError("No valid JSON found in response")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to generate dashboard: {e}\n"
                             f"   Response: {response[:200]}...")


# Singleton instance
_watson_client = None

def get_watson_client() -> WatsonAssistantClient:
    """Get or create Watson Assistant client singleton"""
    global _watson_client
    if _watson_client is None:
        _watson_client = WatsonAssistantClient()
    return _watson_client

# Made with Bob
