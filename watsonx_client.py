#!/usr/bin/env python3
"""
WatsonX AI Client for PanelPulse
Handles all interactions with IBM watsonx.ai LLM
"""

import os
import json
from typing import Dict, List, Optional
import requests


class WatsonXClient:
    """Client for IBM watsonx.ai API"""
    
    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        """
        Initialize WatsonX client
        
        Args:
            api_key: IBM Cloud API key (or set WATSONX_API_KEY env var)
            project_id: WatsonX project ID (or set WATSONX_PROJECT_ID env var)
        """
        self.api_key = api_key or os.getenv('WATSONX_API_KEY', 'YOUR_WATSONX_API_KEY_HERE')
        self.project_id = project_id or os.getenv('WATSONX_PROJECT_ID', 'YOUR_PROJECT_ID_HERE')
        
        # WatsonX API endpoints
        self.auth_url = "https://iam.cloud.ibm.com/identity/token"
        self.api_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        
        # Model configuration
        self.model_id = "ibm/granite-13b-chat-v2"  # Default model
        self.access_token = None
        
    def _get_access_token(self) -> str:
        """Get IBM Cloud IAM access token"""
        if self.access_token:
            return self.access_token
            
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        
        try:
            response = requests.post(self.auth_url, headers=headers, data=data)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token
        except Exception as e:
            raise RuntimeError(f"❌ Failed to authenticate with watsonx.ai: {e}\n"
                             f"   Please check your WATSONX_API_KEY in .env file\n"
                             f"   Get your API key from: https://cloud.ibm.com/iam/apikeys")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_p: float = 1.0,
        top_k: int = 50
    ) -> str:
        """
        Generate text using watsonx.ai
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            
        Returns:
            Generated text
        """
        token = self._get_access_token()
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repetition_penalty": 1.1
            },
            "model_id": self.model_id,
            "project_id": self.project_id
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            return result["results"][0]["generated_text"].strip()
        except Exception as e:
            raise RuntimeError(f"❌ WatsonX API error: {e}\n"
                             f"   Check your WATSONX_PROJECT_ID and API credentials\n"
                             f"   Verify at: https://dataplatform.cloud.ibm.com/wx/home")
    
    def generate_question(
        self,
        role: str,
        resume: str,
        job_description: str,
        previous_questions: List[str] = None,
        focus_area: str = ""
    ) -> str:
        """
        Generate an interview question using watsonx.ai
        
        Args:
            role: Interviewer role (hiring-manager, system-architect, senior-dev)
            resume: Candidate's resume
            job_description: Target job description
            previous_questions: List of already asked questions
            focus_area: Specific area to focus on
            
        Returns:
            Generated interview question
        """
        previous_q = "\n".join(previous_questions) if previous_questions else "None"
        
        prompt = f"""You are an expert {role} conducting a technical interview.

Resume Summary:
{resume[:500]}...

Job Requirements:
{job_description[:500]}...

Previous Questions Asked:
{previous_q}

Focus Area: {focus_area or 'General assessment'}

Generate ONE specific, insightful interview question that:
1. Is relevant to the candidate's experience and the job requirements
2. Is different from previous questions
3. Encourages detailed, specific answers
4. Follows best practices for {role} interviews

Question:"""

        return self.generate(prompt, max_tokens=200, temperature=0.8)
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        role: str,
        resume: str,
        job_description: str
    ) -> Dict:
        """
        Evaluate an interview answer using watsonx.ai
        
        Args:
            question: The question that was asked
            answer: Candidate's answer
            role: Interviewer role
            resume: Candidate's resume
            job_description: Job requirements
            
        Returns:
            Dictionary with evaluation metrics
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

        response = self.generate(prompt, max_tokens=400, temperature=0.3)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in AI response")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to parse AI evaluation: {e}\n"
                             f"   AI Response: {response[:200]}...\n"
                             f"   This indicates an issue with the AI model or prompt")
    
    def generate_dashboard(
        self,
        evaluations: List[Dict],
        resume: str,
        job_description: str
    ) -> Dict:
        """
        Generate final interview dashboard using watsonx.ai
        
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

All Strengths Noted: {', '.join(all_strengths[:10])}
All Weaknesses Noted: {', '.join(all_weaknesses[:10])}

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

        response = self.generate(prompt, max_tokens=600, temperature=0.3)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                dashboard = json.loads(json_str)
                dashboard['overall_score'] = int(avg_score)  # Use calculated score
                return dashboard
            else:
                raise ValueError("No valid JSON found in AI response")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to generate AI dashboard: {e}\n"
                             f"   AI Response: {response[:200]}...\n"
                             f"   This indicates an issue with the AI model or prompt")


# Singleton instance
_watsonx_client = None

def get_watsonx_client() -> WatsonXClient:
    """Get or create WatsonX client singleton"""
    global _watsonx_client
    if _watsonx_client is None:
        _watsonx_client = WatsonXClient()
    return _watsonx_client

# Made with Bob
