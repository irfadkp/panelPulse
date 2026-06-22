#!/usr/bin/env python3
"""
PanelPulse - Mock Technical Interview Orchestrator
A multi-agent system that simulates a realistic technical interview panel.
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


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
    """Base class for all interview agents"""
    
    def __init__(self, name: str, role: str, model: str = "gemini-3.5-flash"):
        self.name = name
        self.role = role
        self.model = model
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate a response based on context. Override in subclasses."""
        raise NotImplementedError


class HiringManagerAgent(BaseAgent):
    """Hiring Manager - Evaluates behavioral competencies"""
    
    def __init__(self):
        super().__init__("Hiring Manager", "hiring-manager", "gemini-3.5-flash")
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
            # Ask initial question
            question = self.questions[self.question_index % len(self.questions)]
            self.question_index += 1
            return f"{self.name}: {question}"
        else:
            # Provide follow-up if answer is vague
            if len(user_input.split()) < 30 or "we" in user_input.lower():
                return f"{self.name}: That's interesting. Can you be more specific about YOUR role in that situation? What actions did YOU personally take?"
            return ""


class SystemArchitectAgent(BaseAgent):
    """System Architect - Evaluates system design and scalability"""
    
    def __init__(self):
        super().__init__("System Architect", "system-architect", "gemini-3.5-pro")
        self.questions = [
            "Design a distributed tracing system for a microservices architecture with 50+ services. How would you handle trace sampling and storage at scale?",
            "You're building a real-time analytics pipeline that needs to process 100K events/second. Walk me through your architecture choices and the trade-offs.",
            "How would you design a multi-region deployment strategy for a critical service that requires 99.99% uptime? What are the failure modes you'd plan for?",
            "Explain how you would implement circuit breakers in a Kubernetes environment. What metrics would you monitor?"
        ]
        self.question_index = 0
    
    def generate_response(self, context: InterviewContext, user_input: str = "") -> str:
        """Generate system design question or hint"""
        if not user_input:
            question = self.questions[self.question_index % len(self.questions)]
            self.question_index += 1
            return f"{self.name}: {question}"
        else:
            return ""
    
    def provide_hint(self, context: InterviewContext) -> str:
        """Provide a small hint when user struggles"""
        return f"{self.name}: Let me give you a hint - think about the trade-offs between consistency and availability in this scenario. How would CAP theorem apply here?"


