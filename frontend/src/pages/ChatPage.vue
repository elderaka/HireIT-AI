<template>
  <div class="h-screen w-full flex flex-col overflow-hidden font-ibm">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <div class="flex-1 flex items-stretch overflow-hidden min-h-0">
      <!-- History Panel -->
      <aside class="w-64 bg-white border-r border-neutral-300 flex flex-col">
        <div class="px-6 py-4 border-b border-neutral-300">
          <h2 class="text-lg font-bold text-slate-900">Chat History</h2>
          <p class="text-xs text-neutral-600 mt-1">
            Your conversation sessions
          </p>
        </div>

        <div class="flex-1 overflow-y-auto p-4">
          <!-- Agent Selector -->
          <div class="mb-4">
            <label class="text-xs font-bold text-slate-900 mb-2 block"
              >Select Agent</label
            >
            <div class="space-y-2">
              <div
                v-for="agent in agents"
                :key="agent.id"
                @click="switchToAgent(agent)"
                :class="[
                  'p-3 rounded-xl cursor-pointer transition-all border',
                  currentAgent?.id === agent.id
                    ? 'bg-sky-50 border-sky-300'
                    : 'bg-white border-neutral-200 hover:border-neutral-300',
                ]"
              >
                <div class="flex items-center gap-2">
                  <span class="text-2xl">{{ agent.icon }}</span>
                  <div class="flex-1 min-w-0">
                    <div class="font-bold text-xs text-slate-900 truncate">
                      {{ agent.name }}
                    </div>
                    <div
                      v-if="currentAgent?.id === agent.id"
                      class="text-xs text-green-600 font-bold"
                    >
                      ● Active
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Conversations -->
          <div>
            <label class="text-xs font-bold text-slate-900 mb-2 block"
              >Recent Chats</label
            >
            <div
              v-if="conversations.length === 0"
              class="text-xs text-neutral-500 text-center py-8"
            >
              <div class="text-3xl mb-2">💬</div>
              <p>Chat history will appear here</p>
            </div>
            <div v-else class="space-y-2">
              <div
                v-for="conv in conversations"
                :key="conv.id"
                class="p-2 rounded-lg bg-neutral-50 hover:bg-neutral-100 cursor-pointer transition-colors border border-neutral-200"
              >
                <div class="flex items-start gap-2">
                  <span class="text-lg">{{ conv.agentIcon }}</span>
                  <div class="flex-1 min-w-0">
                    <div class="text-xs font-semibold text-slate-900 truncate">
                      {{ conv.agentName }} - {{ conv.messageCount }} messages
                    </div>
                    <div class="text-xs text-neutral-500">
                      {{ formatTime(conv.createdAt) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-neutral-300 bg-neutral-100">
          <div class="text-xs text-neutral-600">
            <strong>Tip:</strong> Your current session is automatically saved
          </div>
        </div>
      </aside>

      <!-- Watsonx Chat Container -->
      <div id="watsonx-chat-root" class="flex-1 relative bg-white"></div>

      <!-- Right Sidebar -->
      <aside
        :class="[
          'bg-white border-l border-neutral-200 flex flex-col transition-all duration-300 ease-in-out relative',
          rightSidebarOpen ? 'w-64' : 'w-12',
        ]"
      >
        <button
          @click="rightSidebarOpen = !rightSidebarOpen"
          class="absolute -left-4 top-4 bg-white border border-neutral-300 rounded-full p-1 hover:bg-neutral-100 transition-colors z-10"
        >
          <svg
            :class="[
              'w-5 h-5 text-neutral-600 transition-transform duration-300',
              rightSidebarOpen && 'rotate-180',
            ]"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
              clip-rule="evenodd"
            />
          </svg>
        </button>

        <div
          v-show="rightSidebarOpen"
          class="flex flex-col h-full overflow-hidden"
        >
          <div
            class="px-6 py-3 border-t border-b border-neutral-400 text-slate-900 text-sm"
          >
            Applicant Tracker
          </div>
          <!-- Right sidebar content here -->
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import Navbar from "@/components/Navbar.vue";

const rightSidebarOpen = ref(true);
const agents = ref([]);
const currentAgent = ref(null);
const conversations = ref([]);
const currentConversationId = ref(null);
let watsonxInstance = null;

// Load conversations from backend
const loadConversations = async () => {
  try {
    const response = await fetch("http://localhost:3001/api/conversations");
    const data = await response.json();
    conversations.value = data.conversations;
  } catch (error) {
    console.error("Failed to load conversations:", error);
  }
};

// Create new conversation with backend
const createConversation = async (agentId, agentName, agentIcon) => {
  try {
    const response = await fetch("http://localhost:3001/api/conversations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ agentId }),
    });

    const data = await response.json();
    currentConversationId.value = data.conversationId;

    // Reload conversations list
    await loadConversations();

    return data.conversationId;
  } catch (error) {
    console.error("Failed to create conversation:", error);
    return null;
  }
};

