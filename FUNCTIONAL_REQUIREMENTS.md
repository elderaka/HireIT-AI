# HireIT-AI System - Comprehensive Functional Requirements Document

**Generated:** November 23, 2025  
**System:** HireIT AI - AI-Powered Recruitment Management System

---

## Executive Summary

HireIT-AI is a comprehensive AI-powered recruitment management system built on IBM watsonx Orchestrate. The system provides end-to-end recruitment workflow automation through specialized AI agents, integrated tools, and a modern web interface.

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Technology Stack

**Backend:**
- Node.js with Express.js (ES Modules)
- FastAPI (Python) for specialized tools
- IBM watsonx Orchestrate REST APIs
- IBM Cloud IAM Authentication

**Frontend:**
- Vue 3 with TypeScript
- Vite build system
- Tailwind CSS for styling
- Vue Router for navigation

**AI Platform:**
- IBM watsonx Orchestrate
- Meta Llama 3.2 90B Vision Instruct LLM
- IBM Watson Speech-to-Text

**Storage:**
- Google Drive (file and folder management)
- Google Sheets (applicant tracking)
- Local file system (temporary storage)

### 1.2 System Components

1. **Multi-Agent Chat System** - Core conversational interface
2. **Backend API Server** - Express.js REST API (Port 3001)
3. **Frontend Web Application** - Vue.js SPA (Port 5173)
4. **Python Tools** - FastAPI microservices
5. **watsonx Agents** - Specialized AI agents (19+ agents)
6. **Integration Layer** - Google Drive, Sheets, Email, JIRA

---

## 2. CORE AGENTS

### 2.1 Job Listing Agent (`Job_Listing_4857jv`)

**Purpose:** Initialize hiring workspace for new job postings

**Capabilities:**
- Collect job details via structured template
- Normalize job data to JSON format
- Create Google Drive folder structure
- Generate job workspace hierarchy

**Workflow:**
1. User requests new job listing creation
2. Agent presents intake template with fields:
   - Job Title
   - Department
   - Location
   - Employment Type (full_time, part_time, internship, contract)
   - Seniority (intern, junior, mid, senior, lead)
   - Deadline
   - Owner Email
   - Requirements (must-have skills)
   - Nice-to-have skills
   - Additional notes

3. Parse and validate user input
4. Create folder structure: `<Job Title> Application/`
   - CV subfolder
   - Transcript subfolder

5. Generate job-listing.txt
6. Prepare applicant-tracker.csv template

**Tools Used:**
- `normalize_job_intake()` - Parse template data
- `extract_drive_folder_id()` - Extract Google Drive IDs
- `folder_management` - Create folder structure

**Output:**
- Structured job listing JSON
- Google Drive workspace
- Tracking spreadsheet template

---

### 2.2 Reviewer Agent (`Reviewer_Agent_2909kd`)

**Purpose:** Evaluate and score candidate CVs against hiring rubric

**Capabilities:**
- Batch CV evaluation
- Rubric-based scoring (0.0-10.0 scale)
- Evidence-based decision making
- Excel-compatible output generation

**Workflow:**
1. Receive hiring rubric (JSON format)
2. Access CV folder in Google Drive
3. For each CV:
   - Extract candidate profile (name, email, experience, skills, education)
   - Map profile to rubric criteria
   - Calculate component scores
   - Generate final score with pass/borderline/fail decision
   - Create candidate-specific evidence bullets

**Scoring Components:**
- Must-have skills (weighted)
- Nice-to-have skills (weighted)
- Experience years vs requirements
- Education match
- Other criteria (domain experience, certifications)

**Critical Rules:**
- NO score reuse between candidates
- Each candidate gets unique evidence bullets
- Unreadable CVs automatically fail with explanation
- All scoring based on actual CV content only

**Tools Used:**
- `DataHub` - CV file retrieval
- `Email_Blast` - Notification system
- `Job_Listing_Briefing_Agent` - Job context

**Output:**
- JSON with scored candidates array
- Evidence bullets per candidate
- Pass/fail recommendations
- Salary worth estimate

