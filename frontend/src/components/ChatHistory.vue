<template>
  <div class="chat-history-panel p-6 bg-white rounded-lg shadow-lg">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 mb-2">Chat History</h2>
      <p class="text-sm text-neutral-600">View your conversation history and messages</p>
    </div>

    <!-- Agent Filter -->
    <div class="mb-4">
      <label class="block text-sm font-semibold text-slate-900 mb-2">
        Filter by Agent
      </label>
      <select
        v-model="selectedAgentId"
        @change="loadHistory"
        class="w-full px-4 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      >
        <option value="">All Agents</option>
        <option v-for="agent in availableAgents" :key="agent.id" :value="agent.id">
          {{ agent.name }}
        </option>
      </select>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="text-sm text-neutral-600 mt-2">Loading chat history...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
      <p class="text-sm text-red-700">{{ error }}</p>
      <button
        @click="loadHistory"
        class="mt-2 text-sm text-red-600 hover:text-red-700 font-semibold"
      >
        Try Again
      </button>
    </div>

    <!-- Chat Threads -->
    <div v-else-if="threads.length > 0" class="space-y-4">
      <div
        v-for="thread in threads"
        :key="thread.id"
        class="border border-neutral-200 rounded-lg overflow-hidden hover:border-blue-300 transition-colors"
      >
        <!-- Thread Header -->
        <div
          @click="toggleThread(thread.id)"
          class="bg-neutral-50 px-4 py-3 cursor-pointer flex items-center justify-between hover:bg-neutral-100"
        >
          <div class="flex-1">
            <h3 class="font-semibold text-slate-900 text-sm">
              Thread #{{ thread.id.substring(0, 8) }}
            </h3>
            <p class="text-xs text-neutral-600 mt-1">
              {{ formatDate(thread.created_at) }} • {{ thread.messages?.length || 0 }} messages
            </p>
          </div>
          <svg
            :class="['w-5 h-5 text-neutral-600 transition-transform', expandedThreads.has(thread.id) ? 'rotate-180' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>

        <!-- Thread Messages -->
        <div v-if="expandedThreads.has(thread.id)" class="p-4 bg-white space-y-3">
          <div
            v-for="message in thread.messages"
            :key="message.id"
            :class="[
              'p-3 rounded-lg',
              message.role === 'user' ? 'bg-blue-50 ml-8' : 'bg-neutral-50 mr-8'
            ]"
          >
            <div class="flex items-center gap-2 mb-1">
              <span
                :class="[
                  'text-xs font-bold uppercase',
                  message.role === 'user' ? 'text-blue-700' : 'text-neutral-700'
                ]"
              >
                {{ message.role }}
              </span>
              <span class="text-xs text-neutral-500">
                {{ formatDate(message.created_at) }}
              </span>
            </div>
            <div class="text-sm text-slate-900">
              {{ getMessageContent(message) }}
            </div>
          </div>

          <div v-if="!thread.messages || thread.messages.length === 0" class="text-center py-4 text-neutral-500 text-sm">
            No messages in this thread
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <svg class="w-16 h-16 text-neutral-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
      <p class="text-neutral-600 font-semibold mb-2">No chat history found</p>
      <p class="text-sm text-neutral-500">Start a conversation to see your history here</p>
    </div>

    <!-- Refresh Button -->
    <div class="mt-6 text-center">
      <button
        @click="loadHistory"
        :disabled="loading"
        class="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-neutral-300 text-white rounded-lg font-semibold transition-colors"
      >
        {{ loading ? 'Loading...' : 'Refresh History' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getAgents, getChatHistory } from '@/services/orchestrate.service.js';

const threads = ref([]);
const availableAgents = ref([]);
const selectedAgentId = ref('');
const loading = ref(false);
const error = ref(null);
const expandedThreads = ref(new Set());

// Load available agents
const loadAgents = async () => {
  try {
    const response = await getAgents();
    availableAgents.value = response.agents || response.data || [];
  } catch (err) {
    console.error('Error loading agents:', err);
  }
};

// Load chat history
const loadHistory = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const history = await getChatHistory(selectedAgentId.value || null, 20);
    threads.value = history;
  } catch (err) {
    error.value = err.message || 'Failed to load chat history';
    console.error('Error loading chat history:', err);
  } finally {
    loading.value = false;
  }
};

// Toggle thread expansion
const toggleThread = (threadId) => {
  if (expandedThreads.value.has(threadId)) {
    expandedThreads.value.delete(threadId);
  } else {
    expandedThreads.value.add(threadId);
  }
  // Force reactivity update
  expandedThreads.value = new Set(expandedThreads.value);
};

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown date';
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Extract message content
const getMessageContent = (message) => {
  if (typeof message.content === 'string') {
    return message.content;
  }
  
  if (Array.isArray(message.content)) {
    return message.content.map(c => c.text || c.value || '').join(' ');
  }
  
  if (message.content?.text) {
    return message.content.text;
  }
  
  return 'No content';
};

onMounted(async () => {
  await loadAgents();
  await loadHistory();
});
</script>

<style scoped>
.chat-history-panel {
  max-width: 800px;
  margin: 0 auto;
}
</style>