// Format timestamp for display
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  // Less than 1 minute
  if (diff < 60000) return "Just now";

  // Less than 1 hour
  if (diff < 3600000) {
    const mins = Math.floor(diff / 60000);
    return `${mins}m ago`;
  }

  // Less than 1 day
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours}h ago`;
  }

  // Show date
  return date.toLocaleDateString();
};

// Fetch agents from backend
const loadAgents = async () => {
  try {
    const response = await fetch("http://localhost:3001/api/agents");
    const data = await response.json();
    agents.value = data.agents;

    // Auto-select first agent
    if (agents.value.length > 0) {
      switchToAgent(agents.value[0]);
    }
  } catch (error) {
    console.error("Failed to load agents:", error);
  }
};

// Initialize watsonx chat with specific agent
const initWatsonxChat = async (agent) => {
  // Wait for DOM to be ready
  await new Promise((resolve) => setTimeout(resolve, 100));

  const rootElement = document.getElementById("watsonx-chat-root");
  if (!rootElement) {
    console.error("Root element not found");
    return;
  }

  // Destroy existing instance if any
  if (watsonxInstance) {
    try {
      if (typeof watsonxInstance.destroy === "function") {
        watsonxInstance.destroy();
      }
      // Clear the root element
      rootElement.innerHTML = "";
    } catch (e) {
      console.log("Clearing previous instance:", e.message);
    }
  }

  // Configure for new agent - use custom mode with customElement
  window.wxOConfiguration = {
    orchestrationID:
      "69234d49cb514b0b9cf983c7a47f2f14_ee108010-e155-409a-a2b5-2dfe15fb2376",
    hostURL: "https://us-south.watson-orchestrate.cloud.ibm.com",
    crn: "crn:v1:bluemix:public:watsonx-orchestrate:us-south:a/69234d49cb514b0b9cf983c7a47f2f14:ee108010-e155-409a-a2b5-2dfe15fb2376::",
    deploymentPlatform: "ibmcloud",
    showLauncher: false,
    layout: {
      form: "custom",
      customElement: rootElement,
      showOrchestrateHeader: true,
    },
    header: {
      showResetButton: false,
      showAiDisclaimer: false,
    },
    chatOptions: {
      agentId: agent.agentId,
      agentEnvironmentId: agent.environmentId,
    },
    style: {
      headerColor: "#000000",
      userMessageBackgroundColor: "#e0e0e0",
      primaryColor: "#0f62fe",
      showBackgroundGradient: false,
    },
  };

  // Load/reload watsonx
  if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
    try {
      watsonxInstance = window.wxoLoader.init();
    } catch (e) {
      console.error("Error initializing wxoLoader:", e);
    }
  } else {
    // Load script if not already loaded
    const existingScript = document.querySelector(
      'script[src*="wxoLoader.js"]'
    );
    if (existingScript) {
      existingScript.remove();
    }

    const script = document.createElement("script");
    script.src =
      "https://us-south.watson-orchestrate.cloud.ibm.com/wxochat/wxoLoader.js?embed=true";
    script.onload = () => {
      if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
        try {
          watsonxInstance = window.wxoLoader.init();
        } catch (e) {
          console.error("Error initializing wxoLoader after load:", e);
        }
      }
    };
    script.onerror = () => {
      console.error("Failed to load wxoLoader script");
    };
    document.head.appendChild(script);
  }
};

// Switch to different agent
const switchToAgent = async (agent) => {
  if (currentAgent.value?.id === agent.id) {
    console.log("Agent already active");
    return;
  }

  currentAgent.value = agent;
  console.log("Switching to agent:", agent.name);

  // Create new conversation with backend
  await createConversation(agent.id, agent.name, agent.icon);

  await initWatsonxChat(agent);
};

onMounted(async () => {
  loadConversations();
  await loadAgents();
});

onBeforeUnmount(() => {
  if (watsonxInstance && watsonxInstance.destroy) {
    watsonxInstance.destroy();
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap");

/* Custom scrollbar for agent list */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f5f5f5;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #d0d0d0;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #b0b0b0;
}
</style>

<style>
/* Global overrides to prevent watsonx from affecting navbar and layout */
body.wxo-embed-body-temp {
  overflow: visible !important;
  position: static !important;
}

/* Ensure watsonx chat custom mode fills the container */
#watsonx-chat-root {
  position: relative;
  z-index: 1;
  overflow: hidden;
}

/* Prevent watsonx from affecting the page structure */
.min-h-screen {
  position: relative;
  z-index: auto;
}
</style>
