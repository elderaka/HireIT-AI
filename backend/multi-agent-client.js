import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class MultiAgentClient {
  constructor() {
    this.apiKey = process.env.WATSONX_API_KEY;
    this.hostURL = 'https://us-south.watson-orchestrate.cloud.ibm.com';
    this.orchestrationID = '69234d49cb514b0b9cf983c7a47f2f14_ee108010-e155-409a-a2b5-2dfe15fb2376';
    this.crn = 'crn:v1:bluemix:public:watsonx-orchestrate:us-south:a/69234d49cb514b0b9cf983c7a47f2f14:ee108010-e155-409a-a2b5-2dfe15fb2376::';
    this.accessToken = null;
    this.tokenExpiry = null;
    
    // Load agent configurations
    const configPath = path.join(__dirname, 'agents-config.json');
    this.agentsConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    
    // Store active conversations per agent
    this.conversations = new Map(); // { conversationId: { agentId, messages, createdAt } }
  }

  /**
   * Get IBM Cloud IAM access token
   */
  async getAccessToken() {
    if (this.accessToken && this.tokenExpiry && Date.now() < this.tokenExpiry) {
      return this.accessToken;
    }

    try {
      const response = await fetch('https://iam.cloud.ibm.com/identity/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        },
        body: `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${this.apiKey}`
      });

      if (!response.ok) {
        throw new Error(`Failed to get IAM token: ${response.statusText}`);
      }

      const data = await response.json();
      this.accessToken = data.access_token;
      this.tokenExpiry = Date.now() + (data.expires_in - 300) * 1000;
      
      return this.accessToken;
    } catch (error) {
      console.error('Error getting IAM token:', error);
      throw error;
    }
  }

  /**
   * Get all available agents
   */
  getAgents() {
    return this.agentsConfig.agents;
  }

  /**
   * Get agent configuration by ID
   */
  getAgentConfig(agentId) {
    return this.agentsConfig.agents.find(a => a.id === agentId);
  }

  /**
   * Create a new conversation
   */
  async createConversation(agentId) {
    const agent = this.getAgentConfig(agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} not found`);
    }

    const conversationId = `${agentId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    this.conversations.set(conversationId, {
      agentId,
      agentName: agent.name,
      messages: [],
      createdAt: new Date().toISOString(),
      lastActivity: new Date().toISOString()
    });

    return {
      conversationId,
      agentId,
      agentName: agent.name,
      createdAt: this.conversations.get(conversationId).createdAt
    };
  }

  /**
   * Send message to specific agent
   */
  async sendMessage(conversationId, message, agentId) {
    try {
      const conversation = this.conversations.get(conversationId);
      if (!conversation) {
        throw new Error(`Conversation ${conversationId} not found`);
      }

      // If agentId provided and different, switch agent
      if (agentId && agentId !== conversation.agentId) {
        const newAgent = this.getAgentConfig(agentId);
        if (!newAgent) {
          throw new Error(`Agent ${agentId} not found`);
        }
        conversation.agentId = agentId;
        conversation.agentName = newAgent.name;
      }

      const agent = this.getAgentConfig(conversation.agentId);
      const token = await this.getAccessToken();

      // Add user message to history
      const userMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      };
      conversation.messages.push(userMessage);

      // Call watsonx Orchestrate REST API
      const apiUrl = `${this.hostURL}/v2/assistants/${agent.agentId}/message`;
      
      const payload = {
        input: {
          message_type: 'text',
          text: message
        },
        context: {
          global: {
            system: {
              user_id: conversationId
            }
          }
        }
      };

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Watsonx API error:', errorText);
        throw new Error(`Watsonx API error: ${response.status}`);
      }

      const data = await response.json();
      
      // Extract assistant response
      const assistantText = data.output?.generic?.[0]?.text || data.output?.text || 'No response';
      
      const assistantMessage = {
        role: 'assistant',
        content: assistantText,
        timestamp: new Date().toISOString(),
        agentId: conversation.agentId,
        agentName: agent.name
      };
      
      conversation.messages.push(assistantMessage);
      conversation.lastActivity = new Date().toISOString();

      return {
        conversationId,
        message: assistantMessage,
        agentId: conversation.agentId,
        agentName: agent.name
      };
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Get conversation history
   */
  getConversation(conversationId) {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }
    return conversation;
  }

  /**
   * List all conversations
   */
  listConversations() {
    return Array.from(this.conversations.entries()).map(([id, data]) => ({
      conversationId: id,
      agentId: data.agentId,
      agentName: data.agentName,
      messageCount: data.messages.length,
      createdAt: data.createdAt,
      lastActivity: data.lastActivity
    }));
  }

  /**
   * Delete conversation
   */
  deleteConversation(conversationId) {
    return this.conversations.delete(conversationId);
  }

  /**
   * Switch agent in existing conversation
   */
  async switchAgent(conversationId, newAgentId) {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }

    const newAgent = this.getAgentConfig(newAgentId);
    if (!newAgent) {
      throw new Error(`Agent ${newAgentId} not found`);
    }

    conversation.agentId = newAgentId;
    conversation.agentName = newAgent.name;

    // Add system message about agent switch
    conversation.messages.push({
      role: 'system',
      content: `Switched to ${newAgent.name}`,
      timestamp: new Date().toISOString()
    });

    return {
      conversationId,
      agentId: newAgentId,
      agentName: newAgent.name
    };
  }
}

export default new MultiAgentClient();
