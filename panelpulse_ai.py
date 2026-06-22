#!/usr/bin/env python3
"""
PanelPulse - AI-Powered Mock Technical Interview Orchestrator
A multi-agent system with pluggable AI providers (ChatGPT, Gemini, etc.)
"""

import json
import sys
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import AI clients
from ai_clients import AIClientFactory, BaseAIClient


class PanelistRole(Enum):
    """Enum for different panelist roles"""
    HIRING_MANAGER = "hiring-manager"
    SYSTEM_ARCHITECT = "system-architect"
    SENIOR_DEV = "senior-dev"


@dataclass
class InterviewContext:
    """Stores the interview state and context"""
    resume: str = ""
    job_description: str = ""
    transcript: List[Dict[str, str]] = field(default_factory=list)
    current_panelist: Optional[PanelistRole] = None
    questions_asked: Dict[PanelistRole, int] = field(default_factory=lambda: {
        PanelistRole.HIRING_MANAGER: 0,
        PanelistRole.SYSTEM_ARCHITECT: 0,
        PanelistRole.SENIOR_DEV: 0
    })
    total_questions: int = 0
    max_questions_per_panelist: int = 2
    max_total_questions: int = 6


class BaseAgent:
    """Base class for all interview agents with AI integration"""
    
    def __init__(self, name: str, role: str, ai_client: BaseAIClient):
        self.name = name
        self.role = role
        self.ai_client = ai_client
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate a response based on context. Override in subclasses."""
        raise NotImplementedError
    
    def _generate_with_ai(self, prompt: str, max_tokens: int = 300) -> str:
        """Helper method to generate response using AI client"""
        try:
            return self.ai_client.generate(prompt, max_tokens=max_tokens, temperature=0.7)
        except Exception as e:
            print(f"⚠️  AI generation failed: {e}")
            return ""


class HiringManagerAgent(BaseAgent):
    """Hiring Manager - Evaluates behavioral competencies"""
    
    def __init__(self, ai_client: BaseAIClient):
        super().__init__("Hiring Manager", "hiring-manager", ai_client)
        self.questions = [
            "Tell me about a time you strongly disagreed with a product owner regarding technical debt. How did you handle it?",
            "Describe a situation where you had to take ownership of a critical production failure. What was your specific role in resolving it?",
            "Can you share an example of when you had to balance competing priorities under tight deadlines? What was your approach?",
            "Tell me about a time when you had to mentor a junior developer who was struggling. What specific actions did you take?"
        ]
        self.question_index = 0
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate behavioral question or follow-up"""
        if not user_input:
            question = self.questions[self.question_index % len(self.questions)]
            self.question_index += 1
            return f"{self.name}: {question}"
        else:
            if len(user_input.split()) < 30 or "we" in user_input.lower():
                return f"{self.name}: That's interesting. Can you be more specific about YOUR role in that situation? What actions did YOU personally take?"
            return ""


class SystemArchitectAgent(BaseAgent):
    """System Architect - Evaluates system design and scalability"""
    
    def __init__(self, ai_client: BaseAIClient):
        super().__init__("System Architect", "system-architect", ai_client)
        self.questions = [
            "Design a distributed tracing system for a microservices architecture with 50+ services. How would you handle trace sampling and storage at scale?",
            "You're building a real-time analytics pipeline that needs to process 100K events/second. Walk me through your architecture choices and the trade-offs.",
            "How would you design a multi-region deployment strategy for a critical service that requires 99.99% uptime? What are the failure modes you'd plan for?",
            "Explain how you would implement circuit breakers in a Kubernetes environment. What metrics would you monitor?"
        ]
        self.question_index = 0
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate system design question"""
        if not user_input:
            question = self.questions[self.question_index % len(self.questions)]
            self.question_index += 1
            return f"{self.name}: {question}"
        else:
            return ""


class SeniorDevAgent(BaseAgent):
    """Senior Developer - Evaluates technical depth and debugging"""
    
    def __init__(self, ai_client: BaseAIClient):
        super().__init__("Senior Developer", "senior-dev", ai_client)
        self.questions = [
            "Walk me through how you would optimize a slow Spring Data JPA query that's causing 5-second response times. What's your debugging methodology?",
            "You have a Kubernetes pod stuck in CrashLoopBackOff. Walk me through your step-by-step debugging process.",
            "Explain how you manage complex state in a React application. What patterns do you use and why?",
            "You notice a memory leak in a production Node.js service. How do you identify the root cause and fix it without downtime?"
        ]
        self.question_index = 0
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate technical question"""
        if not user_input:
            question = self.questions[self.question_index % len(self.questions)]
            self.question_index += 1
            return f"{self.name}: {question}"
        else:
            return ""


