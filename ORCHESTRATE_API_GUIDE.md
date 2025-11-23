# Orchestrate API Integration Guide

This guide explains how to use the Orchestrate API endpoints to fetch chat history, threads, messages, and available agents.

## Base Configuration

Your instance URL is configured in `.env`:
```
SERVICE_INSTANCE_URL=https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376
```

## Available Backend API Endpoints

### 1. Get All Available Agents

**Endpoint:** `GET http://localhost:3001/api/orchestrate/agents`

**Query Parameters:**
- `query` - Search by agent name/description
- `ids` - Filter by specific agent IDs (comma-separated)
- `names` - Filter by agent names (comma-separated)
- `limit` - Pagination limit
- `offset` - Pagination offset
- `sort` - Sort order: `asc`, `desc`, or `recent`

**Example:**
```javascript
// Get all agents
fetch('http://localhost:3001/api/orchestrate/agents')
  .then(res => res.json())
  .then(data => console.log(data));

// Search for specific agents
fetch('http://localhost:3001/api/orchestrate/agents?query=interview&limit=10')
  .then(res => res.json())
  .then(data => console.log(data));
```

### 2. Get All Message Threads

**Endpoint:** `GET http://localhost:3001/api/orchestrate/threads`

**Query Parameters:**
- `agent_id` - Filter by specific agent ID
- `limit` - Pagination limit
- `offset` - Pagination offset

**Example:**
```javascript
// Get all threads
fetch('http://localhost:3001/api/orchestrate/threads')
  .then(res => res.json())
  .then(data => console.log(data));

// Get threads for specific agent
fetch('http://localhost:3001/api/orchestrate/threads?agent_id=abc123&limit=20')
  .then(res => res.json())
  .then(data => console.log(data));
```

### 3. Get Specific Thread

**Endpoint:** `GET http://localhost:3001/api/orchestrate/threads/:threadId`

**Example:**
```javascript
const threadId = 'thread_abc123';
fetch(`http://localhost:3001/api/orchestrate/threads/${threadId}`)
  .then(res => res.json())
  .then(data => console.log(data));
```

### 4. Get Messages in a Thread

**Endpoint:** `GET http://localhost:3001/api/orchestrate/threads/:threadId/messages`

**Query Parameters:**
- `limit` - Pagination limit
- `offset` - Pagination offset

**Example:**
```javascript
const threadId = 'thread_abc123';
fetch(`http://localhost:3001/api/orchestrate/threads/${threadId}/messages`)
  .then(res => res.json())
  .then(data => console.log(data));
```

### 5. Get Specific Message

**Endpoint:** `GET http://localhost:3001/api/orchestrate/threads/:threadId/messages/:messageId`

**Example:**
```javascript
const threadId = 'thread_abc123';
const messageId = 'msg_xyz789';
fetch(`http://localhost:3001/api/orchestrate/threads/${threadId}/messages/${messageId}`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Using the Frontend Service

The frontend service (`orchestrate.service.js`) provides convenient wrapper functions:

### Import the Service

```javascript
import orchestrateService from '@/services/orchestrate.service.js';
// OR
import { getAgents, getChatHistory, getThreads } from '@/services/orchestrate.service.js';
```

### Get Available Agents

```javascript
// Get all agents
const agents = await orchestrateService.getAgents();

// Search for agents
const searchResults = await orchestrateService.getAgents({
  query: 'interview',
  limit: 10
});

// Filter by specific names
const filteredAgents = await orchestrateService.getAgents({
  names: 'Interviewer,Job Listing',
  sort: 'recent'
});
```

### Get Chat History

```javascript
// Get all chat history
const history = await orchestrateService.getChatHistory();

// Get history for specific agent
const agentHistory = await orchestrateService.getChatHistory('agent_id_here', 20);

// Each thread includes messages
history.forEach(thread => {
  console.log('Thread ID:', thread.id);
  console.log('Messages:', thread.messages);
});
```

### Get Threads and Messages

```javascript
// Get all threads
const threads = await orchestrateService.getThreads();

// Get threads for specific agent
const agentThreads = await orchestrateService.getThreads({
  agent_id: 'abc123',
  limit: 10
});

// Get specific thread
const thread = await orchestrateService.getThread('thread_id_here');

// Get messages in a thread
const messages = await orchestrateService.getThreadMessages('thread_id_here');

// Get specific message
const message = await orchestrateService.getMessage('thread_id', 'message_id');
```

## Vue Component Example

### Using in ChatPage.vue

Add chat history functionality to your ChatPage:

