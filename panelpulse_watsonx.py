#!/usr/bin/env python3
"""
PanelPulse with WatsonX AI Integration
Intelligent mock interview system powered by IBM watsonx.ai
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from watsonx_client import get_watsonx_client


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
    evaluations: List[Dict] = field(default_factory=list)


class WatsonXAgent:
    """Base class for watsonx-powered interview agents"""
    
    def __init__(self, name: str, role: str, focus_area: str):
        self.name = name
        self.role = role
        self.focus_area = focus_area
        self.watsonx = get_watsonx_client()
        self.questions_asked = []
    
    def generate_question(self, context: InterviewContext) -> str:
        """Generate a question using watsonx.ai"""
        print(f"🤖 {self.name} is thinking...")
        
        question = self.watsonx.generate_question(
            role=self.role,
            resume=context.resume,
            job_description=context.job_description,
            previous_questions=self.questions_asked,
            focus_area=self.focus_area
        )
        
        self.questions_asked.append(question)
        return question
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        context: InterviewContext
    ) -> Dict:
        """Evaluate an answer using watsonx.ai"""
        print(f"🤖 {self.name} is evaluating your answer...")
        
        evaluation = self.watsonx.evaluate_answer(
            question=question,
            answer=answer,
            role=self.role,
            resume=context.resume,
            job_description=context.job_description
        )
        
        return evaluation
    
    def should_follow_up(self, evaluation: Dict) -> Optional[str]:
        """Determine if a follow-up question is needed based on evaluation"""
        score = evaluation.get('score', 0)
        has_examples = evaluation.get('has_specific_examples', False)
        
        # Ask follow-up if score is low or lacks examples
        if score < 60 or not has_examples:
            weaknesses = evaluation.get('weaknesses', [])
            if weaknesses:
                return f"I noticed {weaknesses[0]}. Can you elaborate with a specific example?"
        
        return None


class HiringManagerAgent(WatsonXAgent):
    """Hiring Manager - Evaluates behavioral competencies with watsonx.ai"""
    
    def __init__(self):
        super().__init__(
            name="Hiring Manager",
            role="hiring-manager",
            focus_area="behavioral competencies, leadership, conflict resolution, and team collaboration"
        )


class SystemArchitectAgent(WatsonXAgent):
    """System Architect - Evaluates system design with watsonx.ai"""
    
    def __init__(self):
        super().__init__(
            name="System Architect",
            role="system-architect",
            focus_area="system design, scalability, distributed systems, and architectural trade-offs"
        )


class SeniorDevAgent(WatsonXAgent):
    """Senior Developer - Evaluates technical depth with watsonx.ai"""
    
    def __init__(self):
        super().__init__(
            name="Senior Developer",
            role="senior-dev",
            focus_area="technical depth, debugging methodology, framework expertise, and best practices"
        )


class HealthMonitorAgent:
    """Silent agent that uses watsonx.ai to generate comprehensive feedback"""
    
    def __init__(self):
        self.name = "Health Monitor"
        self.role = "health-monitor"
        self.watsonx = get_watsonx_client()
    
    def generate_dashboard(self, context: InterviewContext) -> Dict:
        """Generate final feedback dashboard using watsonx.ai"""
        print("\n🤖 Generating comprehensive interview analysis...")
        
        dashboard = self.watsonx.generate_dashboard(
            evaluations=context.evaluations,
            resume=context.resume,
            job_description=context.job_description
        )
        
        return dashboard


class InterviewOrchestrator:
    """Main controller that manages the watsonx-powered interview flow"""
    
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
        self.current_evaluation = None
    
    def start_interview(self, resume: str, job_description: str):
        """Initialize and start the interview"""
        self.context.resume = resume
        self.context.job_description = job_description
        
        print("\n" + "="*80)
        print("🎯 PANELPULSE - AI-POWERED MOCK INTERVIEW")
        print("   Powered by IBM watsonx.ai")
        print("="*80)
        print("\n📋 Interview Setup Complete")
        print(f"   Resume: {len(resume)} characters")
        print(f"   Job Description: {len(job_description)} characters")
        print("\n👥 AI Interview Panel:")
        print("   • Hiring Manager - Behavioral & Leadership (watsonx.ai)")
        print("   • System Architect - System Design & Scalability (watsonx.ai)")
        print("   • Senior Developer - Technical Depth & Debugging (watsonx.ai)")
        print("\n" + "="*80)
        print("The AI will generate personalized questions based on your resume.")
        print("Each answer will be intelligently evaluated by watsonx.ai.")
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
        
        # Generate question using watsonx.ai
        question = agent.generate_question(self.context)
        self.last_question = question
        self.awaiting_answer = True
        self.context.current_panelist = current_role
        self.context.questions_asked[current_role] += 1
        self.context.total_questions += 1
        
        print(f"\n[Question {self.context.total_questions}/{self.context.max_total_questions}]")
        print(f"**{agent.name}:** {question}")
        print("\n" + "-"*80)
    
    def process_answer(self, answer: str):
        """Process user's answer with watsonx.ai evaluation"""
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
        
        # Evaluate answer using watsonx.ai
        agent = self.agents[self.context.current_panelist]
        evaluation = agent.evaluate_answer(
            self.last_question,
            answer,
            self.context
        )
        
        # Store evaluation
        evaluation['panelist'] = self.context.current_panelist.value
        evaluation['question'] = self.last_question
        evaluation['answer'] = answer
        self.context.evaluations.append(evaluation)
        
        # Show quick feedback
        score = evaluation.get('score', 0)
        print(f"\n✓ Answer recorded. Score: {score}/100")
        
        self.awaiting_answer = False
        
        # Check for follow-up
        follow_up = agent.should_follow_up(evaluation)
        
        if follow_up and self.context.total_questions < self.context.max_total_questions:
            print(f"\n**{agent.name}:** {follow_up}")
            print("-"*80)
            self.awaiting_answer = True
            self.last_question = follow_up
            # Increment question count for follow-up
            self.context.total_questions += 1
            self.context.questions_asked[self.context.current_panelist] += 1
        else:
            # Move to next question
            print("\n🤖 Moving to next question...\n")
            self._ask_next_question()
    
    def _end_interview(self):
        """End the interview and generate watsonx.ai-powered feedback"""
        print("\n" + "="*80)
        print("🎬 INTERVIEW COMPLETE")
        print("="*80)
        print("\n🤖 WatsonX AI is analyzing your performance...\n")
        
        # Generate dashboard using watsonx.ai
        dashboard = self.health_monitor.generate_dashboard(self.context)
        
        # Display dashboard
        print("="*80)
        print("📊 AI-POWERED INTERVIEW ANALYSIS")
        print("   Generated by IBM watsonx.ai")
        print("="*80)
        print(f"\n🎯 Overall Score: {dashboard['overall_score']}/100")
        print(f"{'█' * (dashboard['overall_score'] // 2)}")
        
        print("\n✅ Strengths:")
        for strength in dashboard.get('strengths', []):
            print(f"   • {strength}")
        
        if dashboard.get('critical_gaps'):
            print("\n⚠️  Critical Gaps:")
            for gap in dashboard['critical_gaps']:
                print(f"\n   📌 {gap.get('topic', 'Unknown')}")
                print(f"      Flagged by: {gap.get('panelist_flagged', 'Unknown')}")
                print(f"      Issue: {gap.get('what_went_wrong', 'N/A')}")
                print(f"      Fix: {gap.get('how_to_fix', 'N/A')}")
        
        print(f"\n💬 Behavioral Feedback:")
        print(f"   {dashboard.get('behavioral_feedback', 'N/A')}")
        
        hire_rec = dashboard.get('hire_recommendation', False)
        print(f"\n🎯 Hire Recommendation: {'✅ YES' if hire_rec else '❌ NO'}")
        
        print("\n" + "="*80)
        print("📄 Full JSON Output:")
        print("="*80)
        print(json.dumps(dashboard, indent=2))
        print("="*80 + "\n")


def main():
    """Main entry point for the watsonx-powered application"""
    print("\n🚀 Welcome to PanelPulse - AI-Powered Mock Interview")
    print("   Powered by IBM watsonx.ai\n")
    
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
    
    print("\n✨ Thank you for using PanelPulse with watsonx.ai!")
    print("   Your interview has been intelligently analyzed.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interview interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
