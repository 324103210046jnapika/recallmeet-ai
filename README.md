# RecallMeet AI

### AI Meeting Intelligence Agent with Persistent Memory

> **AI Agents That Learn Using Hindsight**

RecallMeet AI is an AI-powered meeting intelligence agent that remembers important information from previous client interactions and uses that experience to prepare users for future meetings.

Instead of treating every meeting as an isolated conversation, RecallMeet builds a continuous understanding of each client and turns previous meeting experience into actionable preparation for the next interaction.

---

## 💡 What is RecallMeet AI?

Imagine that you have several meetings with the same client.

During different meetings, the client may tell you:

- They prefer AWS deployment
- The project should be completed within six weeks
- RBAC is mandatory
- Security approval is required
- Some documents are still pending
- Certain commitments were made
- Some follow-up actions are still open

After several meetings, remembering all of this information becomes difficult.

RecallMeet AI solves this problem by allowing an AI agent to **learn from previous meeting experiences**.

Before the next meeting, the user can simply ask:

> **"Prepare me for my meeting with Acme Corp."**

RecallMeet retrieves relevant information from previous meetings, understands the current situation, and generates a focused meeting preparation brief.

### In simple words:

> **RecallMeet turns past meeting experience into useful preparation for the next meeting.**

---

## 🎯 Problem Statement

Client relationships often involve many conversations over time.

Important information can become scattered across:

- Meeting notes
- Previous decisions
- Client requirements
- Security concerns
- Commitments
- Follow-up actions
- Delivery timelines

Traditional meeting tools mainly focus on recording or summarizing individual meetings.

However, the next meeting often depends on what happened in previous meetings.

### The key problem

> **How can an AI agent remember previous experiences and use them intelligently during future interactions?**

RecallMeet AI addresses this problem using persistent memory and contextual reasoning.

---

## ✨ Features

- 🧠 **Persistent Client Memory** - Maintains important information from previous meetings
- 🔄 **RETAIN → RECALL → REFLECT** - Uses the core Hindsight memory workflow
- 📋 **AI Meeting Preparation** - Generates preparation briefs for upcoming meetings
- 🎯 **Client Intelligence** - Identifies priorities, decisions, commitments, and concerns
- ⚠️ **Open Action Tracking** - Surfaces unresolved issues and pending follow-ups
- 💬 **Talking Points** - Provides relevant discussion topics
- ❓ **Suggested Questions** - Generates questions based on previous interactions
- 📅 **Meeting Timeline** - Displays the history of client interactions
- 🔀 **Memory ON/OFF** - Allows comparison with and without accumulated memory
- 🔍 **Memory Sources** - Shows the memories used during preparation
- 📊 **Interactive Dashboard** - Provides an overview of meetings and client memory
- 🛡️ **Resilient Memory Architecture** - Supports local fallback memory for reliable development and demonstration
- 🧪 **Automated Backend Testing** - Includes Pytest-based tests

---

# 🧠 How Does RecallMeet Learn?

The main idea behind RecallMeet is the ability of an AI agent to learn from previous experiences.

The system follows a memory workflow inspired by Hindsight:

```text
Previous Meeting
       ↓
    RETAIN
       ↓
     MEMORY
       ↓
    RECALL
       ↓
Relevant Memories
       ↓
   REFLECT
       ↓
Contextual Understanding
       ↓
   PREPARE
       ↓
Meeting Preparation
```

The first three stages represent the memory workflow, while `PREPARE` is RecallMeet's application-level intelligence layer.

---

## 1️⃣ RETAIN - Remember the Experience

After a meeting, important information is retained as memory.

For example:

```text
Client: Acme Corp

AWS deployment is preferred.
Project target is six weeks.
RBAC is mandatory.
Security review is required.
Architecture proposal is expected.
```

### RETAIN means:

> **Store useful experience so that it can be used later.**

---

## 2️⃣ RECALL - Retrieve Relevant Experience

Before a future meeting, RecallMeet searches the accumulated memory for information related to the current context.

For example:

```text
User:
Prepare me for my meeting with Acme Corp.
```

The system can retrieve information related to:

- AWS
- Security
- RBAC
- Delivery timeline
- Previous commitments
- Open follow-ups
- Previous decisions

### RECALL means:

> **Retrieve the relevant information from previous experiences.**

---

## 3️⃣ REFLECT - Understand the Experience

Simply retrieving old information is not enough.

The system needs to understand what is important for the current situation.

For example:

```text
The main unresolved issue is security approval.

RBAC validation and final security documentation
are important follow-up items before sign-off.
```

### REFLECT means:

> **Reason about retrieved experiences and identify what matters now.**

---

## 4️⃣ PREPARE - Turn Experience into Action