class HealthMonitorAgent(BaseAgent):
    """Silent agent that analyzes interview and generates feedback"""
    
    def __init__(self, ai_client: BaseAIClient):
        super().__init__("Health Monitor", "health-monitor", ai_client)
        self.observations: List[Dict] = []
    
    def observe(self, panelist: str, question: str, answer: str):
        """Record an observation during the interview"""
        self.observations.append({
            "panelist": panelist,
            "question": question,
            "answer": answer,
            "answer_length": len(answer.split()),
            "contains_specifics": self._has_specifics(answer)
        })
    
    def _has_specifics(self, answer: str) -> bool:
        """Check if answer contains specific technical details"""
        technical_indicators = [
            "kubernetes", "docker", "microservices", "api", "database",
            "cache", "queue", "monitoring", "metrics", "logs", "trace",
            "circuit breaker", "load balancer", "cdn", "sql", "nosql"
        ]
        answer_lower = answer.lower()
        return any(indicator in answer_lower for indicator in technical_indicators)
    
    def generate_dashboard(self, context: InterviewContext) -> Dict:
        """Generate comprehensive feedback dashboard"""
        if not self.observations:
            return {"error": "No observations recorded"}
        
        # Calculate metrics
        total_answers = len(self.observations)
        specific_answers = sum(1 for obs in self.observations if obs["contains_specifics"])
        avg_length = sum(obs["answer_length"] for obs in self.observations) / total_answers
        
        # Calculate overall score
        specificity_score = (specific_answers / total_answers) * 40
        depth_score = min((avg_length / 50) * 30, 30)
        completion_score = (context.total_questions / context.max_total_questions) * 30
        overall_score = int(specificity_score + depth_score + completion_score)
        
        # Identify strengths
        strengths = []
        if specific_answers >= total_answers * 0.7:
            strengths.append("Strong technical vocabulary and specific examples")
        if avg_length >= 50:
            strengths.append("Detailed and thorough responses")
        if completion_score == 30:
            strengths.append("Completed all interview questions")
        
        # Identify gaps
        critical_gaps = []
        panelist_scores = {}
        for obs in self.observations:
            panelist = obs["panelist"]
            if panelist not in panelist_scores:
                panelist_scores[panelist] = []
            panelist_scores[panelist].append(obs["contains_specifics"])
        
        for panelist, scores in panelist_scores.items():
            if sum(scores) / len(scores) < 0.5:
                critical_gaps.append({
                    "topic": f"{panelist} questions",
                    "panelist_flagged": panelist,
                    "what_went_wrong": "Responses lacked technical depth and specific examples",
                    "how_to_fix": "Study relevant technologies and practice with concrete examples"
                })
        
        return {
            "overall_score": overall_score,
            "strengths": strengths if strengths else ["Keep practicing to build more strengths"],
            "critical_gaps": critical_gaps,
            "behavioral_feedback": "Good effort. Focus on providing more specific examples with measurable outcomes.",
            "hire_recommendation": overall_score >= 70
        }


