/**
 * Orchestrate API Service
 * Wrapper for calling Orchestrate API endpoints through backend
 */

const API_BASE_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/api/orchestrate`;

/**
 * Get all available agents from Orchestrate
 * @param {Object} options - Query options
 * @param {string} options.query - Search by name/description
 * @param {string} options.ids - Filter by specific agent IDs (comma-separated)
 * @param {string} options.names - Filter by agent names (comma-separated)
 * @param {number} options.limit - Pagination limit
 * @param {number} options.offset - Pagination offset
 * @param {string} options.sort - Sort order ('asc', 'desc', 'recent')
 * @returns {Promise<Object>} List of agents
 */
export async function getAgents(options = {}) {
  try {
    const params = new URLSearchParams();
    if (options.query) params.append('query', options.query);
    if (options.ids) params.append('ids', options.ids);
    if (options.names) params.append('names', options.names);
    if (options.limit) params.append('limit', options.limit);
    if (options.offset) params.append('offset', options.offset);
    if (options.sort) params.append('sort', options.sort);

    const url = `${API_BASE_URL}/agents${params.toString() ? '?' + params.toString() : ''}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch agents');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching agents:', error);
    throw error;
  }
}

/**
 * Get all message threads
 * @param {Object} options - Query options
 * @param {string} options.agent_id - Filter by agent ID
 * @param {number} options.limit - Pagination limit
 * @param {number} options.offset - Pagination offset
 * @returns {Promise<Object>} List of threads
 */
export async function getThreads(options = {}) {
  try {
    const params = new URLSearchParams();
    if (options.agent_id) params.append('agent_id', options.agent_id);
    if (options.limit) params.append('limit', options.limit);
    if (options.offset) params.append('offset', options.offset);

    const url = `${API_BASE_URL}/threads${params.toString() ? '?' + params.toString() : ''}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch threads');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching threads:', error);
    throw error;
  }
}

/**
 * Get specific thread by ID
 * @param {string} threadId - Thread ID
 * @returns {Promise<Object>} Thread details
 */
export async function getThread(threadId) {
  try {
    const response = await fetch(`${API_BASE_URL}/threads/${threadId}`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch thread');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching thread:', error);
    throw error;
  }
}

/**
 * Get messages in a thread
 * @param {string} threadId - Thread ID
 * @param {Object} options - Query options
 * @param {number} options.limit - Pagination limit
 * @param {number} options.offset - Pagination offset
 * @returns {Promise<Object>} List of messages
 */
export async function getThreadMessages(threadId, options = {}) {
  try {
    const params = new URLSearchParams();
    if (options.limit) params.append('limit', options.limit);
    if (options.offset) params.append('offset', options.offset);

    const url = `${API_BASE_URL}/threads/${threadId}/messages${params.toString() ? '?' + params.toString() : ''}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch messages');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching messages:', error);
    throw error;
  }
}

/**
 * Get specific message in a thread
 * @param {string} threadId - Thread ID
 * @param {string} messageId - Message ID
 * @returns {Promise<Object>} Message details
 */
export async function getMessage(threadId, messageId) {
  try {
    const response = await fetch(`${API_BASE_URL}/threads/${threadId}/messages/${messageId}`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch message');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching message:', error);
    throw error;
  }
}

/**
 * Get chat history for the current agent
 * Convenience method that fetches threads and their messages
 * @param {string} agentId - Filter by specific agent (optional)
 * @param {number} limit - Number of threads to fetch
 * @returns {Promise<Array>} Array of threads with messages
 */
export async function getChatHistory(agentId = null, limit = 20) {
  try {
    // Get threads
    const threadsResponse = await getThreads({
      agent_id: agentId,
      limit: limit
    });
    
    const threads = threadsResponse.threads || threadsResponse.data || [];
    
    // Fetch messages for each thread
    const threadsWithMessages = await Promise.all(
      threads.map(async (thread) => {
        try {
          const messagesResponse = await getThreadMessages(thread.id);
          return {
            ...thread,
            messages: messagesResponse.messages || messagesResponse.data || []
          };
        } catch (error) {
          console.error(`Error fetching messages for thread ${thread.id}:`, error);
          return {
            ...thread,
            messages: []
          };
        }
      })
    );
    
    return threadsWithMessages;
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw error;
  }
}

export default {
  getAgents,
  getThreads,
  getThread,
  getThreadMessages,
  getMessage,
  getChatHistory
};