RecallMeet converts the accumulated context into a useful meeting preparation brief.

The generated preparation can contain:

- Client priorities
- Open action items
- Previous commitments
- Unresolved concerns
- Risks
- Talking points
- Questions to ask
- Suggested agenda
- Recommended next steps

### PREPARE means:

> **Turn accumulated experience into actionable preparation for the next interaction.**

---

# 🏢 Demo Scenario - Acme Corp

RecallMeet includes a multi-meeting demonstration using a client called **Acme Corp**.

The demonstration shows how information accumulates across multiple interactions.

---

## 📅 Meeting 1 - System Planning & Security Sync

During the first meeting, the following information is captured.

### Client Requirements

- Analytics dashboard requirements discussed
- AWS deployment preferred
- Six-week delivery target
- Security requirements discussed
- RBAC is mandatory

### Decisions

- AWS selected as the preferred deployment platform
- Six-week delivery target
- RBAC required

### Concerns

- Security review
- RBAC requirements

### Commitments

- Architecture proposal
- Security plan

### Follow-ups

- Continue technical discussion
- Share security plan

---

## 📅 Meeting 2 - Security Sign-off Meeting

During the second interaction, additional information is captured.

### New Information

- Security architecture is a major blocker
- RBAC demonstration is required
- Final security documents are required
- Production approval depends on the security review

### Commitments

- Final RBAC demonstration
- Final security documentation

### Follow-ups

- Schedule security sign-off
- Send required documents

---

## 📅 Meeting 3 - Security Sign-off Planning

The third meeting provides the latest client context.

### Current Situation

- AWS remains the preferred deployment platform
- Six-week delivery target remains important
- Security approval is still pending
- RBAC remains mandatory
- Final security architecture is required
- Security documentation is required before sign-off

### Current Concerns

- Security approval
- Architecture review

### Open Actions

- Schedule security sign-off
- Share security documentation

---

# 📋 Preparing for the Next Meeting

After these meetings, the user can ask:

```text
Prepare me for my meeting with Acme Corp.
```

RecallMeet uses the accumulated client context and prepares the user for the upcoming interaction.

The resulting preparation can identify:

```text
CLIENT PRIORITIES
• AWS deployment
• Six-week delivery timeline
• Security approval
• RBAC validation

OPEN ACTIONS
• Complete security review
• Share security documentation
• Schedule security sign-off

CONCERNS
• Security approval
• Architecture review
• RBAC validation

TALKING POINTS
• Confirm AWS deployment plan
• Review security approval
• Discuss RBAC status
• Confirm delivery timeline

QUESTIONS
• Is the security review complete?
• Are the final security documents ready?
• Has the RBAC demonstration been completed?
• Is the sign-off meeting scheduled?
```

This demonstrates how information from multiple previous meetings can become useful context for a future meeting.

---

# 🔄 Memory ON vs Memory OFF

RecallMeet includes a **Memory ON/OFF** capability to demonstrate the impact of accumulated experience.

## 🔴 Memory OFF

When memory is disabled:

- Previous client memories are not used
- Preparation relies on the current context
- The agent does not use the accumulated meeting history

---

## 🟢 Memory ON

When memory is enabled, the agent can use relevant previous experiences such as:

- AWS preference
- Six-week timeline
- RBAC requirement
- Security concerns
- Previous commitments
- Open follow-ups
- Previous decisions

This demonstrates why persistent memory can make an AI agent more useful over time.

---

# 🔄 Complete RecallMeet Workflow

```text
┌──────────────────────────────┐
│       Previous Meetings      │
└──────────────┬───────────────┘
               │
               ▼
        ┌─────────────┐
        │   RETAIN    │
        │   Memory    │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   RECALL    │
        │  Relevant   │
        │  Memories   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   REFLECT   │
        │ Understand  │
        │   Context   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   PREPARE   │
        │  Meeting    │
        │    Brief    │
        └──────┬──────┘
               │
               ▼
┌──────────────────────────────┐
│     Better Prepared User     │
└──────────────────────────────┘
```

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │     React Frontend   │
                    │    Vite + Tailwind   │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │        Python        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Meeting Service   Memory Service   Preparation Service
              │                │                │
              │                ▼                │
              │        Hindsight SDK            │
              │                │                │
              │                ▼                │
              │        Memory Processing        │
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                     Meeting Intelligence
                               │
                               ▼
                    Preparation Brief
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **React** | Frontend user interface |
| **Vite** | Frontend development and build |
| **Tailwind CSS** | UI styling |
| **Lucide React** | Interface icons |
| **Python** | Backend development |
| **FastAPI** | REST API backend |
| **Pydantic** | Data validation |
| **Hindsight** | AI memory layer |
| **hindsight-client** | Hindsight Python SDK |
| **Pytest** | Automated backend testing |
| **Uvicorn** | Backend application server |
| **Git** | Version control |
| **GitHub** | Source code hosting |