class SeniorDevAgent(BaseAgent):
    """Senior Developer - Evaluates technical depth and debugging"""
    
    def __init__(self):
        super().__init__("Senior Developer", "senior-dev", "gemini-3.5-flash")
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
    
    def __init__(self):
        super().__init__("Health Monitor", "health-monitor", "gemini-3.5-pro")
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
    
    def _assess_answer_quality(self, answer: str, panelist: str) -> int:
        """Assess the quality of the answer content (0-40 points)"""
        answer_lower = answer.lower()
        quality_score = 40  # Start with full points
        
        # Red flags that reduce score
        red_flags = [
            ("i don't know", -15),
            ("not sure", -10),
            ("maybe", -5),
            ("probably", -5),
            ("i guess", -10),
            ("someone else", -15),
            ("another team", -15),
            ("waited for", -10),
            ("assumed", -10),
            ("restart", -10),
            ("buy bigger", -15),
            ("manually", -10),
            ("feels", -10),
            ("trust", -8),
            ("stopped caring", -20),
            ("gave up", -20),
            ("blame", -15),
            ("not my", -20)
        ]
        
        for phrase, penalty in red_flags:
            if phrase in answer_lower:
                quality_score += penalty
        
        # Positive indicators
        positive_indicators = [
            ("i implemented", 5),
            ("i designed", 5),
            ("i led", 5),
            ("i analyzed", 5),
            ("metrics showed", 5),
            ("reduced by", 5),
            ("improved by", 5),
            ("specific example", 5),
            ("measured", 5),
            ("data-driven", 5)
        ]
        
        for phrase, bonus in positive_indicators:
            if phrase in answer_lower:
                quality_score = min(quality_score + bonus, 40)
        
        return max(0, min(quality_score, 40))
    
    def generate_dashboard(self, context: InterviewContext) -> Dict:
        """Generate final feedback dashboard JSON"""
        # Analyze observations
        total_answers = len(self.observations)
        avg_answer_length = sum(obs["answer_length"] for obs in self.observations) / max(total_answers, 1)
        
        # Build detailed Q&A with scores
        qa_details = []
        for i, entry in enumerate(context.transcript, 1):
            obs = self.observations[i-1] if i-1 < len(self.observations) else None
            
            # Calculate individual answer score
            answer_score = 0
            explanation = []
            
            if obs:
                # Quality assessment (40 points) - checks for red flags and positive indicators
                quality_score = self._assess_answer_quality(entry["answer"], entry["panelist"])
                answer_score += quality_score
                
                if quality_score >= 35:
                    explanation.append(f"✓ High-quality answer with concrete examples ({quality_score}/40)")
                elif quality_score >= 25:
                    explanation.append(f"○ Adequate answer but could be stronger ({quality_score}/40)")
                else:
                    explanation.append(f"✗ Weak answer with red flags or vague statements ({quality_score}/40)")
                
                # Depth (30 points)
                word_count = obs["answer_length"]
                if word_count >= 50:
                    depth_points = 30
                    explanation.append(f"✓ Detailed response ({word_count} words)")
                elif word_count >= 30:
                    depth_points = 20
                    explanation.append(f"○ Moderate detail ({word_count} words)")
                else:
                    depth_points = 10
                    explanation.append(f"✗ Brief response ({word_count} words)")
                answer_score += depth_points
                
                # Completeness (30 points)
                if word_count > 0:
                    answer_score += 30
                    explanation.append("✓ Question answered")
            
            qa_details.append({
                "question_number": i,
                "panelist": entry["panelist"],
                "question": entry["question"],
                "answer": entry["answer"],
                "score": answer_score,
                "max_score": 100,
                "explanation": explanation
            })
        
        # Identify gaps
        critical_gaps = []
        behavioral_weak = sum(1 for obs in self.observations 
                            if obs["panelist"] == "hiring-manager" and obs["answer_length"] < 30)
        
        if behavioral_weak > 0:
            critical_gaps.append({
                "topic": "Behavioral/Leadership",
                "panelist_flagged": "hiring-manager",
                "what_went_wrong": "Answers lacked specific examples and concrete details about personal contributions",
                "how_to_fix": "Use the STAR method (Situation, Task, Action, Result) to structure behavioral answers with specific metrics and outcomes"
            })
        
        # Check for technical depth
        technical_weak = sum(1 for obs in self.observations 
                           if obs["panelist"] in ["system-architect", "senior-dev"] 
                           and not obs["contains_specifics"])
        
        if technical_weak > 0:
            critical_gaps.append({
                "topic": "System Design/Architecture",
                "panelist_flagged": "system-architect",
                "what_went_wrong": "Responses lacked technical depth and specific technology choices",
                "how_to_fix": "Study distributed systems patterns, CAP theorem, and practice designing scalable architectures with specific technology stacks"
            })
        
        # Calculate overall score from individual answer scores
        total_score = sum(qa["score"] for qa in qa_details)
        max_possible_score = len(qa_details) * 100
        overall_score = int((total_score / max_possible_score) * 100) if max_possible_score > 0 else 0
        
        # Determine strengths based on quality scores
        high_quality_answers = sum(1 for qa in qa_details if qa["score"] >= 70)
        strengths = []
        if high_quality_answers >= total_answers * 0.6:
            strengths.append("Strong technical vocabulary and specific examples")
        if avg_answer_length > 40:
            strengths.append("Detailed and thorough responses")
        if context.total_questions == context.max_total_questions:
            strengths.append("Completed full interview with engagement")
        
        if not strengths:
            strengths = ["Showed up and participated in the interview"]
        
        return {
            "overall_score": overall_score,
            "strengths": strengths,
            "critical_gaps": critical_gaps,
            "behavioral_feedback": self._generate_behavioral_feedback(behavioral_weak, total_answers),
            "hire_recommendation": overall_score >= 70,
            "questions_and_answers": qa_details
        }
    
    def _generate_behavioral_feedback(self, weak_count: int, total: int) -> str:
        """Generate behavioral feedback summary"""
        if weak_count == 0:
            return "Strong behavioral responses with concrete examples and clear ownership of outcomes."
        elif weak_count <= total * 0.3:
            return "Good behavioral awareness, but some answers could benefit from more specific examples and metrics."
        else:
            return "Behavioral responses need significant improvement. Focus on providing specific examples with measurable outcomes and clear personal contributions."


