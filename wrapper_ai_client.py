#!/usr/bin/env python3
"""
Bob Shell Wrapper AI client for PanelPulse.
Handles all interactions with the local Bob Shell Wrapper REST API.
"""

import json
import os
from typing import Dict, List, Optional

import requests


class BobShellWrapperClient:
    """Client for the Bob Shell Wrapper REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (base_url or "http://127.0.0.1:5001").rstrip("/")
        self.timeout = timeout or int(os.getenv("BOB_WRAPPER_TIMEOUT", "120"))

    def _execute_prompt(self, prompt: str) -> str:
        """Execute a prompt through the wrapper and return clean output."""
        response = requests.post(
            f"{self.base_url}/api/v1/execute",
            json={"prompt": prompt},
            timeout=self.timeout,
        )
        response.raise_for_status()

        payload = response.json()
        if payload["success"] is not True:
            raise RuntimeError(payload["error"])

        return payload["clean_output"].strip()

    def _extract_json(self, text: str) -> Dict:
        """Extract the first JSON object from wrapper output."""
        start = text.find("{")
        end = text.rfind("}") + 1
        if start < 0 or end <= start:
            raise RuntimeError(f"Failed to parse JSON response from wrapper output: {text[:300]}")
        return json.loads(text[start:end])

    def generate_question(
        self,
        role: str,
        resume: str,
        job_description: str,
        previous_questions: Optional[List[str]] = None,
        focus_area: str = "",
    ) -> str:
        """Generate an interview question using the wrapper-backed AI service."""
        previous_q = "\n".join(previous_questions) if previous_questions else "None"

        prompt = f"""You are an expert {role} conducting a technical interview.

Candidate resume:
{resume[:1200]}

Target job description:
{job_description[:1200]}

Previous questions:
{previous_q}

Focus area:
{focus_area or 'General assessment'}

Generate exactly one concise, specific interview question.
Return only the question text without markdown, labels, or extra commentary."""
        return self._execute_prompt(prompt)

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        role: str,
        resume: str,
        job_description: str,
    ) -> Dict:
        """Evaluate an interview answer using the wrapper-backed AI service."""
        prompt = f"""You are an expert {role} evaluating an interview answer.

Question:
{question}

Candidate answer:
{answer}

Resume context:
{resume[:800]}

Job requirements:
{job_description[:800]}

Return valid JSON only using this schema:
{{
  "score": <integer 0-100>,
  "strengths": ["string", "string"],
  "weaknesses": ["string", "string"],
  "suggestions": ["string", "string"],
  "has_specific_examples": <boolean>,
  "technical_depth": <integer 0-10>
}}"""
        return self._extract_json(self._execute_prompt(prompt))

    def generate_dashboard(
        self,
        evaluations: List[Dict],
        resume: str,
        job_description: str,
    ) -> Dict:
        """Generate the final interview dashboard using the wrapper-backed AI service."""
        prompt = f"""You are an expert interview panel synthesizing final feedback.

Candidate resume:
{resume[:1000]}

Job requirements:
{job_description[:1000]}

Evaluations:
{json.dumps(evaluations, indent=2)}

Return valid JSON only using this schema:
{{
  "overall_score": <integer 0-100>,
  "strengths": ["string", "string", "string"],
  "critical_gaps": [
    {{
      "topic": "string",
      "panelist_flagged": "string",
      "what_went_wrong": "string",
      "how_to_fix": "string"
    }}
  ],
  "behavioral_feedback": "string",
  "hire_recommendation": <boolean>
}}"""
        return self._extract_json(self._execute_prompt(prompt))


_wrapper_client = None


def get_wrapper_client() -> BobShellWrapperClient:
    """Get or create the wrapper client singleton."""
    global _wrapper_client
    if _wrapper_client is None:
        _wrapper_client = BobShellWrapperClient()
    return _wrapper_client