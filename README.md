# RecallMeet AI

### AI Meeting Intelligence Agent with Persistent Memory

> **Hackathon Theme: AI Agents That Learn Using Hindsight**

RecallMeet AI is an AI-powered meeting intelligence agent that remembers important information from previous client interactions and uses that accumulated experience to prepare the user for future meetings.

Instead of treating every meeting as an isolated event, RecallMeet builds a continuous understanding of a client by connecting previous decisions, commitments, concerns, requirements, and follow-up actions.

---

## 🎯 Problem Statement

In long-term client relationships, important information is spread across many meetings.

For example, a client may mention:

- A preferred cloud platform
- A delivery deadline
- Security requirements
- Previous decisions
- Open concerns
- Promised deliverables
- Pending follow-up actions

When the next meeting happens, the user may need to manually search through old notes to remember the full context.

Traditional meeting tools usually focus on individual meeting summaries.

**RecallMeet AI focuses on the relationship across meetings.**

The goal is to answer:

> **How can an AI agent remember previous experiences and use them intelligently during future interactions?**

---

# 💡 What is RecallMeet AI?

RecallMeet AI is a meeting intelligence agent that combines:

1. Meeting history
2. Persistent memory
3. Relevant memory retrieval
4. Contextual reasoning
5. Actionable meeting preparation

A user can ask:

```text
Prepare me for my meeting with Acme Corp.
```

RecallMeet then uses the accumulated client context to produce a preparation brief containing relevant priorities, commitments, concerns, open actions, talking points, questions, and next steps.

### In one sentence

> **RecallMeet turns past meeting experience into useful preparation for the next meeting.**

---

# 🧠 How RecallMeet Learns

The project follows the Hindsight-inspired memory workflow:

```text
Previous Meeting
       │
       ▼
    RETAIN
       │
       ▼
 Persistent Memory
       │
       ▼
    RECALL
       │
       ▼
Relevant Memories
       │
       ▼
   REFLECT
       │
       ▼
Contextual Understanding
       │
       ▼
   PREPARE
       │
       ▼
Actionable Meeting Brief
```

### RETAIN

Important information from a meeting is converted into structured memory.

Example:

```text
Acme Corp prefers AWS.
The project target is six weeks.
RBAC is mandatory.
Security approval is required.
Architecture documentation is expected.
```

**RETAIN = remember useful experience.**

### RECALL

Before a future meeting, RecallMeet retrieves information relevant to the current client and meeting context.

**RECALL = find useful past experience.**

### REFLECT

Retrieved memories are interpreted in the context of the upcoming meeting.

For example:

```text
Security approval remains an important blocker.
RBAC validation and final security documentation
should be discussed before sign-off.
```

**REFLECT = understand what the retrieved experience means now.**

### PREPARE

RecallMeet converts the accumulated context into a practical meeting brief.

**PREPARE = turn experience into action.**

---

# 🏢 Demonstration Scenario: Acme Corp

The project includes a multi-meeting Acme Corp demonstration.

The purpose is to show that useful context accumulates across meetings.

---

## Meeting 1 — System Planning & Security Sync

### Discussed

- Analytics dashboard requirements
- AWS deployment
- Six-week delivery target
- Security requirements
- RBAC requirements

### Decisions

- AWS preferred
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

## Meeting 2 — Security Sign-off Meeting

### New Information

- Security architecture became a major blocker
- RBAC demonstration was required
- Final security documents were required
- Production approval depended on the security review

### Commitments

- Final RBAC demonstration
- Final security documentation

### Follow-ups

- Schedule security sign-off
- Send required documents

---

## Meeting 3 — Security Sign-off Planning

### Current Context

- AWS remains preferred
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

The user can now ask:

```text
Prepare me for my meeting with Acme Corp.
```

RecallMeet retrieves the accumulated context and produces a structured preparation brief.

A typical preparation can contain:

### Client Priorities

- AWS deployment
- Six-week delivery timeline
- Security approval
- RBAC validation

### Open Actions

- Complete security review
- Share security documentation
- Schedule security sign-off

### Concerns

- Security approval
- Architecture review
- RBAC validation

### Commitments

