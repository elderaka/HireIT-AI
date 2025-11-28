# HireIT AI – Structured Recruitment Autopilot

▶️ **Live Demo:** [hireit-ai.vercel.app](https://hireit-ai.vercel.app) – explore HireIT in your browser.

HireIT AI is an end-to-end recruitment autopilot built on **IBM watsonx Orchestrate**.  
It tackles the pain points of modern hiring—high volumes of CVs, fragmented tools, unstructured interviews and AI-assisted candidate cheating—by coordinating multiple specialized agents under a single orchestrator.  
The result is a **governed, scalable and transparent workflow** that automates repetitive tasks while keeping humans in full control of decisions.

## Table of contents

1. [Overview](#overview)  
2. [Key features](#key-features)  
3. [Architecture](#architecture)  
   - [Multi-agent structure](#multi-agent-structure)  
   - [Agent tool usage](#agent-tool-usage)  
4. [Why HireIT?](#why-hireit)  
5. [Installation](#installation)  
6. [Usage](#usage)  
7. [Contributing](#contributing)

---

## Overview

Recruiters today spend enormous time triaging applications, juggling multiple systems (email, sheets, folders, ATS) and manually managing interviews across tools that don’t talk to each other.  
This leads to slow hiring, inconsistent evaluations and burnout.

**HireIT AI** addresses these challenges by orchestrating the entire hiring pipeline with a suite of AI agents:

- **Automation where it counts** – repetitive setup, document creation and tracking are delegated to agents.  
- **Human oversight preserved** – HR still makes every meaningful hiring decision.  
- **Enterprise-ready orchestration** – powered by **IBM watsonx Orchestrate**, built for real workflows rather than one-off chat prompts.

Think of HireIT as a **world-class, structured hiring autopilot**: AI handles the work, humans stay in control.

---

## Key features

### 1. Job Listing Creation

HR defines a new role (e.g., “Backend Engineer”) in the HireIT UI.

The **Job Listing Agent** automatically:

- Creates a dedicated **Google Drive folder structure** for the role.  
- Generates a **structured Job Listing JSON** (title, responsibilities, requirements, location, etc.).  
- Sets up **CV** and **Transcript** subfolders.  
- Initializes an **Applicant Tracking Spreadsheet** pre-wired to track candidate status.

**Output:** a complete, ready-to-use workspace for the entire hiring process, with consistent structure every time.

---

### 2. CV Review

The **CV Reviewer Agent** and **Mass Review Agent** work together to process incoming applications.

They can:

- **Read ATS-formatted CVs** – reliably parse structured resumes.  
- Perform **requirements matching** – map experience, skills and education against the Job Listing JSON.  
- Score and categorize candidates (e.g., strong match / partial / weak).  
- Produce **shortlist summaries** for HR to review.

Instead of manually reading every CV, recruiters review ranked results with traceable reasoning.

---

### 3. Applicant Tracking Pipeline

The **Application Agent** maintains a **real-time view of the candidate pipeline**:

- Tracks **candidate identity and contact details**.  
- Updates **status across stages** (applied, shortlisted, interviewed, final, rejected, etc.).  
- Logs **interview schedules and outcomes**.  
- Automatically updates the **tracking spreadsheet** to reflect the latest state.

This gives HR end-to-end visibility into hiring progress without manually massaging spreadsheets.

---

### 4. Interview Transcription & Documentation

During live or recorded interviews, the **Interview Agent** and **Transcriber** handle documentation:

- **Transcribe conversations** in (near) real time.  
- Capture **interviewer questions** and **candidate responses**.  
- Generate **structured interview documentation** aligned with the job’s requirements.  
- Store transcripts in the **appropriate folder structure** created by the Job Listing Agent.  
- Enable **post-hoc review and comparison** of candidates based on actual conversation content.

Interviewers retain full control over questions and evaluation.  
AI simply removes note-taking overhead and ensures structured artifacts.

---

## Architecture

HireIT AI is built around a **true multi-agent architecture** coordinated by a central **Supervisor Agent** using **IBM watsonx Orchestrate**.

At a high level:

1. The **Supervisor Agent** receives high-level intents (e.g., “Create a Backend Engineer role”, “Review new CVs”, “Generate interview doc for candidate X”).  
2. It **delegates** to specialized agents based on the task.  
3. Each agent invokes the right tools (Drive, Sheets, email, transcription, etc.) and returns structured results.  
4. The Supervisor aggregates outcomes and exposes them through the frontend UI.

Orchestrate isn’t a side utility – it’s the **brain** that routes tasks, enforces order and glues agents together into a consistent, repeatable process.

### Multi-agent structure

Core agents (mapped to your watsonx Orchestrate agent YAMLs):

- **Supervisor Agent**  
  - Central coordinator and policy enforcer.  
  - Decides which agent to invoke, in what order and with what context.  

- **Job Listing Agent**  
  - Creates folder structures, job listing JSON and initial tracking assets.  

- **Application / Applicant Tracker Agent**  
  - Maintains the candidate pipeline, updates statuses, and ensures the spreadsheet reflects reality.  

- **CV Reviewer Agent / Mass Review Agent**  
  - Parses CVs, scores and ranks candidates against job requirements.  
  - Can batch-review many CVs in one go.  

- **Interview Agent**  
  - Orchestrates interview sessions, links transcripts to candidates and roles, and can trigger follow-up tasks.  

- **Transcriber Agent**  
  - Handles speech-to-text transcription and generates structured notes.  

- **Hiring Assistant Agent**  
  - Provides HR-friendly summaries across roles, candidates and stages.  
  - Helps HR compare candidates and surface priorities.

Each agent has **clear ownership**, making the system easier to reason about, audit and extend.

### Agent tool usage

Agents are not just chatting: they are **tool-using workers**.

Examples:

- **Job Listing Agent**  
  - Uses Drive APIs (via Orchestrate tools) to create folder hierarchies.  
  - Writes initial JSON configs and files into storage.

- **Application Agent**  
  - Uses Sheets/Docs tools to update structured tracking tables.  
  - Can send notifications or update status fields automatically.

- **CV Reviewer / Mass Review**  
  - Reads files from CV folders.  
  - Interprets content using LLMs and returns structured scoring metadata.

- **Interview Agent + Transcriber**  
  - Uses transcription tools to process audio/video.  
  - Stores transcripts and links them back to the right role + candidate.

Because all of this is orchestrated via **IBM watsonx Orchestrate**, you get:

- **Traceable flows** – who did what, when, and using which tool.  
- **Deterministic pipelines** – the same inputs produce consistent outputs.  
- **Composable extension points** – adding a new agent or step doesn’t require rewriting the world.

---

## Why HireIT?

There are many “AI hiring” tools. Most of them are:

- a single chatbot with a prompt, or  
- a thin UI over a generic LLM API.

HireIT AI is deliberately different:

- **Orchestrate-first design**  
  - IBM watsonx Orchestrate is the core engine, not a checkbox.  
  - The system is built as a *workflow* of agents and tools, not a monolithic prompt.

- **True multi-agent architecture**  
  - Multiple agents with distinct responsibilities and tool access.  
  - Delegation and composition through the Supervisor Agent.

- **Real-world workflow coverage**  
  - From job creation → CV review → pipeline tracking → interview documentation.  
  - Spaces, files and sheets are created and kept in sync automatically.

- **Governable and auditable**  
  - HR teams retain control; AI is the operator, not the decision maker.  
  - Each step can be inspected, repeated and improved.

- **Built to production patterns**  
  - Structured agent YAMLs, clear tool definitions, and a real frontend + backend.  
  - Not a slide-only concept: there’s a working deployment at  
    **[hireit-ai.vercel.app](https://hireit-ai.vercel.app)**.

In short: HireIT is designed to look and behave like the hiring autopilot you’d actually want to run in a serious HR environment.

---

## Installation

> The exact steps depend on your environment and secrets (IBM keys, API credentials, etc.).  
> Below is a high-level guide you can adapt.

### Prerequisites

- Python 3.10+ (for backend / orchestration helpers)  
- Node.js + npm (for frontend)  
- IBM watsonx Orchestrate account with access to:
  - Agents  
  - Tools / Connections (Drive, Sheets, mail, etc.)
- Configured credentials for any external services (Google Drive/Sheets, email provider, etc.)

### Clone the repository

```bash
git clone https://github.com/elderaka/HireIT-AI.git
cd HireIT-AI
```

### Backend setup

```bash
# Example – adjust to your actual backend folder structure
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scriptsctivate

# Install dependencies
pip install -r requirements.txt
```

Set environment variables (e.g. in `.env`):

- IBM watsonx Orchestrate credentials  
- Any Google / mail API keys you use  
- Config relevant to your deployment

Run the backend (example, adjust to your entrypoint):

```bash
uvicorn main:app --reload
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Then open the printed localhost URL in your browser.

For production, you can deploy the frontend to **Vercel** (as in the hackathon build) and the backend to your preferred host.

---

## Usage

1. Open the UI (local dev or: **[hireit-ai.vercel.app](https://hireit-ai.vercel.app)**).  
2. Create a new **job** by entering the role and requirements.  
3. Let HireIT:
   - generate the workspace (folders, sheets, JSON config),  
   - review incoming CVs,  
   - maintain the pipeline status.  
4. During interviews, use the interview/transcription agent to capture structured notes.  
5. Use summaries and tracking sheets to compare candidates and make the final hiring decision.

AI does the busywork. HR signs off.

---

## Contributing

Contributions, feedback and issue reports are welcome.

Some ideas:

- New agents (e.g., offer letter generation, onboarding tasks).  
- Additional tool integrations (Slack/Teams notifications, calendar sync).  
- Improved scoring strategies for CV review and interview evaluation.

Open an issue or submit a pull request on  
`https://github.com/elderaka/HireIT-AI`.

---

Smarter hiring begins with **structured automation**.  
HireIT AI shows how a serious, orchestrated, multi-agent system can turn chaotic recruiting into a controlled, world-class workflow.