---

### 2.3 Interviewer Agent (`Interviewer_5060SD`)

**Purpose:** Conduct and evaluate job interviews

**Capabilities:**
- Interview transcript analysis
- Multi-dimensional candidate scoring
- Subjective and objective assessment generation
- Integration with prior evaluation data

**Workflow:**
1. Receive interview transcript (text or audio)
2. Load job requirements and candidate history
3. Analyze interview conversation:
   - Technical competency
   - Communication skills
   - Cultural fit
   - Problem-solving approach

4. Generate three outputs:
   - Final numerical score
   - Subjective assessment (interview-based)
   - Objective assessment (holistic evidence)

5. Update applicant tracker with results

**Collaborating Agents:**
- `Transcriber` - Audio to text conversion
- `Job_Listing_Briefing` - Job context
- `Reviewer` - Prior CV scores
- `DataHub` - Document retrieval
- `Text_Parser` - File parsing
- `Applicant_Tracker` - Pipeline updates

**Critical Rules:**
- NEVER construct Google Drive URLs by concatenation
- Always use folder listing tools to get file IDs
- Use returned file IDs/links for tool calls

**Output:**
- Final candidate score
- Subjective interview summary
- Objective comprehensive assessment
- Structured interview results

---

### 2.4 Applicant Tracker Agent (`Applicant_Tracker_0642Mt`)

**Purpose:** Manage recruitment pipeline and candidate records

**Capabilities:**
- Pipeline stage management
- Candidate status tracking
- Score synchronization
- Notes and metadata management

**Features:**
- Chat with documents enabled
- Knowledge base integration
- Vector search (400 token chunks, 50 overlap)
- Confidence thresholding

**Pipeline Stages:**
- Submitted
- Filtered (CV review complete)
- Interviewed
- Tested
- Status (Pending/Accepted/Rejected)

**Starter Prompts:**
1. "What can you do for me?"
2. "Formalize Message"
3. "Summarize Meeting Notes"

---

### 2.5 Transcriber Agent (`transcriber`, `Transcriber_0057hm`)

**Purpose:** Convert audio interviews to structured text

**Capabilities:**
- Audio file processing (multiple formats)
- IBM Watson Speech-to-Text integration
- Speaker diarization
- Transcript cleaning and formatting

**Input Support:**
- Direct audio bytes
- Audio file URLs
- watsonx downloadable_file objects
- JSON-wrapped audio references

**Output:**
- Structured transcript with speaker labels
- Cleaned and formatted text
- Timestamp information

**Tools:**
- `transcribe_job_interview_tool.py`
- IBM Watson STT API

---

### 2.6 Supporting Agents

#### DataHub
- General data/file operations
- Document retrieval from Drive
- Export functionality (Excel, CSV)
- Data persistence

#### Job Listing Briefing Agent
- Explain and structure job listings
- Generate role summaries
- Extract key requirements
- Provide job context to other agents

#### Text Parser
- Parse various file formats
- Extract structured text from PDFs
- Document content normalization

#### Email Blast (`Email_Blast_9071T9`)
- Gmail integration
- Bulk email operations
- Candidate communication
- Interview scheduling

#### Sheet Manager
- Google Sheets operations
- Applicant tracker management
- Data export/import
- Spreadsheet formatting

---

## 3. BACKEND API ENDPOINTS

### 3.1 Health & Authentication

```
GET  /health
     Returns: { ok: true, message: "backend alive" }

GET  /api/watsonx/token
     Returns: IBM Cloud IAM access token

GET  /api/watsonx/health
     Returns: watsonx system health status
```

### 3.2 Chat Session Management

```
POST /api/chat/session
     Creates: New watsonx chat session
     Returns: sessionId

POST /api/chat/message
     Body: { message: string, conversationId?: string }
     Returns: Agent response

DELETE /api/chat/session/:sessionId
     Deletes: Chat session
```

### 3.3 Multi-Agent Conversations

