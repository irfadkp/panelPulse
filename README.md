# PanelPulse - Mock Technical Interview System

🎯 **Realistic technical interview practice with multi-agent orchestration**

PanelPulse simulates a complete technical interview panel with three specialized interviewers, providing job seekers with realistic practice and detailed performance feedback. Available in both CLI and beautiful web interface versions.

![Interview Orchestrator Architecture](interview_orchestrator.png)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Web Application](#-web-application)
- [Configuration](#-configuration)
- [Dashboard & Feedback](#-dashboard--feedback)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🎯 Overview

PanelPulse provides a comprehensive mock interview experience with:

- **Three Specialized Interviewers**:
  - 🎭 **Hiring Manager** - Behavioral competencies and leadership
  - 🏗️ **System Architect** - System design and scalability
  - 💻 **Senior Developer** - Technical depth and debugging

- **Silent Performance Monitor**: Real-time analysis and feedback generation

- **Multiple Interfaces**:
  - CLI version for terminal-based interviews
  - Modern web application with React + Flask

## ✨ Features

### Core Features
- ✅ Realistic multi-agent interview simulation
- ✅ 6 questions total (2 per panelist)
- ✅ Intelligent follow-up questions
- ✅ Real-time performance analysis
- ✅ Comprehensive feedback dashboard
- ✅ Actionable improvement suggestions
- ✅ Privacy-first (no data persistence)

### Web Application Features
- 🎨 Beautiful modern UI with Tailwind CSS
- 📊 Visual score dashboard with charts
- 📱 Fully responsive design
- ⚡ Real-time progress tracking
- 🎬 Smooth animations with Framer Motion
- 💾 Download report as JSON

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (required for all versions)
- **Node.js 16+** (required for web version)
- **AI Provider API Key** (optional, for AI-powered version)

### Fastest Way to Run

#### CLI Version (No AI Required)

```bash
cd /root/panelpulse
python3 panelpulse.py
```

#### AI-Powered Version (Pluggable AI Providers)

PanelPulse supports multiple AI providers - choose the one you prefer!

**Supported Providers:**
- 🤖 **ChatGPT** (OpenAI) - GPT-4, GPT-3.5-turbo
- 🔮 **Gemini** (Google) - Gemini Pro
- 🎭 **Mock** (No API key needed) - Simple rule-based responses

**Setup:**

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and configure your preferred provider
nano .env

# 3. Run AI-powered version
python3 panelpulse_ai.py
```

**Example .env configuration:**

```bash
# For ChatGPT
AI_PROVIDER=chatgpt
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4

# OR for Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-pro

# OR for Mock (no API key needed)
AI_PROVIDER=mock
```

**Get API Keys:**
- ChatGPT: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey

#### Web Version (2 Commands)

```bash
# Terminal 1 - Backend
cd /root/panelpulse
pip3 install Flask flask-cors
python3 app.py

# Terminal 2 - Frontend
cd /root/panelpulse/frontend
npm install
npm run dev
```

Then open: **http://localhost:3000**

## 🏗️ Architecture

### System Overview

PanelPulse uses a **multi-agent orchestration pattern** where a central coordinator manages the flow between specialized interviewer agents.

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│              (CLI / Web Browser / API Client)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Interview Orchestrator                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ InterviewContext (State Management)                       │  │
│  │  - resume: str                                            │  │
│  │  - job_description: str                                   │  │
│  │  - transcript: List[Dict]                                 │  │
│  │  - current_panelist: PanelistRole                         │  │
│  │  - questions_asked: Dict[PanelistRole, int]               │  │
│  │  - total_questions: int                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  Flow Control:                                                   │
│  1. start_interview() - Initialize context                       │
│  2. _ask_next_question() - Route to panelist                     │
│  3. process_answer() - Record & analyze                          │
│  4. _end_interview() - Generate dashboard                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Hiring     │    │   System     │    │   Senior     │
│   Manager    │    │  Architect   │    │  Developer   │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ Questions:   │    │ Questions:   │    │ Questions:   │
│ - Behavioral │    │ - System     │    │ - Technical  │
│ - Leadership │    │   Design     │    │   Depth      │
│ - Conflict   │    │ - Scalability│    │ - Debugging  │
│              │    │ - Trade-offs │    │ - Best       │
│ Follow-ups:  │    │              │    │   Practices  │
│ - Probe for  │    │ Hints:       │    │              │
│   specifics  │    │ - CAP theorem│    │ Scenarios:   │
│ - Challenge  │    │ - Patterns   │    │ - Pod crash  │
│   vague "we" │    │              │    │ - Memory leak│
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Health Monitor     │
                  │  (Silent Observer)   │
                  ├──────────────────────┤
                  │ Observations:        │
                  │ - Answer length      │
                  │ - Technical depth    │
                  │ - Specificity        │
                  │ - Completeness       │
                  │                      │
                  │ Analysis:            │
                  │ - Score calculation  │
                  │ - Gap identification │
                  │ - Strength detection │
                  │                      │
                  │ Output:              │
                  │ - JSON dashboard     │
                  │ - Recommendations    │
                  └──────────────────────┘
```

### Design Principles

1. **Single Responsibility**: Each agent has one clear purpose
2. **Separation of Concerns**: Interview flow, question generation, and analysis are separate
3. **Extensibility**: Easy to add new panelists or modify questions
4. **Stateful Management**: Interview context tracks all state
5. **Silent Observation**: Health monitor doesn't interfere with interview flow

### Agent Responsibilities

#### 1. Interview Orchestrator
- Main controller managing interview flow
- Routes questions between panelists
- Ensures structured turn-taking (2 questions per panelist)
- Triggers final dashboard generation

#### 2. Hiring Manager Agent
- Evaluates behavioral competencies and leadership
- Asks scenario-based questions (STAR method)
- Probes for specific personal contributions
- Follows up on vague "we" answers

**Example Questions**:
- "Tell me about a time you strongly disagreed with a product owner..."
- "Describe a situation where you had to deliver bad news to stakeholders..."

#### 3. System Architect Agent
- Evaluates system design and scalability knowledge
- Asks about distributed systems, Kubernetes, observability
- Focuses on trade-offs and architectural decisions
- Can provide hints when candidates struggle

**Example Questions**:
- "Design a distributed logging system for 1000 microservices..."
- "How would you ensure zero-downtime deployments in Kubernetes?"

#### 4. Senior Developer Agent
- Evaluates technical depth and debugging skills
- Asks framework-specific questions
- Presents hypothetical debugging scenarios
- Tests knowledge of best practices

**Example Questions**:
- "A pod keeps crashing with OOMKilled. Walk me through your debugging steps..."
- "Explain your approach to optimizing a slow database query..."

#### 5. Health Monitor Agent
- Silent observer during interview
- Analyzes all responses in real-time
- Tracks knowledge gaps and weak areas
- Generates comprehensive feedback dashboard

## 🤖 AI Provider System

PanelPulse features a **pluggable AI provider architecture** that allows you to choose your preferred AI service. The system is designed to be flexible and extensible.

### Architecture

```
┌─────────────────────────────────────────┐
│     Interview Orchestrator              │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │    AI Client Factory              │ │
│  │  (Provider Selection)             │ │
│  └───────────┬───────────────────────┘ │
│              │                          │
│    ┌─────────┼─────────┐               │
│    │         │         │               │
│    ▼         ▼         ▼               │
│  ┌────┐  ┌────┐  ┌────┐               │
│  │GPT │  │Gem │  │Mock│               │
│  │ 4  │  │ini │  │    │               │
│  └────┘  └────┘  └────┘               │
└─────────────────────────────────────────┘
```

### Supported Providers

| Provider | Models | API Key Required | Best For |
|----------|--------|------------------|----------|
| **ChatGPT** | GPT-4, GPT-3.5-turbo | ✅ Yes | Advanced reasoning, detailed feedback |
| **Gemini** | Gemini Pro | ✅ Yes | Fast responses, good quality |
| **Mock** | Rule-based | ❌ No | Testing, no API costs |

### Configuration

**1. Copy environment template:**
```bash
cp .env.example .env
```

**2. Edit .env file:**
```bash
# Choose your provider
AI_PROVIDER=gemini  # or chatgpt, mock

# Add your API key
GEMINI_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
```

**3. Run AI-powered version:**
```bash
python3 panelpulse_ai.py
```

### Getting API Keys

#### ChatGPT (OpenAI)
1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in
3. Create new API key
4. Copy to `.env` as `OPENAI_API_KEY`

#### Gemini (Google)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy to `.env` as `GEMINI_API_KEY`

### Adding Custom Providers

Want to add your own AI provider? It's easy!

**1. Create a new client:**
```python
# ai_clients/my_provider_client.py
from .base_client import BaseAIClient

class MyProviderClient(BaseAIClient):
    def generate(self, prompt, max_tokens=500, temperature=0.7, **kwargs):
        # Your implementation here
        pass
    
    def validate_credentials(self):
        # Validation logic
        pass
```

**2. Register in factory:**
```python
# ai_clients/client_factory.py
SUPPORTED_PROVIDERS = {
    'myprovider': MyProviderClient,
    # ... existing providers
}
```

**3. Configure in .env:**
```bash
AI_PROVIDER=myprovider
MYPROVIDER_API_KEY=your_key
```

## 📦 Installation

### Full Installation

```bash
# 1. Clone or navigate to the repository
cd /root/panelpulse

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Install Node dependencies (for web version)
cd frontend
npm install
cd ..
```

### Minimal Installation (CLI Only)

```bash
# No dependencies needed!
python3 panelpulse.py
```

### System-Wide Installation (Alternative)

```bash
# Python packages
sudo apt install python3-flask python3-flask-cors -y

# Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 💻 Usage

### CLI Version

#### Basic Usage

```bash
python3 panelpulse.py
```

#### Interview Flow

1. **Provide Resume**: Paste your resume and press Enter twice
2. **Provide Job Description**: Paste the target job description and press Enter twice
3. **Answer Questions**: The system will ask 6 questions total (2 per panelist)
4. **Receive Feedback**: Get a detailed dashboard with scores and improvement areas

#### Example Session

```
🚀 Welcome to PanelPulse - Mock Technical Interview System

📝 Please paste your resume (press Enter twice when done):
Senior Software Engineer with 5 years experience in distributed systems,
Kubernetes, and microservices architecture...


📋 Please paste the job description (press Enter twice when done):
Looking for Senior Backend Engineer with expertise in Kubernetes...


🎯 PANELPULSE - MOCK TECHNICAL INTERVIEW
================================================================================

[Question 1/6]
**Hiring Manager:** Tell me about a time you strongly disagreed with a 
product owner regarding technical debt. How did you handle it?

💭 Your answer: [Type your detailed answer here]
```

### Web Application

#### Starting the Application

**Method 1: Two Terminals**

```bash
# Terminal 1 - Backend
cd /root/panelpulse
python3 app.py

# Terminal 2 - Frontend
cd /root/panelpulse/frontend
npm run dev
```

**Method 2: Using tmux**

```bash
cd /root/panelpulse

# Start tmux session
tmux new -s panelpulse

# Split window (Ctrl+b then ")
python3 app.py

# Switch pane (Ctrl+b then arrow key)
cd frontend && npm run dev

# Detach: Ctrl+b then d
# Reattach: tmux attach -t panelpulse
```

#### Using the Web Interface

1. **Welcome Screen**: Click "Start Interview" button
2. **Setup Screen**: 
   - Enter your resume and job description
   - Or click "Load Example Data" for quick testing
3. **Interview Screen**: 
   - Answer 6 questions from the panel
   - See real-time progress
   - Get word count feedback
4. **Dashboard Screen**: 
   - View your overall score
   - See strengths and gaps
   - Download report as JSON
   - Restart for another practice

#### API Endpoints

**POST `/api/start-interview`**
```json
{
  "resume": "string",
  "job_description": "string"
}
```

**POST `/api/submit-answer`**
```json
{
  "session_id": "string",
  "answer": "string"
}
```

**GET `/api/example-data`**
Returns example resume and job description for testing.

## 📊 Dashboard & Feedback

### Dashboard Output

After completing all 6 questions, you receive a comprehensive feedback dashboard:

```json
{
  "overall_score": 75,
  "strengths": [
    "Strong technical vocabulary and specific examples",
    "Detailed and thorough responses",
    "Good use of metrics and measurable outcomes"
  ],
  "critical_gaps": [
    {
      "topic": "System Design/Architecture",
      "panelist_flagged": "system-architect",
      "what_went_wrong": "Responses lacked technical depth and specific technology choices",
      "how_to_fix": "Study distributed systems patterns, CAP theorem, and practice designing scalable architectures"
    }
  ],
  "behavioral_feedback": "Good behavioral awareness, but some answers could benefit from more specific examples and metrics.",
  "hire_recommendation": true
}
```

### Scoring Algorithm

**Overall Score (0-100)** is calculated from:

- **Specificity (40%)**: Use of technical terms and concrete examples
- **Depth (30%)**: Average answer length and detail level
- **Completion (30%)**: Finishing all questions

**Hire Recommendation**: Score ≥ 70

### Visual Dashboard (Web Version)

- 📊 **Circular Score Chart**: Animated radial chart with color coding
- ✅ **Strengths Grid**: Visual list with checkmarks
- ⚠️ **Critical Gaps**: Expandable cards with detailed feedback
- 💬 **Behavioral Summary**: Overall soft skills assessment
- 📥 **Download Report**: Export as JSON

## 🎓 Tips for Success

### Behavioral Questions (Hiring Manager)

✅ **Do:**
- Use the STAR method (Situation, Task, Action, Result)
- Focus on YOUR specific role and contributions
- Include metrics and measurable outcomes
- Be specific about challenges and how you overcame them

❌ **Don't:**
- Use vague "we" statements without clarifying your part
- Give generic answers without concrete examples
- Skip the results/impact of your actions

### System Design Questions (System Architect)

✅ **Do:**
- Think about trade-offs (CAP theorem, consistency vs. availability)
- Mention specific technologies and why you chose them
- Consider scalability, fault tolerance, and monitoring
- Discuss failure modes and mitigation strategies

❌ **Don't:**
- Jump to solutions without understanding requirements
- Ignore non-functional requirements
- Forget about operational concerns

### Technical Questions (Senior Developer)

✅ **Do:**
- Provide step-by-step debugging methodology
- Reference specific tools and commands
- Explain your reasoning and decision-making process
- Mention best practices and design patterns

❌ **Don't:**
- Give one-word answers
- Skip the "why" behind your approach
- Ignore edge cases or error handling

## 🔧 Configuration

### Adjusting Interview Length

Edit `panelpulse.py`:

```python
@dataclass
class InterviewContext:
    max_questions_per_panelist: int = 2  # Change this
    max_total_questions: int = 6         # And this
```

### Customizing Questions

Edit question lists in agent classes:

```python
class HiringManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Hiring Manager", "hiring-manager")
        self.questions = [
            "Your custom question 1",
            "Your custom question 2",
            # Add more...
        ]
```

### Modifying Scoring Weights

Edit `HealthMonitorAgent.generate_dashboard()`:

```python
specificity_score = (specific_answers / total) * 50  # Increase weight
depth_score = min((avg_length / 50) * 25, 25)        # Decrease weight
completion_score = (completed / total) * 25          # Adjust
```

### Web UI Customization

**Colors** - Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
    }
  }
}
```

**Animations** - Edit `frontend/src/components/*.jsx`:
```javascript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
```

## 🐛 Troubleshooting

### CLI Issues

**Script exits immediately**
```bash
# Ensure you press Enter twice after pasting resume/job description
```

**Type checking errors**
```bash
# These are informational only, script will still run
```

### Web Application Issues

**Frontend won't start**
```bash
# Check Node.js version
node --version  # Need 16+

# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

**Backend won't start**
```bash
# Check Python version
python3 --version  # Need 3.7+

# Install dependencies
pip3 install Flask flask-cors
```

**API calls failing**
```bash
# Ensure backend is running on port 5000
curl http://localhost:5000/api/example-data

# Check CORS configuration in app.py
```

**Port already in use**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## 📁 Project Structure

```
panelpulse/
├── panelpulse.py              # CLI version (no AI)
├── panelpulse_ai.py           # AI-powered CLI version
├── app.py                     # Web backend
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── example_resume.txt         # Sample resume
├── example_job_description.txt # Sample job description
├── README.md                  # This file
├── ai_clients/                # Pluggable AI providers
│   ├── __init__.py
│   ├── base_client.py         # Abstract base class
│   ├── chatgpt_client.py      # OpenAI ChatGPT
│   ├── gemini_client.py       # Google Gemini
│   ├── mock_client.py         # No API needed
│   └── client_factory.py      # Provider factory
├── frontend/                  # React web application
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── services/api.js
│   │   └── components/
│   │       ├── WelcomeScreen.jsx
│   │       ├── SetupScreen.jsx
│   │       ├── InterviewScreen.jsx
│   │       └── DashboardScreen.jsx
│   └── dist/                  # Production build
├── static/                    # Static assets
└── templates/                 # HTML templates
```

## 🔒 Security & Privacy

### Data Handling

- ✅ **No persistence**: All data in memory only
- ✅ **No logging**: No files written to disk
- ✅ **No network**: Completely offline
- ✅ **No external APIs**: Self-contained system

## 🚀 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

### Serve with Flask

Update `app.py`:
```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend/dist', 'index.html')
```

### Deployment Options

- **Heroku**: Use Procfile with gunicorn
- **AWS**: EC2 + nginx or Elastic Beanstalk
- **Google Cloud**: App Engine or Cloud Run
- **Docker**: Multi-stage build with nginx

### Docker Example

```dockerfile
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=frontend /app/frontend/dist ./frontend/dist
COPY *.py ./
CMD ["python", "app.py"]
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Additional question banks for different roles
- [ ] Better scoring algorithms
- [ ] Video recording and analysis
- [ ] Multi-language support
- [ ] Historical performance tracking
- [ ] Export to PDF
- [ ] Mobile app version

## 📚 Technologies Used

### Backend
- **Python 3.7+**: Core language
- **Flask**: Web framework
- **Flask-CORS**: CORS support

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Recharts**: Charts
- **Lucide React**: Icons
- **Axios**: HTTP client

## 📄 License

This project is provided as-is for educational and practice purposes.

## 🙏 Acknowledgments

Built with ❤️ for job seekers preparing for technical interviews.

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue in the repository

---

**Good luck with your interview preparation! 🚀**