---

# 📦 Installation

## Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- npm
- Git
- Hindsight API credentials

---

## 1. Clone the Repository

```bash
git clone https://github.com/324103210046jnapika/recallmeet-ai.git
cd recallmeet-ai
```

---

# ⚙️ Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

---

# 🔐 Environment Configuration

Create:

```text
backend/.env
```

using:

```text
backend/.env.example
```

Configure the required environment variables.

Example:

```env
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_api_key_here
HINDSIGHT_BANK_ID=recallmeet-demo
HINDSIGHT_TIMEOUT=15

HOST=0.0.0.0
PORT=8000

GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile

DATA_DIR=data
```

> **Important:** Never commit your real `.env` file or API keys to GitHub.

---

# 🚀 Start the Backend

From the project root:

```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
```

Create:

```text
frontend/.env
```

with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```powershell
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🚀 Quick Start

After starting both services:

### Backend

```text
http://127.0.0.1:8000
```

### Frontend

```text
http://localhost:5173
```

Then:

1. Open RecallMeet AI
2. Select **Acme Corp**
3. Review the meeting history
4. Review the client memory
5. Keep **Memory ON**
6. Click **Prepare for my next meeting**
7. Review the generated preparation
8. Review the memory sources
9. Toggle Memory OFF to compare the result

---

# 📖 Usage Guide

## Dashboard

The dashboard provides an overview of:

- Total meetings
- Clients
- Memory activity
- Recent interactions
- Client history

---

## Client Memory

Select a client such as:

```text
Acme Corp
```

The system displays the accumulated context from previous interactions.

---

## Memory Evolution

The interface provides a timeline showing how client information evolves across meetings.

This demonstrates that the agent is not simply processing one meeting at a time.

---

## Meeting Preparation

Click:

```text
Prepare for my next meeting
```

The system processes the relevant client context and generates a preparation brief.

---

## Preparation Brief

The preparation result can include:

- Executive summary
- Client priorities
- Commitments
- Open actions
- Concerns
- Talking points
- Questions
- Suggested agenda
- Next steps
- Memory sources

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Check application and memory service status |
| `GET` | `/api/meetings` | Retrieve recorded meetings |
| `GET` | `/api/meetings/{id}` | Retrieve a specific meeting |
| `POST` | `/api/meetings` | Record a new meeting |
| `POST` | `/api/meetings/prepare` | Prepare for an upcoming meeting |
| `POST` | `/api/meetings/seed` | Load demonstration meetings |
| `POST` | `/api/memory/recall` | Retrieve relevant memories |
| `GET` | `/api/clients` | Retrieve available clients |
| `GET` | `/api/clients/{client}` | Retrieve client information |

---

# 🧠 Hindsight Integration

RecallMeet is designed around Hindsight's persistent-memory architecture.

The backend integrates the Hindsight Python SDK and supports the following memory operations:

```text
RETAIN
   ↓
Store Experience

RECALL
   ↓
Retrieve Relevant Experience

REFLECT
   ↓
Reason About Experience
```

RecallMeet then adds its application-level intelligence:

```text
Hindsight Memory
       │
       ▼
RETAIN → RECALL → REFLECT
       │
       ▼
RecallMeet Intelligence
       │
       ▼
PREPARE
       │
       ▼
Meeting Preparation
```

This allows the memory layer and the meeting intelligence layer to work together.

---

# 🛡️ Resilient Memory Architecture

RecallMeet is designed to remain functional even when the external memory service is temporarily unavailable.

The application can use a local development memory fallback.

```text
                 RecallMeet
                      │
                      ▼
             Hindsight Service
                      │
               ┌──────┴──────┐
               │             │
          Available      Unavailable
               │             │
               ▼             ▼
        Hindsight Cloud   Local Memory
               │             │
               └──────┬──────┘
                      │
                      ▼
             Meeting Intelligence
                      │
                      ▼
              Preparation Brief
