import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import watsonxClient from "./watsonx-client.js";
import multiAgentClient from "./multi-agent-client.js";

dotenv.config();

const app = express();
app.use(cors());
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

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log("Backend running on http://localhost:" + PORT);
  console.log("\nWatsonx Orchestrate Integration Ready!");
  console.log("Make sure to configure your .env file with IBM Cloud credentials.");
});