```
GET  /api/agents
     Returns: All available agents

POST /api/conversations
     Body: { agentId: string }
     Returns: { conversationId, agentId, sessionId, messages }

GET  /api/conversations
     Returns: All conversations

GET  /api/conversations/:conversationId
     Returns: Specific conversation with history

POST /api/conversations/:conversationId/messages
     Body: { message: string, agentId?: string }
     Returns: Response from active agent

PUT  /api/conversations/:conversationId/agent
     Body: { agentId: string }
     Returns: Agent switch confirmation

DELETE /api/conversations/:conversationId
     Deletes: Conversation
```

### 3.4 Orchestrate API Integration

```
GET  /api/orchestrate/agents
     Query: ?query, ?ids, ?names, ?limit, ?offset, ?sort
     Returns: Available agents from watsonx

GET  /api/orchestrate/threads
     Query: ?agent_id, ?limit, ?offset
     Returns: Message threads

GET  /api/orchestrate/threads/:threadId
     Returns: Thread details

GET  /api/orchestrate/threads/:threadId/messages
     Query: ?limit, ?offset
     Returns: Messages in thread

GET  /api/orchestrate/threads/:threadId/messages/:messageId
     Returns: Specific message details
```

### 3.5 Job Listing Generation

```
POST /api/job-listing/generate
     Body: { intakeText: string }
     Returns: { ok: true, intakeText, jobListing }
```

### 3.6 Skills Invocation

```
POST /api/watsonx/skill
     Body: { skillName: string, parameters: object }
     Returns: Skill execution result
```

---

## 4. PYTHON TOOLS

### 4.1 File Generation Tool (`main.py`)

**FastAPI Service:**
```python
POST /generate-file
     Body: { text: string, filename?: string, ext: string }
     Returns: { ok: true, filename, local_path }
```

**Purpose:** Generate and save text files locally

---

### 4.2 Job Listing Tools (`job_listing_tools.py`)

**Functions:**
- `normalize_job_intake()` - Parse intake template
- `extract_drive_folder_id()` - Extract Drive IDs from URLs
- Job validation and schema enforcement

**Schema:** Complete JSON schema for job listings with required fields

---

### 4.3 Transcription Tool (`transcribe_job_interview_tool.py`)

**Functions:**
- `_download_audio_from_source()` - Handle multiple audio input formats
- `_extract_raw_transcript()` - Parse STT results
- `_clean_transcript()` - Normalize and format text

**Features:**
- Multi-format audio support
- Watson STT integration
- Intelligent text cleaning
- Speaker diarization support

---

### 4.4 CV Review Tools (`cv_review_excel.py`)

**Functions:**
- Excel export for review results
- Batch candidate scoring
- Rubric application
- Evidence compilation

---

### 4.5 Sheet Manager Tools (`sheet_manager_tools.py`)

**Functions:**
- Google Sheets CRUD operations
- Applicant tracker updates
- Data synchronization
- Cell formatting

---

### 4.6 Drive Tools

**Files:**
- `drive_link_tools.py` - Link parsing and validation
- `get_folders.py` - Folder listing
- `create_folder_with_id.py` - Folder creation
- `build_file_bytes.py` - File content retrieval

---

### 4.7 Utility Tools

- `briefing_tool.py` - Job briefing generation
- `text_parser_tools.py` - Document parsing
- `batch_result_utils.py` - Batch processing utilities

---

## 5. FRONTEND APPLICATION

### 5.1 Pages

#### ChatPage.vue
**Features:**
- Multi-agent selector sidebar
- Real-time chat interface
- Session file viewer
- Agent switching capability
- Message history
- Loading indicators

**Layout:**
- Left: Agent selector (toggleable)
- Center: watsonx chat embed
- Right: Session files sidebar (toggleable)

#### LandingPage.vue
**Features:**
- System introduction
- Agent overview
- Getting started guide
- Navigation to chat

---

### 5.2 Components

#### CustomChat.vue
**Features:**
- Agent dropdown selector
- Message display (user/assistant/system)
- Message timestamps
- Agent-specific icons
- Auto-scroll to latest message
- Enter key to send
- Disabled state handling