- Final architecture
- Security documentation
- RBAC demonstration

### Talking Points

- Confirm AWS deployment plan
- Review security status
- Discuss RBAC
- Confirm delivery timeline

### Suggested Questions

- Is the security review complete?
- Are the final security documents ready?
- Has the RBAC demonstration been completed?
- Is the sign-off meeting scheduled?

---

# 🔀 Memory ON vs Memory OFF

RecallMeet provides a **Memory ON/OFF** comparison mode.

## Memory OFF

When memory is disabled:

- Previous memories are not used for the preparation request.
- The preparation uses the current meeting context only.
- Memory count is zero.
- This provides a baseline for comparison.

## Memory ON

When memory is enabled:

- Relevant previous meetings are recalled.
- Client priorities are carried forward.
- Previous decisions can be surfaced.
- Commitments can be identified.
- Unresolved concerns can be highlighted.
- Open follow-ups can be included.
- Memory sources can be displayed.

This demonstrates the practical value of persistent memory.

---

# 🏗️ System Architecture

```text
                    ┌────────────────────────┐
                    │     React Frontend     │
                    │   Vite + Tailwind CSS  │
                    └───────────┬────────────┘
                                │
                                │ REST API
                                ▼
                    ┌────────────────────────┐
                    │     FastAPI Backend    │
                    │         Python         │
                    └───────────┬────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       Meeting Service    Memory Service    Preparation Service
              │                 │                 │
              │                 ▼                 │
              │        Hindsight Python SDK       │
              │                 │                 │
              │                 ▼                 │
              │        Memory Operations          │
              │                                   │
              └─────────────────┬─────────────────┘
                                │
                                ▼
                     Meeting Intelligence
                                │
                                ▼
                       Preparation Brief
```

---

# 🔄 Application Workflow

```text
1. Record Meeting
        ↓
2. Extract Important Meeting Context
        ↓
3. RETAIN Experience
        ↓
4. Store/maintain Memory
        ↓
5. User Requests Meeting Preparation
        ↓
6. RECALL Relevant Memories
        ↓
7. REFLECT on Retrieved Context
        ↓
8. Generate Preparation Brief
        ↓
9. Display Memory Sources + Actionable Insights
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| React | Frontend application |
| Vite | Frontend development and build tool |
| Tailwind CSS | UI styling |
| Lucide React | Interface icons |
| Python | Backend development |
| FastAPI | REST API |
| Pydantic | Data validation |
| Hindsight | Memory architecture |
| hindsight-client | Official Hindsight Python SDK |
| Pytest | Backend testing |
| Uvicorn | Backend server |
| Git | Version control |
| GitHub | Source code hosting |

---

# 📁 Project Structure

```text
recallmeet-ai/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── models/
│   │   │
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
│   │   └── utils/
│   │       └── logger.py
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

# ⚙️ Installation

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- npm
- Git
- Hindsight API credentials for Cloud usage

---

# 1. Clone the Repository

```bash
git clone https://github.com/324103210046jnapika/recallmeet-ai.git
cd recallmeet-ai
```

---

# 2. Create Python Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

---

# 3. Configure Backend Environment

Create:

```text
backend/.env
```

using:

```text
backend/.env.example
```

Example configuration:

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

> **Security:** Never commit `backend/.env` or any API key to GitHub.

---

# 4. Start the Backend

From the project root:

```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 5. Start the Frontend

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

Start Vite:

```powershell
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🚀 Quick Demo

After starting both backend and frontend:

1. Open `http://localhost:5173`
2. Select **Acme Corp**
3. Review the meeting history
4. Review the Memory Evolution section
5. Keep **Memory ON**
6. Click **Prepare for your next meeting**
7. Review the generated preparation brief
8. Review the **Memory Sources**
9. Toggle **Memory OFF**
10. Run preparation again to compare the baseline

---

# 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Check application and memory status |
| GET | `/api/meetings` | List meetings |
| GET | `/api/meetings/{id}` | Get a specific meeting |
| POST | `/api/meetings` | Record a new meeting |
| POST | `/api/meetings/prepare` | Prepare for an upcoming meeting |
| POST | `/api/meetings/seed` | Load demonstration meeting data |
| POST | `/api/memory/recall` | Retrieve relevant memories |
| GET | `/api/clients` | List clients |
| GET | `/api/clients/{client}` | Get client information |
| GET | `/api/insights/{client}` | Get client relationship insights |

