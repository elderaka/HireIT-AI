const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

class WatsonxService {
  constructor() {
    this.baseUrl = API_BASE_URL;
    this.sessionId = null;
  }

  /**
   * Check watsonx connection health
   */
  async checkHealth() {
    try {
      const response = await fetch(`${this.baseUrl}/api/watsonx/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * Create a new chat session
   */
  async createSession() {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to create session');
      }

      const data = await response.json();
      this.sessionId = data.sessionId;
      return data.sessionId;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  }

  /**
   * Send a message to watsonx
   */
  async sendMessage(message, conversationId = null) {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message,
          conversationId: conversationId || this.sessionId
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Delete current session
   */
  async deleteSession(sessionId = null) {
    try {
      const id = sessionId || this.sessionId;
      if (!id) return;

      const response = await fetch(`${this.baseUrl}/api/chat/session/${id}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        this.sessionId = null;
      }

      return await response.json();
    } catch (error) {
      console.error('Error deleting session:', error);
      throw error;
    }
  }

  /**
   * Invoke a specific watsonx skill
   */
  async invokeSkill(skillName, parameters = {}) {
    try {
      const response = await fetch(`${this.baseUrl}/api/watsonx/skill`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          skillName,
          parameters
        })
      });

      if (!response.ok) {
        throw new Error('Failed to invoke skill');
      }

      return await response.json();
    } catch (error) {
      console.error('Error invoking skill:', error);
      throw error;
    }
  }

  /**
   * Generate job listing
   */
  async generateJobListing(intakeText) {
    try {
      const response = await fetch(`${this.baseUrl}/api/job-listing/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ intakeText })
      });

      if (!response.ok) {
        throw new Error('Failed to generate job listing');
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating job listing:', error);
      throw error;
    }
  }
}

export default new WatsonxService();
