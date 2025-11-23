import fetch from 'node-fetch';

class WatsonxOrchestrateClient {
  constructor() {
    this.apiKey = process.env.IBM_CLOUD_API_KEY;
    this.orchestrateUrl = process.env.WATSONX_ORCHESTRATE_URL;
    this.projectId = process.env.WATSONX_PROJECT_ID;
    this.spaceId = process.env.WATSONX_SPACE_ID;
    this.agentId = process.env.WATSONX_AGENT_ID;
    this.accessToken = null;
    this.tokenExpiry = null;
  }

  /**
   * Get IAM access token from IBM Cloud
   */
  async getAccessToken() {
    // Return cached token if still valid
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
        body: new URLSearchParams({
          grant_type: 'urn:ibm:params:oauth:grant-type:apikey',
          apikey: this.apiKey
        })
      });

      if (!response.ok) {
        throw new Error(`Failed to get access token: ${response.statusText}`);
      }

      const data = await response.json();
      this.accessToken = data.access_token;
      // Set expiry to 5 minutes before actual expiry
      this.tokenExpiry = Date.now() + (data.expires_in - 300) * 1000;
      
      return this.accessToken;
    } catch (error) {
      console.error('Error getting IBM Cloud access token:', error);
      throw error;
    }
  }

  /**
   * Send a message to watsonx Orchestrate agent
   */
  async sendMessage(message, conversationId = null) {
    try {
      const token = await this.getAccessToken();
      
      const payload = {
        input: {
          text: message
        },
        context: {
          global: {
            system: {
              turn_count: 1
            }
          }
        }
      };

      if (conversationId) {
        payload.context.conversation_id = conversationId;
      }

      if (this.projectId) {
        payload.project_id = this.projectId;
      }

      const response = await fetch(`${this.orchestrateUrl}/assistants/${this.agentId}/sessions`, {
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
        throw new Error(`Watsonx API error: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message to watsonx:', error);
      throw error;
    }
  }

  /**
   * Create a new session/conversation
   */
  async createSession() {
    try {
      const token = await this.getAccessToken();
      
      const response = await fetch(`${this.orchestrateUrl}/assistants/${this.agentId}/sessions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to create session: ${response.statusText}`);
      }

      const data = await response.json();
      return data.session_id;
    } catch (error) {
      console.error('Error creating watsonx session:', error);
      throw error;
    }
  }

  /**
   * Delete a session
   */
  async deleteSession(sessionId) {
    try {
      const token = await this.getAccessToken();
      
      const response = await fetch(`${this.orchestrateUrl}/assistants/${this.agentId}/sessions/${sessionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      return response.ok;
    } catch (error) {
      console.error('Error deleting watsonx session:', error);
      throw error;
    }
  }

  /**
   * Invoke a specific skill/action
   */
  async invokeSkill(skillName, parameters = {}) {
    try {
      const token = await this.getAccessToken();
      
      const payload = {
        skill_name: skillName,
        parameters: parameters,
        project_id: this.projectId
      };

      const response = await fetch(`${this.orchestrateUrl}/skills/invoke`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Failed to invoke skill: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error invoking watsonx skill:', error);
      throw error;
    }
  }

  /**
   * Health check - verify credentials and connectivity
   */
  async healthCheck() {
    try {
      const token = await this.getAccessToken();
      return {
        status: 'connected',
        hasToken: !!token,
        configuredAgentId: this.agentId,
        configuredProjectId: this.projectId
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message
      };
    }
  }
}

// Export singleton instance
export default new WatsonxOrchestrateClient();