class InterviewOrchestrator:
    """Main orchestrator that manages the interview flow"""
    
    def __init__(self, ai_provider: Optional[str] = None):
        """Initialize orchestrator with AI provider"""
        try:
            # Create AI client
            self.ai_client = AIClientFactory.create_client(provider=ai_provider)
            print(f"✅ Using AI provider: {os.getenv('AI_PROVIDER', 'gemini')}")
            
            # Initialize agents with AI client
            self.hiring_manager = HiringManagerAgent(self.ai_client)
            self.system_architect = SystemArchitectAgent(self.ai_client)
            self.senior_dev = SeniorDevAgent(self.ai_client)
            self.health_monitor = HealthMonitorAgent(self.ai_client)
            
            self.panelist_order = [
                (PanelistRole.HIRING_MANAGER, self.hiring_manager),
                (PanelistRole.SYSTEM_ARCHITECT, self.system_architect),
                (PanelistRole.SENIOR_DEV, self.senior_dev)
            ]
            self.current_panelist_index = 0
            
        except Exception as e:
            print(f"❌ Failed to initialize AI client: {e}")
            print("\n💡 Tip: Check your .env file configuration")
            print("   Run: cp .env.example .env")
            print("   Then edit .env with your API keys")
            sys.exit(1)
    
    def start_interview(self, resume: str, job_description: str) -> InterviewContext:
        """Start a new interview"""
        context = InterviewContext(resume=resume, job_description=job_description)
        
        print("\n" + "="*80)
        print("🎯 PANELPULSE - AI-POWERED MOCK TECHNICAL INTERVIEW")
        print("="*80)
        print(f"\n📊 AI Provider: {os.getenv('AI_PROVIDER', 'gemini').upper()}")
        print(f"👥 Panel: {len(self.panelist_order)} interviewers")
        print(f"❓ Questions: {context.max_total_questions} total\n")
        
        return context
    
    def _ask_next_question(self, context: InterviewContext) -> str:
        """Ask the next question from the current panelist"""
        role, agent = self.panelist_order[self.current_panelist_index]
        context.current_panelist = role
        question = agent.generate_response(context)
        
        context.transcript.append({
            "role": agent.role,
            "type": "question",
            "content": question
        })
        
        return question
    
    def process_answer(self, context: InterviewContext, answer: str) -> Optional[str]:
        """Process user's answer and return next question or None if interview complete"""
        role, agent = self.panelist_order[self.current_panelist_index]
        
        # Record answer
        context.transcript.append({
            "role": "candidate",
            "type": "answer",
            "content": answer
        })
        
        # Health monitor observes
        last_question = [t for t in context.transcript if t["type"] == "question"][-1]["content"]
        self.health_monitor.observe(agent.name, last_question, answer)
        
        # Update counters
        context.questions_asked[role] += 1
        context.total_questions += 1
        
        # Check if we should move to next panelist
        if context.questions_asked[role] >= context.max_questions_per_panelist:
            self.current_panelist_index += 1
        
        # Check if interview is complete
        if context.total_questions >= context.max_total_questions:
            return None
        
        # Ask next question
        return self._ask_next_question(context)
    
    def _end_interview(self, context: InterviewContext) -> Dict:
        """End interview and generate dashboard"""
        print("\n" + "="*80)
        print("📊 GENERATING PERFORMANCE DASHBOARD...")
        print("="*80 + "\n")
        
        dashboard = self.health_monitor.generate_dashboard(context)
        return dashboard


def main():
    """Main CLI interface"""
    print("\n🚀 Welcome to PanelPulse - AI-Powered Mock Technical Interview System\n")
    
    # Get resume
    print("📝 Please paste your resume (press Enter twice when done):")
    resume_lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if line.strip() == "":
            empty_count += 1
        else:
            empty_count = 0
            resume_lines.append(line)
    resume = "\n".join(resume_lines)
    
    # Get job description
    print("\n📋 Please paste the job description (press Enter twice when done):")
    jd_lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if line.strip() == "":
            empty_count += 1
        else:
            empty_count = 0
            jd_lines.append(line)
    job_description = "\n".join(jd_lines)
    
    # Initialize orchestrator
    orchestrator = InterviewOrchestrator()
    context = orchestrator.start_interview(resume, job_description)
    
    # Start interview
    question = orchestrator._ask_next_question(context)
    question_num = 1
    
    while question:
        print(f"\n[Question {question_num}/{context.max_total_questions}]")
        print(question)
        print("\n💭 Your answer:")
        answer = input()
        
        question = orchestrator.process_answer(context, answer)
        question_num += 1
    
    # Generate dashboard
    dashboard = orchestrator._end_interview(context)
    
    # Display results
    print(json.dumps(dashboard, indent=2))
    print("\n✅ Interview complete! Good luck with your preparation! 🚀\n")


if __name__ == "__main__":
    main()