```

### Current Demonstration Note

The Hindsight Python SDK and Hindsight Cloud integration are configured and verified.

During the current demonstration environment, the Hindsight Cloud `retain` operation is limited by available account credits. Therefore, RecallMeet uses a resilient local fallback memory store so that the complete application workflow remains functional.

The fallback is intended for development and demonstration reliability.

---

# 📁 Project Structure

```text
recallmeet-ai/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   │   ├── meeting.py
│   │   │   ├── memory.py
│   │   │   ├── prepare.py
│   │   │   ├── client.py
│   │   │   └── insight.py
│   │   │
│   │   ├── services/
│   │   │   ├── hindsight_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── meeting_service.py
│   │   │   ├── insight_service.py
│   │   │   └── prep_service.py
│   │   │
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── meetings.py
│   │   │   ├── memory.py
│   │   │   ├── clients.py
│   │   │   └── insights.py
│   │   │
│   │   ├── utils/
│   │   │   └── logger.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_meetings.py
│   │   └── test_prep.py
│   │
│   ├── seed_data.py
│   ├── verify_api.py
│   ├── requirements.txt
│   └── .env.example
│
├── data/
│   └── meetings.json
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   ├── clients.js
│   │   │   ├── insights.js
│   │   │   ├── meetings.js
│   │   │   └── memory.js
│   │   │
│   │   ├── components/
│   │   │   └── MemoryStatusBadge.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

# 🧪 Testing

Run the backend test suite:

```bash
pytest backend/tests -q
```

The test suite covers:

- ✅ Health endpoint
- ✅ Meeting APIs
- ✅ Meeting preparation
- ✅ Core backend functionality
- ✅ Memory-related workflow

The project has also been validated with a successful frontend production build.

---

# 📊 Example Preparation Output

For an Acme Corp preparation request, RecallMeet can identify:

```text
CLIENT
Acme Corp

PRIORITIES
• AWS deployment
• Six-week delivery timeline
• Security approval
• RBAC

OPEN ACTIONS
• Complete security review
• Share security documentation
• Schedule security sign-off

CONCERNS
• Security approval
• Architecture review
• RBAC validation

COMMITMENTS
• Final architecture
• Security documentation
• RBAC demonstration

TALKING POINTS
• Confirm AWS deployment
• Review security status
• Discuss RBAC
• Confirm delivery timeline

QUESTIONS
• Is the security review complete?
• Are the final security documents ready?
• Has the RBAC demonstration been completed?
• Is the sign-off meeting scheduled?
```

---

# 🌍 Real-World Applications

RecallMeet's persistent-memory approach can be applied to many real-world scenarios.

### 👔 Sales

Remember client requirements, budgets, objections, and previous discussions.

### 🤝 Customer Success

Track customer concerns, commitments, unresolved issues, and product requirements.

### 💼 Consulting

Maintain long-term project and stakeholder context.

### 📊 Account Management

Understand client history across multiple interactions.

### 🧑‍💻 Technical Support

Remember previous incidents and troubleshooting steps.

### 📋 Project Management

Track decisions, deadlines, dependencies, and action items.

### 🏢 Business Development

Maintain context across long-term customer conversations.

---

# 🚀 Future Enhancements

- ☁️ Production Hindsight Cloud memory
- 🎙️ Automatic meeting transcription
- 📅 Calendar integration
- 📧 Email integration
- 🔗 CRM integration
- 🔐 Multi-user authentication
- 🧠 Automatic memory extraction from transcripts
- 📈 Advanced client intelligence analytics
- 👥 Team-wide shared memory
- 🧩 Memory confidence and source attribution
- 🔔 Intelligent follow-up reminders
- 🚀 Production deployment

---

# 📋 Project Validation

The current project has been validated through:

- ✅ Backend automated tests
- ✅ Frontend production build
- ✅ REST API verification
- ✅ Hindsight SDK integration verification
- ✅ Meeting creation and retrieval
- ✅ Multi-meeting Acme Corp demonstration
- ✅ Meeting preparation workflow
- ✅ Memory ON/OFF workflow
- ✅ Memory source display
- ✅ Local fallback memory workflow

---

# 👥 Team ByteBloom

### Team Members

- **Elaprolu Jnapika Chowdary**
- **Byrraju Jahnavi**
- **Miriyala Vishnu Vardhani Devi Miriyala**
- **Vamisetti Someswara Krishna Prasad**
- **CHOWTIPALLI G S P SURYA PRABHAS**

---

# 🔗 Project Links

### GitHub Repository

https://github.com/324103210046jnapika/recallmeet-ai

### Project Article

https://medium.com/@jnapika2cse1.gdg/recallmeet-ai-building-an-ai-meeting-agent-that-learns-from-experience-using-hindsight-8a935aa82cde

---

# 🏆 Hackathon

This project was built for the theme:

> **AI Agents That Learn Using Hindsight**

RecallMeet AI explores how persistent memory can allow AI agents to learn from previous experiences and use those experiences to make future interactions more useful.

---

# 💭 Core Idea

> **Meetings should not be isolated events.**

> **Every interaction can become useful experience for the next interaction.**

---

# 📜 License

This project is developed for educational, hackathon, and portfolio purposes.

---

# ⭐ Support

If you find RecallMeet AI interesting, consider giving the repository a ⭐ on GitHub.
