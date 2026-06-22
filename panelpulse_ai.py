#!/usr/bin/env python3
"""
PanelPulse AI - AI-powered mock technical interview orchestrator.
Uses the local Bob Shell Wrapper service for question generation and evaluation.
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from wrapper_ai_client import get_wrapper_client


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


class AIAgent:
    """Base AI-powered agent using the Bob Shell Wrapper service"""

    def __init__(self, name: str, role: str, focus_area: str):
        self.name = name
        self.role = role
        self.focus_area = focus_area
        self.ai_client = get_wrapper_client()
        self.questions_asked = []

    def generate_question(self, context: InterviewContext) -> str:
        """Generate a contextual question using the wrapper-backed AI service"""
        question_text = self.ai_client.generate_question(
            role=self.role,
            resume=context.resume,
            job_description=context.job_description,
            previous_questions=self.questions_asked,
            focus_area=self.focus_area
        )

        self.questions_asked.append(question_text)
        return f"**{self.name}:** {question_text}"

    def evaluate_answer(self, question: str, answer: str, context: InterviewContext) -> Dict:
        """Evaluate answer using the wrapper-backed AI service"""
        return self.ai_client.evaluate_answer(
            question=question,
            answer=answer,
            role=self.role,
            resume=context.resume,
            job_description=context.job_description
        )


class HiringManagerAgent(AIAgent):
    """AI-powered Hiring Manager - Evaluates behavioral competencies"""

    def __init__(self):
        super().__init__(
            name="Hiring Manager",
            role="hiring-manager",
            focus_area="Behavioral competencies, leadership, conflict resolution, ownership, and team collaboration"
        )


class SystemArchitectAgent(AIAgent):
    """AI-powered System Architect - Evaluates system design and scalability"""

    def __init__(self):
        super().__init__(
            name="System Architect",
            role="system-architect",
            focus_area="System design, scalability, distributed systems, architecture patterns, and trade-offs"
        )


class SeniorDevAgent(AIAgent):
    """AI-powered Senior Developer - Evaluates technical depth and debugging"""

    def __init__(self):
        super().__init__(
            name="Senior Developer",
            role="senior-dev",
            focus_area="Technical depth, debugging methodology, code quality, and problem-solving"
        )


class HealthMonitorAgent:
    """AI-powered agent that analyzes interview and generates comprehensive feedback"""

    def __init__(self):
        self.ai_client = get_wrapper_client()

    def generate_dashboard(self, context: InterviewContext) -> Dict:
        """Generate comprehensive interview dashboard using the wrapper-backed AI service"""

        qa_details = []
        for i, entry in enumerate(context.transcript, 1):
            evaluation = context.evaluations[i - 1] if i - 1 < len(context.evaluations) else {}

            score = evaluation.get('score', 0)
            strengths = evaluation.get('strengths', [])
            weaknesses = evaluation.get('weaknesses', [])
            suggestions = evaluation.get('suggestions', [])

            explanation = []
            if score >= 70:
                explanation.append(f"✓ Strong answer (Score: {score}/100)")
            elif score >= 50:
                explanation.append(f"○ Adequate answer (Score: {score}/100)")
            else:
                explanation.append(f"✗ Weak answer (Score: {score}/100)")

            if strengths:
                explanation.append(f"Strengths: {', '.join(strengths[:2])}")
            if weaknesses:
                explanation.append(f"Weaknesses: {', '.join(weaknesses[:2])}")

            qa_details.append({
                "question_number": i,
                "panelist": entry["panelist"],
                "question": entry["question"],
                "answer": entry["answer"],
                "score": score,
                "max_score": 100,
                "explanation": explanation,
                "ai_strengths": strengths,
                "ai_weaknesses": weaknesses,
                "ai_suggestions": suggestions
            })

        dashboard = self.ai_client.generate_dashboard(
            evaluations=context.evaluations,
            resume=context.resume,
            job_description=context.job_description
        )

        dashboard['questions_and_answers'] = qa_details
        return dashboard


class InterviewOrchestrator:
    """Main controller that manages the AI-powered interview flow"""

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
        """Initialize and start the AI-powered interview"""
        self.context.resume = resume
        self.context.job_description = job_description

        print("\n" + "=" * 80)
        print("🚀 PANELPULSE AI - INTELLIGENT MOCK INTERVIEW")
        print("=" * 80)
        print("\n📋 Interview Setup Complete")
        print(f"   Resume: {len(resume)} characters")
        print(f"   Job Description: {len(job_description)} characters")
        print("\n🤖 AI-Powered Interview Panel:")
        print("   • Hiring Manager - Behavioral & Leadership")
        print("   • System Architect - System Design & Scalability")
        print("   • Senior Developer - Technical Depth & Debugging")
        print("\n🔌 AI Service: /root/bob-shell-wrapper-main")
        print("=" * 80)
        print("The interview will consist of 6 AI-generated questions (2 per panelist).")
        print("Questions are dynamically generated based on your resume and the job requirements.")
        print("=" * 80 + "\n")

        self._ask_next_question()

    def _ask_next_question(self):
        """Ask the next AI-generated question from current panelist"""
        if self.context.total_questions >= self.context.max_total_questions:
            self._end_interview()
            return

        current_role = self.panelist_order[self.current_panelist_index]
        agent = self.agents[current_role]

        if self.context.questions_asked[current_role] >= self.context.max_questions_per_panelist:
            self.current_panelist_index = (self.current_panelist_index + 1) % len(self.panelist_order)
            current_role = self.panelist_order[self.current_panelist_index]
            agent = self.agents[current_role]

        print(f"\n🤖 Generating question using AI service...")
        question = agent.generate_question(self.context)
        self.last_question = question
        self.awaiting_answer = True
        self.context.current_panelist = current_role
        self.context.questions_asked[current_role] += 1
        self.context.total_questions += 1

        print(f"\n[Question {self.context.total_questions}/{self.context.max_total_questions}]")
        print(question)
        print("\n" + "-" * 80)

    def process_answer(self, answer: str):
        """Process user's answer with AI evaluation and continue interview"""
        if not self.awaiting_answer:
            print("⚠️  No question is currently active. Please wait for the next question.")
            return

        if self.context.current_panelist is None:
            print("⚠️  Error: No active panelist. Please restart the interview.")
            return

        self.context.transcript.append({
            "panelist": self.context.current_panelist.value,
            "question": self.last_question,
            "answer": answer
        })

        print("\n🤖 Evaluating answer using AI service...")
        agent = self.agents[self.context.current_panelist]
        evaluation = agent.evaluate_answer(self.last_question, answer, self.context)
        self.context.evaluations.append(evaluation)

        score = evaluation.get('score', 0)
        print(f"✓ Answer recorded (AI Score: {score}/100)")

        self.awaiting_answer = False

        print("\n✓ Moving to next question...\n")
        self._ask_next_question()

    def _end_interview(self):
        """End the interview and generate AI-powered feedback"""
        print("\n" + "=" * 80)
        print("🎬 INTERVIEW COMPLETE")
        print("=" * 80)
        print("\n🤖 Generating comprehensive AI-powered feedback...\n")

        dashboard = self.health_monitor.generate_dashboard(self.context)

        print("=" * 80)
        print("📊 AI-POWERED INTERVIEW DASHBOARD")
        print("=" * 80)
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

        print("\n" + "=" * 80)
        print("📄 Full JSON Output:")
        print("=" * 80)
        print(json.dumps(dashboard, indent=2))
        print("=" * 80 + "\n")


def main():
    """Main entry point for the AI-powered application"""
    print("\n🚀 Welcome to PanelPulse AI - Intelligent Mock Interview System")
    print("🔌 Using AI services from /root/bob-shell-wrapper-main\n")

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

    orchestrator = InterviewOrchestrator()
    orchestrator.start_interview(resume, job_description)

    while orchestrator.context.total_questions < orchestrator.context.max_total_questions:
        if orchestrator.awaiting_answer:
            print("\n💭 Your answer: ", end="")
            answer = input().strip()

            if not answer:
                print("⚠️  Please provide an answer.")
                continue

            orchestrator.process_answer(answer)

    print("\n✨ Thank you for using PanelPulse AI! Good luck with your real interviews!\n")


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