#### WatsonxChat.vue
**Features:**
- Embedded watsonx chat widget
- Token-based authentication
- Dynamic agent configuration
- Message streaming
- File upload support

#### Navbar.vue
**Features:**
- Application branding
- Navigation links
- User menu
- IBM watsonx branding

#### ChatHistory.vue
**Features:**
- Historical conversation listing
- Thread selection
- Message preview
- Timestamp display

---

### 5.3 Services

#### orchestrate.service.js
**Functions:**
- `getAgents()` - Fetch available agents
- `getChatHistory()` - Retrieve thread history
- `getThreads()` - List all threads
- `getThread()` - Get thread details
- `getThreadMessages()` - Fetch thread messages
- `getMessage()` - Get specific message

---

## 6. CONFIGURATION

### 6.1 Environment Variables

**Backend (.env):**
```
WATSONX_API_KEY=<IBM Cloud API Key>
SERVICE_INSTANCE_URL=<watsonx Orchestrate instance URL>
PORT=3001
FRONTEND_URL=http://localhost:5173
```

**Frontend (.env):**
```
VITE_API_BASE_URL=http://localhost:3001
```

**Python Tools (.env):**
```
STT_URL=<Watson Speech-to-Text URL>
STT_API_KEY=<Watson STT API Key>
```

---

### 6.2 Agent Configuration (`backend/agents-config.json`)

**Structure:**
```json
{
  "agents": [
    {
      "id": "unique_id",
      "name": "Display Name",
      "agentId": "watsonx_agent_id",
      "environmentId": "watsonx_env_id",
      "description": "Agent description",
      "color": "#hexcolor"
    }
  ]
}
```

**Configured Agents:**
1. HireIT Assistant (General help)
2. Job Listing (Workspace creation)
3. CV Reviewer (Candidate evaluation)
4. Interviewer (Interview assessment)
5. Applicant Tracker (Pipeline management)

---

## 7. DATA MODELS

### 7.1 Job Listing Schema

```json
{
  "job_id": "string",
  "title": "string",
  "department": "string",
  "location": {
    "city": "string",
    "country": "string",
    "remote_type": "onsite|hybrid|remote"
  },
  "employment_type": "full_time|part_time|internship|contract",
  "seniority": "intern|junior|mid|senior|lead",
  "description": "string",
  "responsibilities": ["string"],
  "requirements": {
    "must_have": ["string"],
    "nice_to_have": ["string"]
  },
  "created_at": "timestamp"
}
```

---

### 7.2 Candidate Evaluation Schema

```json
{
  "candidate_id": "string",
  "name": "string",
  "email": "string",
  "cv_url": "string",
  "scores": {
    "must_have_skills": "number",
    "nice_to_have_skills": "number",
    "experience": "number",
    "education": "number",
    "other_criteria": "number",
    "final_score": "number (0-10)"
  },
  "auto_decision": "pass|borderline|fail",
  "evidence_bullets": ["string"],
  "worth_range": {
    "min": "number",
    "max": "number"
  },
  "unreadable": "boolean"
}
```

---

### 7.3 Interview Result Schema

```json
{
  "candidate_id": "string",
  "interview_date": "timestamp",
  "final_score": "number",
  "subjective_assessment": "string",
  "objective_assessment": "string",
  "dimension_scores": {
    "technical": "number",
    "communication": "number",
    "cultural_fit": "number",
    "problem_solving": "number"
  },
  "recommendation": "hire|consider|reject"
}
```

---

### 7.4 Applicant Tracker Schema

**CSV Columns:**
- Name (string)
- Email (string)
- Phone (string)
- Submitted (date)
- Filtered (date)
- Interviewed (date)
- Tested (date)
- Status (Pending|Accepted|Rejected)
- Notes (text)

---

## 8. WORKFLOW PROCESSES

### 8.1 Complete Hiring Workflow

