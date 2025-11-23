<template>
  <div class="flex flex-col h-full bg-white">
    <!-- Agent Selector Header -->
    <div class="border-b border-neutral-300 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-2xl">{{ currentAgent?.icon }}</span>
          <div>
            <h2 class="text-lg font-bold text-slate-900">{{ currentAgent?.name || 'Select Agent' }}</h2>
            <p class="text-sm text-neutral-600">{{ currentAgent?.description }}</p>
          </div>
        </div>
        
        <!-- Agent Dropdown -->
        <div class="relative">
          <button 
            @click="showAgentDropdown = !showAgentDropdown"
            class="px-4 py-2 bg-sky-50/20 border border-neutral-300 rounded-2xl hover:bg-sky-50/30 transition-colors flex items-center gap-2"
          >
            <span>Switch Agent</span>
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
          
          <!-- Dropdown Menu -->
          <div v-show="showAgentDropdown" class="absolute right-0 mt-2 w-80 bg-white border border-neutral-300 rounded-2xl shadow-lg z-10">
            <div 
              v-for="agent in agents" 
              :key="agent.id"
              @click="switchAgent(agent.id)"
              class="px-4 py-3 hover:bg-neutral-100 cursor-pointer flex items-center gap-3 first:rounded-t-2xl last:rounded-b-2xl"
            >
              <span class="text-2xl">{{ agent.icon }}</span>
              <div class="flex-1">
                <div class="font-bold text-sm">{{ agent.name }}</div>
                <div class="text-xs text-neutral-600">{{ agent.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto px-6 py-4">
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center">
        <div class="text-6xl mb-4">{{ currentAgent?.icon || '💬' }}</div>
        <h3 class="text-2xl font-bold text-slate-900 mb-2">Start a conversation</h3>
        <p class="text-neutral-600 max-w-md">
          Ask {{ currentAgent?.name || 'the agent' }} anything. You can switch agents at any time to get specialized help.
        </p>
      </div>

      <div v-for="(msg, index) in messages" :key="index" class="mb-4">
        <!-- User Message -->
        <div v-if="msg.role === 'user'" class="flex justify-end">
          <div class="bg-sky-50/20 px-4 py-3 rounded-2xl max-w-[70%]">
            <p class="text-slate-900">{{ msg.content }}</p>
            <span class="text-xs text-neutral-600 mt-1 block">{{ formatTime(msg.timestamp) }}</span>
          </div>
        </div>

        <!-- Assistant Message -->
        <div v-else-if="msg.role === 'assistant'" class="flex justify-start">
          <div class="flex gap-3 max-w-[70%]">
            <div class="flex-shrink-0">
              <span class="text-2xl">{{ getAgentIcon(msg.agentId) }}</span>
            </div>
            <div>
              <div class="bg-neutral-100 px-4 py-3 rounded-2xl">
                <p class="text-slate-900 whitespace-pre-wrap">{{ msg.content }}</p>
              </div>
              <div class="flex items-center gap-2 mt-1">
                <span class="text-xs text-neutral-600">{{ msg.agentName }}</span>
                <span class="text-xs text-neutral-400">•</span>
                <span class="text-xs text-neutral-600">{{ formatTime(msg.timestamp) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- System Message -->
        <div v-else-if="msg.role === 'system'" class="flex justify-center">
          <div class="bg-neutral-200 px-3 py-1 rounded-full text-xs text-neutral-600">
            {{ msg.content }}
          </div>
        </div>
      </div>

      <!-- Loading Indicator -->
      <div v-if="isLoading" class="flex justify-start mb-4">
        <div class="flex gap-3 max-w-[70%]">
          <div class="flex-shrink-0">
            <span class="text-2xl">{{ currentAgent?.icon }}</span>
          </div>
          <div class="bg-neutral-100 px-4 py-3 rounded-2xl">
            <div class="flex gap-1">
              <div class="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
              <div class="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-neutral-300 px-6 py-4 bg-white">
      <div class="flex gap-3 items-end">
        <textarea
          v-model="inputMessage"
          @keydown.enter.prevent="handleEnter"
          placeholder="Type your message..."
          rows="1"
          class="flex-1 px-4 py-3 border border-neutral-300 rounded-2xl resize-none focus:outline-none focus:border-sky-50 transition-colors"
          :disabled="isLoading || !currentConversationId"
        ></textarea>
        <button
          @click="sendMessage"
          :disabled="!inputMessage.trim() || isLoading || !currentConversationId"
          class="px-6 py-3 bg-sky-50/20 text-slate-900 rounded-2xl font-bold hover:bg-sky-50/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>
      <p v-if="!currentConversationId" class="text-xs text-neutral-600 mt-2">Select an agent to start chatting</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue';

const API_BASE = 'http://localhost:3001/api';

// State
const agents = ref([]);
const currentAgentId = ref(null);
const currentConversationId = ref(null);
const messages = ref([]);
const inputMessage = ref('');
const isLoading = ref(false);
const showAgentDropdown = ref(false);
const messagesContainer = ref(null);

// Computed
const currentAgent = computed(() => {
  return agents.value.find(a => a.id === currentAgentId.value);
});

// Methods
const loadAgents = async () => {
  try {
    const response = await fetch(`${API_BASE}/agents`);
    const data = await response.json();
    agents.value = data.agents;
    
    // Auto-select first agent
    if (agents.value.length > 0 && !currentAgentId.value) {
      await createConversation(agents.value[0].id);
    }
  } catch (error) {
    console.error('Failed to load agents:', error);
  }
};

const createConversation = async (agentId) => {
  try {
    const response = await fetch(`${API_BASE}/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentId })
    });
    
    const data = await response.json();
    currentConversationId.value = data.conversationId;
    currentAgentId.value = agentId;
    messages.value = [];
  } catch (error) {
    console.error('Failed to create conversation:', error);
  }
};

const switchAgent = async (agentId) => {
  showAgentDropdown.value = false;
  
  if (agentId === currentAgentId.value) return;
  
  try {
    if (currentConversationId.value) {
      // Switch agent in existing conversation
      await fetch(`${API_BASE}/conversations/${currentConversationId.value}/agent`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agentId })
      });
      
      currentAgentId.value = agentId;
      
      // Reload conversation to get system message
      const response = await fetch(`${API_BASE}/conversations/${currentConversationId.value}`);
      const data = await response.json();
      messages.value = data.messages;
    } else {
      // Create new conversation with new agent
      await createConversation(agentId);
    }
  } catch (error) {
    console.error('Failed to switch agent:', error);
  }
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value || !currentConversationId.value) return;
  
  const messageText = inputMessage.value.trim();
  inputMessage.value = '';
  isLoading.value = true;
  
  try {
    const response = await fetch(`${API_BASE}/conversations/${currentConversationId.value}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: messageText })
    });
    
    if (!response.ok) {
      throw new Error('Failed to send message');
    }
    
    const data = await response.json();
    
    // Reload full conversation to get both user and assistant messages
    const convResponse = await fetch(`${API_BASE}/conversations/${currentConversationId.value}`);
    const convData = await convResponse.json();
    messages.value = convData.messages;
    
    await scrollToBottom();
  } catch (error) {
    console.error('Failed to send message:', error);
    inputMessage.value = messageText; // Restore message on error
  } finally {
    isLoading.value = false;
  }
};

const handleEnter = (e) => {
  if (e.shiftKey) {
    // Allow new line with Shift+Enter
    return;
  }
  sendMessage();
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
};

const getAgentIcon = (agentId) => {
  const agent = agents.value.find(a => a.id === agentId);
  return agent?.icon || '🤖';
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// Watchers
watch(messages, () => {
  scrollToBottom();
});

// Lifecycle
onMounted(() => {
  loadAgents();
});

// Close dropdown when clicking outside
const handleClickOutside = (e) => {
  if (!e.target.closest('.relative')) {
    showAgentDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap");

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f5f5f5;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #d0d0d0;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #b0b0b0;
}

textarea {
  font-family: 'IBM Plex Sans', sans-serif;
  min-height: 48px;
  max-height: 120px;
}
</style>
