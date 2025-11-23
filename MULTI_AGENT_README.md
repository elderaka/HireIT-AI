# Multi-Agent Chat System

## Overview

This is a scalable multi-agent chat system built with watsonx Orchestrate REST APIs, Vue.js, and Express.js. It allows seamless switching between different AI agents while maintaining conversation context.

## Architecture

### Backend (Express.js)
- **Multi-Agent Client** (`backend/multi-agent-client.js`): Core logic for managing multiple agents and conversations
- **REST API Endpoints** (`backend/index.js`): RESTful API for frontend communication
- **Agent Configuration** (`backend/agents-config.json`): Centralized agent definitions

### Frontend (Vue.js)
- **CustomChat Component** (`frontend/src/components/CustomChat.vue`): Main chat UI with agent switching
- **ChatPage** (`frontend/src/pages/ChatPage.vue`): Main page integrating chat with sidebars

## Features

✅ **Multi-Agent Support**: Switch between different specialized agents on the fly
✅ **Conversation Management**: Create, manage, and delete conversations
✅ **Agent Switching**: Change agents mid-conversation with context preservation
✅ **Real-time Messaging**: Async communication with watsonx Orchestrate
✅ **Scalable Architecture**: Easy to add new agents via configuration
✅ **Custom UI**: Full control over chat appearance and behavior

## API Endpoints

### Agents
- `GET /api/agents` - Get all available agents
- `GET /api/agents/:agentId` - Get specific agent config

### Conversations
- `POST /api/conversations` - Create new conversation with agent
  ```json
  { "agentId": "interviewer" }
  ```
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/:id` - Get conversation details
- `DELETE /api/conversations/:id` - Delete conversation

### Messages
- `POST /api/conversations/:id/messages` - Send message
  ```json
  { "message": "Hello", "agentId": "optional-for-switch" }
  ```

### Agent Management
- `PUT /api/conversations/:id/agent` - Switch agent
  ```json
  { "agentId": "reviewer" }
  ```

## Available Agents

1. **Interviewer** 🎤
   - Specialized in conducting interviews
   - Scores candidates and generates summaries
   - Produces structured interview results

2. **Reviewer** 📋
   - Reviews and evaluates applications
   - Analyzes resumes and candidate profiles

3. **Job Listing** 📝
   - Generates professional job listings
   - Creates job descriptions from requirements

4. **Data Hub** 📊
   - Manages candidate data and analytics
   - Organizes recruitment information

## Adding New Agents

1. Add agent configuration to `backend/agents-config.json`:
```json
{
  "id": "new_agent",
  "name": "New Agent",
  "agentId": "watsonx-agent-id",
  "environmentId": "watsonx-env-id",
  "description": "Agent description",
  "icon": "🤖",
  "color": "#hexcolor"
}
```

2. Deploy the agent in watsonx Orchestrate
3. Restart backend server
4. Agent automatically appears in frontend dropdown

## Environment Variables

### Backend (.env)
```env
WATSONX_API_KEY=your_ibm_cloud_api_key
PORT=3001
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:3001
```

## Running the System

1. **Start Backend**:
```bash
cd backend
node index.js
```

2. **Start Frontend**:
```bash
cd frontend
npm run dev
```

3. **Access Application**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:3001

## Conversation Flow

1. Frontend loads available agents from `/api/agents`
2. User selects agent → Creates conversation via `/api/conversations`
3. User sends message → POST to `/api/conversations/:id/messages`
4. Backend routes to appropriate watsonx agent via REST API
5. Response stored in conversation history
6. User can switch agent mid-conversation without losing context

## Scalability Features

- **Stateless API**: Each request is independent
- **Agent Isolation**: Agents don't interfere with each other
- **Conversation Persistence**: In-memory storage (can be replaced with database)
- **Horizontal Scaling**: Backend can be scaled across multiple instances
- **Configuration-Driven**: New agents added without code changes

## Future Enhancements

- [ ] Database persistence for conversations
- [ ] User authentication and authorization
- [ ] Conversation history export
- [ ] Agent analytics and usage metrics
- [ ] WebSocket support for real-time updates
- [ ] Multi-user conversation support
- [ ] File upload and attachment support
- [ ] Agent performance monitoring

## Technical Stack

- **Backend**: Node.js, Express.js, node-fetch
- **Frontend**: Vue 3, Vite, Tailwind CSS
- **AI Platform**: IBM watsonx Orchestrate
- **Authentication**: IBM Cloud IAM