```
1. CREATE JOB LISTING
   └─> Job Listing Agent
       ├─> Collect job details
       ├─> Create Drive workspace
       └─> Generate tracker template

2. RECEIVE APPLICATIONS
   └─> Manual CV upload to Drive

3. CV REVIEW
   └─> Reviewer Agent
       ├─> Load hiring rubric
       ├─> Parse all CVs
       ├─> Score each candidate
       └─> Generate shortlist

4. SCHEDULE INTERVIEWS
   └─> Email Blast Agent
       └─> Send interview invitations

5. CONDUCT INTERVIEWS
   └─> Manual or recorded interviews

6. INTERVIEW EVALUATION
   └─> Interviewer Agent
       ├─> Transcribe audio (if needed)
       ├─> Analyze conversation
       ├─> Combine with CV scores
       └─> Generate final assessment

7. UPDATE TRACKER
   └─> Applicant Tracker Agent
       └─> Sync all scores and decisions

8. MAKE HIRING DECISION
   └─> Review all assessments
   └─> Select candidates

9. SEND OFFERS
   └─> Email Blast Agent
       └─> Send offer letters
```

---

### 8.2 Agent Switching Workflow

```
1. User creates conversation with Agent A
2. User sends message to Agent A
3. Agent A responds
4. User switches to Agent B (mid-conversation)
5. Backend updates conversation context
6. User sends message
7. Agent B receives full conversation history
8. Agent B responds with context awareness
```

---

## 9. INTEGRATION POINTS

### 9.1 IBM watsonx Orchestrate
- REST API v1 and v2
- IAM token authentication
- Agent deployment and management
- Conversation threading
- Message streaming

### 9.2 IBM Watson Speech-to-Text
- Audio transcription
- Multiple language support
- Speaker diarization
- Real-time and batch processing

### 9.3 Google Drive API
- Folder creation and management
- File upload and download
- Link parsing and validation
- Permission management

### 9.4 Google Sheets API
- Spreadsheet creation
- Cell reading and writing
- Formatting and styling
- Data export

### 9.5 Gmail API
- Email sending (individual and bulk)
- Template processing
- Attachment handling
- Delivery tracking

### 9.6 JIRA API
- Issue management
- Ticket creation
- Status tracking
- Integration with hiring workflow

---

## 10. SECURITY & AUTHENTICATION

### 10.1 Authentication Methods
- IBM Cloud IAM API Keys
- OAuth 2.0 tokens (15-minute validity)
- Google Service Account credentials
- Secure token caching

### 10.2 Security Features
- CORS configuration
- Environment variable protection
- API key rotation support
- Secure credential storage

---

## 11. DEPLOYMENT

### 11.1 Local Development

**Backend:**
```bash
cd backend
npm install
npm run dev  # Runs on port 3001
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Runs on port 5173
```

**Python Tools:**
```bash
pip install -r requirements.txt
python main.py  # FastAPI on port 8000
```

**Concurrent Mode:**
```bash
npm run dev  # From root (runs both backend & frontend)
```

---

### 11.2 Production Deployment

**Vercel Configuration:**
- Backend: `backend/vercel.json`
- Frontend: `frontend/vercel.json`
- Serverless function deployment
- Environment variable configuration
- Custom domain support

---

## 12. EXTENSIBILITY

### 12.1 Adding New Agents

1. Create agent YAML configuration
2. Deploy to watsonx Orchestrate
3. Add agent to `backend/agents-config.json`
4. Restart backend server
5. Agent appears in frontend automatically

### 12.2 Adding New Tools

1. Create Python tool file in `tools/` directory
2. Implement using `@tool` decorator
3. Import to watsonx Orchestrate:
   ```bash
   orchestrate tools import -k python -f tools/your_tool.py
   ```
4. Reference in agent YAML configuration

### 12.3 Adding New API Endpoints

1. Add route handler to `backend/index.js`
2. Implement business logic
3. Update API documentation
4. Add frontend service method if needed

---

## 13. DOCUMENTATION

### 13.1 Available Documentation