---

# 🧠 Hindsight Integration

RecallMeet uses the official `hindsight-client` Python SDK and is structured around the Hindsight memory operations:

```text
RETAIN
  ↓
Store experience

RECALL
  ↓
Retrieve relevant experience

REFLECT
  ↓
Reason over experience
```

RecallMeet adds the application-level meeting intelligence layer:

```text
Hindsight Memory
       │
       ▼
RETAIN → RECALL → REFLECT
       │
       ▼
Meeting Intelligence
       │
       ▼
PREPARE
       │
       ▼
Meeting Brief
```

The configured memory bank for the demonstration is:

```text
recallmeet-demo
```

---

# 🛡️ Resilient Memory Fallback

RecallMeet is designed so that the application can continue functioning during development when the external memory operation is unavailable.

The application supports:

```text
                 RecallMeet
                      │
                      ▼
             Hindsight Service
                      │
               ┌──────┴──────┐
               │             │
        Hindsight works   Fallback needed
               │             │
               ▼             ▼
        Hindsight path   Local memory path
               │             │
               └──────┬──────┘
                      │
                      ▼
             Meeting Preparation
```

### Current Hackathon Demonstration

The Hindsight SDK is configured and the Hindsight Cloud endpoint is reachable.

At the time of this submission, the Hindsight Cloud `retain` operation is blocked by insufficient account credits. Therefore, the running demonstration uses the project's resilient local fallback memory for the actual demo data.

This is intentionally documented rather than presenting the local demonstration memory as if it were currently being stored in Hindsight Cloud.

---

# 🧪 Testing

Run the backend tests:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -q
```

The current test suite covers:

- Health endpoint
- Meeting APIs
- Meeting preparation workflow

Validated result:

```text
6 passed
```

The frontend has also been validated with a successful Vite production build.

---

# 📊 Example Output

For the Acme Corp demonstration, RecallMeet can surface information such as:

```text
CLIENT
Acme Corp

PRIORITIES
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

COMMITMENTS
• Final architecture
• Security documentation
• RBAC demonstration

TALKING POINTS
• Confirm AWS deployment plan
• Review security status
• Discuss RBAC
• Confirm delivery timeline
```

---

# 🌍 Real-World Applications

## Sales

Remember customer requirements, budgets, objections, and previous discussions.

## Customer Success

Track customer concerns, commitments, unresolved issues, and product requirements.

## Consulting

Maintain long-term project and stakeholder context.

## Account Management

Understand client history across multiple interactions.

## Technical Support

Remember previous incidents and troubleshooting context.

## Project Management

Track decisions, deadlines, dependencies, and action items.

## Business Development

Maintain context across long-term customer conversations.

---

# 🚀 Future Enhancements

- Production Hindsight Cloud memory
- Automatic meeting transcription
- Calendar integration
- Email integration
- CRM integration
- Multi-user authentication
- Automatic memory extraction from transcripts
- Advanced client intelligence analytics
- Team-wide shared memory
- Memory confidence and source attribution
- Intelligent follow-up reminders
- Production deployment

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

### GitHub

https://github.com/324103210046jnapika/recallmeet-ai

### Project Article

https://medium.com/@jnapika2cse1.gdg/recallmeet-ai-building-an-ai-meeting-agent-that-learns-from-experience-using-hindsight-8a935aa82cde

---

# 🏆 Hackathon

Built for the hackathon theme:

> **AI Agents That Learn Using Hindsight**

The project explores how persistent memory can make AI agents more useful over time by allowing them to retain previous experiences, recall relevant information, reflect on context, and use that knowledge during future interactions.

---

# 💭 Core Idea

> **Meetings should not be isolated events.**

> **Every interaction can become useful experience for the next interaction.**

---

# 📜 License

This project was developed for educational, hackathon, and portfolio purposes.

---

# ⭐ Support

If you find RecallMeet AI useful or interesting, consider giving the repository a ⭐ on GitHub.
