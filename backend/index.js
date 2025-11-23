import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import watsonxClient from "./watsonx-client.js";
import multiAgentClient from "./multi-agent-client.js";

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from parent directory
dotenv.config({ path: path.join(__dirname, '..', '.env') });

const app = express();
app.use(cors({
  origin: process.env.FRONTEND_URL || '*',
  credentials: true
}));
app.use(express.json());

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ ok: true, message: "backend alive" });
});

// Get IBM Cloud IAM token
app.get("/api/watsonx/token", async (req, res) => {
  try {
    const apiKey = process.env.WATSONX_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: "API key not configured" });
    }

    const response = await fetch("https://iam.cloud.ibm.com/identity/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      },
      body: `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${apiKey}`
    });

    if (!response.ok) {
      throw new Error(`Failed to get IAM token: ${response.statusText}`);
    }

    const data = await response.json();
    res.json({ access_token: data.access_token, expires_in: data.expires_in });
  } catch (error) {
    console.error("Error fetching IAM token:", error);
    res.status(500).json({ error: error.message });
  }
});

// Watsonx health check
app.get("/api/watsonx/health", async (req, res) => {
  try {
    const health = await watsonxClient.healthCheck();
    res.json(health);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create a new chat session
app.post("/api/chat/session", async (req, res) => {
  try {
    const sessionId = await watsonxClient.createSession();
    res.json({ sessionId });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Send a message to watsonx
app.post("/api/chat/message", async (req, res) => {
  try {
    const { message, conversationId } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    const response = await watsonxClient.sendMessage(message, conversationId);
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete a chat session
app.delete("/api/chat/session/:sessionId", async (req, res) => {
  try {
    const { sessionId } = req.params;
    const success = await watsonxClient.deleteSession(sessionId);
    res.json({ success });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Invoke a specific skill
app.post("/api/watsonx/skill", async (req, res) => {
  try {
    const { skillName, parameters } = req.body;
    
    if (!skillName) {
      return res.status(400).json({ error: "Skill name is required" });
    }

    const response = await watsonxClient.invokeSkill(skillName, parameters);
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Job listing generation (existing endpoint with watsonx integration)
app.post("/api/job-listing/generate", async (req, res) => {
  try {
    const { intakeText } = req.body;
    
    if (!intakeText) {
      return res.status(400).json({ error: "Intake text is required" });
    }

    // Call watsonx with job listing generation prompt
    const response = await watsonxClient.sendMessage(
      `Generate a professional job listing based on the following intake information: ${intakeText}`
    );
    
    res.json({ 
      ok: true, 
      intakeText,
      jobListing: response 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ========== MULTI-AGENT CHAT ENDPOINTS ==========

// Get all available agents
app.get("/api/agents", (req, res) => {
  try {
    const agents = multiAgentClient.getAgents();
    res.json({ agents });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create new conversation with specific agent
app.post("/api/conversations", async (req, res) => {
  try {
    const { agentId } = req.body;
    
    if (!agentId) {
      return res.status(400).json({ error: "Agent ID is required" });
    }

    const conversation = await multiAgentClient.createConversation(agentId);
    res.json(conversation);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all conversations
app.get("/api/conversations", (req, res) => {
  try {
    const conversations = multiAgentClient.listConversations();
    res.json({ conversations });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get specific conversation
app.get("/api/conversations/:conversationId", (req, res) => {
  try {
    const { conversationId } = req.params;
    const conversation = multiAgentClient.getConversation(conversationId);
    res.json(conversation);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

// Send message in conversation
app.post("/api/conversations/:conversationId/messages", async (req, res) => {
  try {
    const { conversationId } = req.params;
    const { message, agentId } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    const response = await multiAgentClient.sendMessage(conversationId, message, agentId);
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Switch agent in conversation
app.put("/api/conversations/:conversationId/agent", async (req, res) => {
  try {
    const { conversationId } = req.params;
    const { agentId } = req.body;
    
    if (!agentId) {
      return res.status(400).json({ error: "Agent ID is required" });
    }

    const result = await multiAgentClient.switchAgent(conversationId, agentId);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete conversation
app.delete("/api/conversations/:conversationId", (req, res) => {
  try {
    const { conversationId } = req.params;
    const success = multiAgentClient.deleteConversation(conversationId);
    res.json({ success });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ========== ORCHESTRATE API ENDPOINTS ==========

// Get IAM token for Orchestrate API calls
async function getOrchestrateToken() {
  const apiKey = process.env.WATSONX_API_KEY;
  if (!apiKey) {
    throw new Error("WATSONX_API_KEY not configured");
  }

  const response = await fetch("https://iam.cloud.ibm.com/identity/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    body: `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${apiKey}`
  });

  if (!response.ok) {
    throw new Error(`Failed to get IAM token: ${response.statusText}`);
  }

  const data = await response.json();
  return data.access_token;
}

// Get all available agents from Orchestrate
app.get("/api/orchestrate/agents", async (req, res) => {
  try {
    const token = await getOrchestrateToken();
    const serviceUrl = process.env.SERVICE_INSTANCE_URL;
    
    if (!serviceUrl) {
      return res.status(500).json({ error: "SERVICE_INSTANCE_URL not configured" });
    }

    const { query, ids, names, limit, offset, sort } = req.query;
    
    // Build query parameters
    const params = new URLSearchParams();
    if (query) params.append('query', query);
    if (ids) params.append('ids', ids);
    if (names) params.append('names', names);
    if (limit) params.append('limit', limit);
    if (offset) params.append('offset', offset);
    if (sort) params.append('sort', sort);

    // The SERVICE_INSTANCE_URL already includes the full path
    const url = `${serviceUrl}/v2/orchestrate/agents${params.toString() ? '?' + params.toString() : ''}`;
    
    console.log('Fetching agents from:', url);
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch agents: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching Orchestrate agents:", error);
    res.status(500).json({ error: error.message });
  }
});

// Get all message threads
app.get("/api/orchestrate/threads", async (req, res) => {
  try {
    const token = await getOrchestrateToken();
    const serviceUrl = process.env.SERVICE_INSTANCE_URL;
    
    if (!serviceUrl) {
      return res.status(500).json({ error: "SERVICE_INSTANCE_URL not configured" });
    }

    const { agent_id, limit, offset } = req.query;
    
    // Build query parameters
    const params = new URLSearchParams();
    if (agent_id) params.append('agent_id', agent_id);
    if (limit) params.append('limit', limit);
    if (offset) params.append('offset', offset);

    const url = `${serviceUrl}/v1/threads${params.toString() ? '?' + params.toString() : ''}`;
    
    console.log('Fetching threads from:', url);
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch threads: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching threads:", error);
    res.status(500).json({ error: error.message });
  }
});

// Get specific thread by ID
app.get("/api/orchestrate/threads/:threadId", async (req, res) => {
  try {
    const token = await getOrchestrateToken();
    const serviceUrl = process.env.SERVICE_INSTANCE_URL;
    const { threadId } = req.params;
    
    if (!serviceUrl) {
      return res.status(500).json({ error: "SERVICE_INSTANCE_URL not configured" });
    }

    const url = `${serviceUrl}/v1/threads/${threadId}`;
    
    console.log('Fetching thread from:', url);
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch thread: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching thread:", error);
    res.status(500).json({ error: error.message });
  }
});

// Get messages in a thread
app.get("/api/orchestrate/threads/:threadId/messages", async (req, res) => {
  try {
    const token = await getOrchestrateToken();
    const serviceUrl = process.env.SERVICE_INSTANCE_URL;
    const { threadId } = req.params;
    const { limit, offset } = req.query;
    
    if (!serviceUrl) {
      return res.status(500).json({ error: "SERVICE_INSTANCE_URL not configured" });
    }

    // Build query parameters
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit);
    if (offset) params.append('offset', offset);

    const url = `${serviceUrl}/v1/threads/${threadId}/messages${params.toString() ? '?' + params.toString() : ''}`;
    
    console.log('Fetching messages from:', url);
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch messages: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching messages:", error);
    res.status(500).json({ error: error.message });
  }
});

// Get specific message in a thread
app.get("/api/orchestrate/threads/:threadId/messages/:messageId", async (req, res) => {
  try {
    const token = await getOrchestrateToken();
    const serviceUrl = process.env.SERVICE_INSTANCE_URL;
    const { threadId, messageId } = req.params;
    
    if (!serviceUrl) {
      return res.status(500).json({ error: "SERVICE_INSTANCE_URL not configured" });
    }

    const url = `${serviceUrl}/v1/threads/${threadId}/messages/${messageId}`;
    
    console.log('Fetching message from:', url);
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch message: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching message:", error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log("Backend running on http://localhost:" + PORT);
  console.log("\nWatsonx Orchestrate Integration Ready!");
  console.log("Make sure to configure your .env file with IBM Cloud credentials.");
  console.log("\nAvailable Orchestrate API endpoints:");
  console.log("  GET  /api/orchestrate/agents - List all agents");
  console.log("  GET  /api/orchestrate/threads - List all threads");
  console.log("  GET  /api/orchestrate/threads/:threadId - Get thread details");
  console.log("  GET  /api/orchestrate/threads/:threadId/messages - List thread messages");
  console.log("  GET  /api/orchestrate/threads/:threadId/messages/:messageId - Get specific message");
});