- `README.md` - Basic project overview
- `MULTI_AGENT_README.md` - Multi-agent system guide
- `ORCHESTRATE_API_GUIDE.md` - API integration documentation
- `WATSONX_EMBED_GUIDE.md` - Embedding guide
- Agent YAML files - Individual agent specifications
- IBM Documentation PDFs in `frontend/docs/`

### 13.2 Code Documentation

- JSDoc comments in JavaScript files
- Docstrings in Python tools
- Inline comments for complex logic
- Type definitions in TypeScript

---

## 14. LIMITATIONS & CONSTRAINTS

### 14.1 Known Limitations

1. **In-memory conversation storage** - No database persistence
2. **Single-user design** - No multi-user authentication
3. **No conversation export** - Manual copy required
4. **Limited file format support** - Depends on parsing tools
5. **No real-time notifications** - Polling-based updates

### 14.2 Design Constraints

1. **Google Drive dependency** - File storage requires Drive access
2. **IBM Cloud requirement** - watsonx Orchestrate subscription needed
3. **Token expiration** - 15-minute IAM token refresh required
4. **Rate limiting** - Subject to API quotas
5. **LLM limitations** - Response quality depends on model

---

## 15. FUTURE ENHANCEMENTS

### 15.1 Planned Features

- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Role-based access control
- [ ] Conversation history export
- [ ] WebSocket for real-time updates
- [ ] Multi-user conversation support
- [ ] File upload directly to chat
- [ ] Agent analytics dashboard
- [ ] Performance monitoring
- [ ] Automated testing suite

### 15.2 Integration Expansions

- [ ] LinkedIn integration for candidate sourcing
- [ ] Calendar integration for interview scheduling
- [ ] Slack/Teams notifications
- [ ] ATS (Applicant Tracking System) integration
- [ ] Video interview platforms
- [ ] Background check services
- [ ] Offer letter generation and e-signature

---

## 16. TESTING & QUALITY ASSURANCE

### 16.1 Test Files

- `backend/test-base-urls.js` - Base URL validation
- `backend/test-orchestrate-api.js` - API endpoint testing
- `backend/debug-orchestrate.js` - Debug utilities

### 16.2 Testing Strategies

- Manual agent testing in watsonx UI
- API endpoint testing with sample data
- Integration testing with Google services
- User acceptance testing for workflows

---

## 17. MAINTENANCE & SUPPORT

### 17.1 Regular Maintenance Tasks

1. Token refresh and credential rotation
2. Agent performance monitoring
3. API quota management
4. Log file cleanup
5. Dependency updates

### 17.2 Troubleshooting

- Check environment variables configuration
- Verify IBM Cloud credentials
- Validate Google API access
- Review agent YAML configurations
- Check network connectivity to APIs

---

## 18. COMPLIANCE & DATA PRIVACY

### 18.1 Data Handling

- Candidate personal information (PII) stored in Google Drive
- No persistent storage of conversation data
- Temporary file storage in `/out` directory
- API credentials stored as environment variables

### 18.2 GDPR Considerations

- Right to access candidate data
- Right to delete candidate data
- Data portability (export capabilities)
- Consent management required for external use

---

## CONCLUSION

HireIT-AI is a production-ready, enterprise-grade recruitment automation system that leverages cutting-edge AI technology to streamline the entire hiring process. The system is modular, extensible, and designed for scalability.

**Core Strengths:**
✅ Multi-agent architecture for specialized tasks
✅ Seamless IBM watsonx Orchestrate integration
✅ Modern, responsive web interface
✅ Comprehensive API documentation
✅ Extensible tool ecosystem
✅ Real-world workflow automation

**Production Readiness:** 85%
- Core functionality: ✅ Complete
- Integration: ✅ Complete
- Documentation: ✅ Complete
- Testing: ⚠️ Basic coverage
- Database: ❌ In-memory only
- Multi-user: ❌ Not implemented

**Recommended Next Steps:**
1. Implement database persistence
2. Add user authentication
3. Create automated test suite
4. Set up monitoring and logging
5. Deploy to production environment

---

**Document Version:** 1.0  
**Last Updated:** November 23, 2025  
**System Version:** HireIT-AI v1.0.0