class InterviewOrchestrator:
    """Main controller that manages the interview flow"""
    
    def __init__(self):
        self.context = InterviewContext()
        self.agents = {
            PanelistRole.HIRING_MANAGER: HiringManagerAgent(),
            PanelistRole.SYSTEM_ARCHITECT: SystemArchitectAgent(),
            PanelistRole.SENIOR_DEV: SeniorDevAgent()
        }
        self.health_monitor = HealthMonitorAgent()
        self.panelist_order = [
            PanelistRole.HIRING_MANAGER,
            PanelistRole.SYSTEM_ARCHITECT,
            PanelistRole.SENIOR_DEV
        ]
        self.current_panelist_index = 0
        self.awaiting_answer = False
        self.last_question = ""
    
    def start_interview(self, resume: str, job_description: str):
        """Initialize and start the interview"""
        self.context.resume = resume
        self.context.job_description = job_description
        
        print("\n" + "="*80)
        print("🎯 PANELPULSE - MOCK TECHNICAL INTERVIEW")
        print("="*80)
        print("\n📋 Interview Setup Complete")
        print(f"   Resume: {len(resume)} characters")
        print(f"   Job Description: {len(job_description)} characters")
        print("\n👥 Interview Panel:")
        print("   • Hiring Manager - Behavioral & Leadership")
        print("   • System Architect - System Design & Scalability")
        print("   • Senior Developer - Technical Depth & Debugging")
        print("\n" + "="*80)
        print("The interview will consist of 6 questions (2 per panelist).")
        print("Please provide thoughtful, detailed answers.")
        print("="*80 + "\n")
        
        # Start with first question
        self._ask_next_question()
    
    def _ask_next_question(self):
        """Ask the next question from current panelist"""
        if self.context.total_questions >= self.context.max_total_questions:
            self._end_interview()
            return
        
        # Get current panelist
        current_role = self.panelist_order[self.current_panelist_index]
        agent = self.agents[current_role]
        
        # Check if current panelist has asked their quota
        if self.context.questions_asked[current_role] >= self.context.max_questions_per_panelist:
            # Move to next panelist
            self.current_panelist_index = (self.current_panelist_index + 1) % len(self.panelist_order)
            current_role = self.panelist_order[self.current_panelist_index]
            agent = self.agents[current_role]
        
        # Generate question
        question = agent.generate_response(self.context)
        self.last_question = question
        self.awaiting_answer = True
        self.context.current_panelist = current_role
        self.context.questions_asked[current_role] += 1
        self.context.total_questions += 1
        
        print(f"\n[Question {self.context.total_questions}/{self.context.max_total_questions}]")
        print(question)
        print("\n" + "-"*80)
    
    def process_answer(self, answer: str):
        """Process user's answer and continue interview"""
        if not self.awaiting_answer:
            print("⚠️  No question is currently active. Please wait for the next question.")
            return
        
        if self.context.current_panelist is None:
            print("⚠️  Error: No active panelist. Please restart the interview.")
            return
        
        # Record answer
        self.context.transcript.append({
            "panelist": self.context.current_panelist.value,
            "question": self.last_question,
            "answer": answer
        })
        
        # Let health monitor observe
        self.health_monitor.observe(
            self.context.current_panelist.value,
            self.last_question,
            answer
        )
        
        self.awaiting_answer = False
        
        # Check for follow-up
        agent = self.agents[self.context.current_panelist]
        follow_up = agent.generate_response(self.context, answer)
        
        if follow_up:
            print(f"\n{follow_up}")
            print("-"*80)
            self.awaiting_answer = True
            self.last_question = follow_up
        else:
            # Move to next question
            print("\n✓ Answer recorded. Moving to next question...\n")
            self._ask_next_question()
    
    def _end_interview(self):
        """End the interview and generate feedback"""
        print("\n" + "="*80)
        print("🎬 INTERVIEW COMPLETE")
        print("="*80)
        print("\nGenerating your Interview Health Trace Dashboard...\n")
        
        # Generate dashboard
        dashboard = self.health_monitor.generate_dashboard(self.context)
        
        # Display dashboard
        print("="*80)
        print("📊 INTERVIEW HEALTH TRACE DASHBOARD")
        print("="*80)
        print(f"\n🎯 Overall Score: {dashboard['overall_score']}/100")
        print(f"{'█' * (dashboard['overall_score'] // 2)}")
        
        print("\n✅ Strengths:")
        for strength in dashboard['strengths']:
            print(f"   • {strength}")
        
        if dashboard['critical_gaps']:
            print("\n⚠️  Critical Gaps:")
            for gap in dashboard['critical_gaps']:
                print(f"\n   📌 {gap['topic']}")
                print(f"      Flagged by: {gap['panelist_flagged']}")
                print(f"      Issue: {gap['what_went_wrong']}")
                print(f"      Fix: {gap['how_to_fix']}")
        
        print(f"\n💬 Behavioral Feedback:")
        print(f"   {dashboard['behavioral_feedback']}")
        
        print(f"\n🎯 Hire Recommendation: {'✅ YES' if dashboard['hire_recommendation'] else '❌ NO'}")
        
        print("\n" + "="*80)
        print("📄 Full JSON Output:")
        print("="*80)
        print(json.dumps(dashboard, indent=2))
        print("="*80 + "\n")


def main():
    """Main entry point for the application"""
    print("\n🚀 Welcome to PanelPulse - Mock Technical Interview System\n")
    
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
    resume = "\n".join(resume_lines).strip()
    
    if not resume:
        print("❌ Resume is required. Exiting.")
        sys.exit(1)
    
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
    job_description = "\n".join(jd_lines).strip()
    
    if not job_description:
        print("❌ Job description is required. Exiting.")
        sys.exit(1)
    
    # Start interview
    orchestrator = InterviewOrchestrator()
    orchestrator.start_interview(resume, job_description)
    
    # Interview loop
    while orchestrator.context.total_questions < orchestrator.context.max_total_questions:
        if orchestrator.awaiting_answer:
            print("\n💭 Your answer: ", end="")
            answer = input().strip()
            
            if not answer:
                print("⚠️  Please provide an answer.")
                continue
            
            orchestrator.process_answer(answer)
    
    print("\n✨ Thank you for using PanelPulse! Good luck with your real interviews!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interview interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

# Made with Bob