```vue
<script setup>
import { ref, onMounted } from 'vue';
import { getAgents, getChatHistory } from '@/services/orchestrate.service.js';

const chatHistory = ref([]);
const orchestrateAgents = ref([]);

// Load agents from Orchestrate API
const loadOrchestrateAgents = async () => {
  try {
    const response = await getAgents({ sort: 'recent' });
    orchestrateAgents.value = response.agents || response.data || [];
    console.log('Loaded agents:', orchestrateAgents.value);
  } catch (error) {
    console.error('Failed to load Orchestrate agents:', error);
  }
};

// Load chat history
const loadChatHistory = async (agentId = null) => {
  try {
    const history = await getChatHistory(agentId, 20);
    chatHistory.value = history;
    console.log('Loaded chat history:', history);
  } catch (error) {
    console.error('Failed to load chat history:', error);
  }
};

// View chat history modal or panel
const showChatHistory = ref(false);

onMounted(async () => {
  await loadOrchestrateAgents();
  await loadChatHistory();
});
</script>
```

### Add a Chat History Button

```vue
<template>
  <div>
    <!-- Chat History Button -->
    <button
      @click="showChatHistory = true"
      class="px-4 py-2 bg-blue-600 text-white rounded-lg"
    >
      View Chat History
    </button>

    <!-- Chat History Modal/Panel -->
    <div v-if="showChatHistory" class="fixed inset-0 bg-black/50 z-50">
      <ChatHistory @close="showChatHistory = false" />
    </div>
  </div>
</template>
```

## Using the ChatHistory Component

Import and use the pre-built ChatHistory component:

```vue
<template>
  <div>
    <!-- Add to your sidebar or modal -->
    <ChatHistory />
  </div>
</template>

<script setup>
import ChatHistory from '@/components/ChatHistory.vue';
</script>
```

## Full API URLs

Based on your `.env` configuration, the full URLs are:

1. **Get Agents:**
   ```
   https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376/api/v2/orchestrate/agents
   ```

2. **Get Threads:**
   ```
   https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376/api/v1/threads
   ```

3. **Get Thread Messages:**
   ```
   https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376/api/v1/threads/{threadId}/messages
   ```

**Note:** All direct API calls require Bearer token authentication. Use the backend proxy endpoints instead to avoid exposing your API key.

## Authentication

The backend handles authentication automatically using your `WATSONX_API_KEY` from `.env`. The backend:

1. Fetches an IAM token from `https://iam.cloud.ibm.com/identity/token`
2. Uses the token as a Bearer token in the Authorization header
3. Proxies requests to Orchestrate API

You don't need to handle authentication in the frontend!

## Error Handling

All service functions throw errors that you should catch:

```javascript
try {
  const agents = await orchestrateService.getAgents();
  console.log('Success:', agents);
} catch (error) {
  console.error('Error:', error.message);
  // Show error to user
}
```

## Testing the APIs

### Using curl (PowerShell)

```powershell
# Get all agents
Invoke-RestMethod -Uri "http://localhost:3001/api/orchestrate/agents" -Method Get

# Get all threads
Invoke-RestMethod -Uri "http://localhost:3001/api/orchestrate/threads" -Method Get

# Get threads for specific agent
Invoke-RestMethod -Uri "http://localhost:3001/api/orchestrate/threads?agent_id=abc123" -Method Get
```

### Using Browser Console

```javascript
// Get agents
fetch('http://localhost:3001/api/orchestrate/agents')
  .then(r => r.json())
  .then(console.log);

// Get threads
fetch('http://localhost:3001/api/orchestrate/threads')
  .then(r => r.json())
  .then(console.log);
```

## Next Steps

1. **Start the backend:** `cd backend && npm start`
2. **Start the frontend:** `cd frontend && npm run dev`
3. **Test the endpoints** using browser console or Postman
4. **Integrate ChatHistory component** into your UI
5. **Customize** the styling and behavior as needed

## Troubleshooting

### "SERVICE_INSTANCE_URL not configured"
- Check your `.env` file has `SERVICE_INSTANCE_URL` set
- Restart the backend server after changing `.env`

### "Failed to get IAM token"
- Verify `WATSONX_API_KEY` is correct in `.env`
- Check IBM Cloud API key permissions

### "Failed to fetch agents/threads"
- Ensure your service instance URL is correct
- Check if you have access to the Orchestrate instance
- Verify the instance ID in the URL matches your account

### CORS errors
- Backend should handle CORS automatically
- Make sure backend is running on port 3001
- Check browser console for detailed error messages

## API Response Examples

### Agents Response
```json
{
  "agents": [
    {
      "id": "agent_123",
      "name": "Interviewer",
      "description": "Handles interview processes",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Threads Response
```json
{
  "threads": [
    {
      "id": "thread_abc123",
      "agent_id": "agent_123",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

### Messages Response
```json
{
  "messages": [
    {
      "id": "msg_xyz789",
      "thread_id": "thread_abc123",
      "role": "user",
      "content": "Hello, I need help with interviews",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg_xyz790",
      "thread_id": "thread_abc123",
      "role": "assistant",
      "content": "I can help you with that...",
      "created_at": "2024-01-15T10:31:00Z"
    }
  ]
}
```
