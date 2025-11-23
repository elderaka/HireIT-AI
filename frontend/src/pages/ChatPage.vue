<template>
  <div class="h-screen w-full flex flex-col overflow-hidden font-['IBM_Plex_Sans'] bg-gradient-to-br from-slate-50 to-neutral-100">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <div class="flex-1 flex items-stretch overflow-hidden min-h-0 relative">
      <!-- Agent Selector Sidebar -->
      <aside
        :class="[
          'w-64 bg-white border-r border-neutral-300 flex flex-col transition-all duration-300 ease-in-out fixed left-0 top-16 bottom-0 z-20',
          showAgentSidebar ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <div class="px-6 py-4 border-b border-neutral-300">
          <h2 class="text-lg font-semibold text-slate-900">Select Agent</h2>
          <p class="text-xs text-neutral-600 mt-1">
            Choose a specialist for your task
          </p>
        </div>

        <div class="flex-1 overflow-y-auto p-4">
          <div class="space-y-2">
            <div
              v-for="agent in agents"
              :key="agent.id"
              @click="switchToAgent(agent)"
              :class="[
                'p-3 rounded-xl cursor-pointer transition-all border',
                currentAgent?.id === agent.id
                  ? 'bg-sky-50 border-sky-300 shadow-sm'
                  : 'bg-white border-neutral-200 hover:border-sky-200 hover:shadow-sm',
              ]"
            >
              <div class="flex items-center gap-2">
                <div class="flex-1 min-w-0">
                  <div class="font-bold text-xs text-slate-900 truncate">
                    {{ agent.name }}
                  </div>
                  <div class="text-xs text-neutral-500 truncate mt-0.5">
                    {{ agent.description }}
                  </div>
                  <div
                    v-if="currentAgent?.id === agent.id"
                    class="text-xs text-green-600 font-bold mt-1"
                  >
                    ● Active
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-neutral-300 bg-neutral-50 flex items-center justify-between">
          <div class="text-xs text-neutral-600">
            <strong>Tip:</strong> Each agent has its own specialized workflow
          </div>
          <button
            @click="showAgentSidebar = false"
            class="text-neutral-500 hover:text-neutral-700"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </aside>

      <!-- Toggle Agent Sidebar Button -->
      <button
        @click="showAgentSidebar = true"
        :class="[
          'fixed left-4 top-20 bg-white border border-neutral-300 rounded-lg p-2 shadow-lg hover:shadow-xl transition-all z-10',
          showAgentSidebar ? 'opacity-0 pointer-events-none' : 'opacity-100'
        ]"
        title="Show agent selector"
      >
        <svg class="w-5 h-5 text-neutral-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      </button>

      <!-- Watsonx Chat Container -->
      <div 
        :key="chatKey" 
        id="watsonx-chat-root" 
        :class="[
          'flex-1 relative bg-white transition-all duration-300 ease-in-out',
          (showAgentSidebar ? 'ml-64' : 'ml-0') + ' ' + (showFilesSidebar ? 'mr-80' : 'mr-0')
        ]"
      ></div>

      <!-- Right Sidebar - Session Files -->
      <aside
        :class="[
          'w-80 bg-white border-l border-neutral-300 flex flex-col transition-all duration-300 ease-in-out fixed right-0 top-16 bottom-0 z-20',
          showFilesSidebar ? 'translate-x-0' : 'translate-x-full'
        ]"
      >
        <div class="px-6 py-4 border-b border-neutral-300 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-slate-900">Session Files</h2>
            <p class="text-xs text-neutral-600 mt-1">
              {{ sessionFiles.length }} file(s)
            </p>
          </div>
          <button
            @click="showFilesSidebar = false"
            class="text-neutral-500 hover:text-neutral-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-4">
          <div v-if="sessionFiles.length === 0" class="text-center py-8 text-neutral-500 text-sm">
            No files generated yet
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="file in sessionFiles"
              :key="file.id"
              class="p-3 bg-neutral-50 rounded-lg border border-neutral-200 hover:border-neutral-300 transition-colors"
            >
              <div class="flex items-start justify-between gap-2">
                <div class="flex-1 min-w-0">
                  <div class="font-semibold text-sm text-slate-900 truncate">
                    {{ file.name }}
                  </div>
                  <div class="text-xs text-neutral-500 mt-1">
                    {{ new Date(file.timestamp).toLocaleTimeString() }}
                  </div>
                </div>
                <div class="flex gap-1">
                  <button
                    @click="downloadFile(file)"
                    class="p-2 text-blue-600 hover:bg-blue-50 rounded transition-colors"
                    title="Download"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                  <button
                    @click="deleteFile(file.id)"
                    class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
                    title="Delete"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-neutral-300 bg-neutral-50">
          <div class="text-xs text-neutral-600">
            Files are cleared when session ends
          </div>
        </div>
      </aside>

      <!-- Toggle Files Sidebar Button -->
      <button
        @click="showFilesSidebar = true"
        :class="[
          'fixed right-4 top-20 bg-white border border-neutral-300 rounded-lg p-2 shadow-lg hover:shadow-xl transition-all z-10',
          showFilesSidebar ? 'opacity-0 pointer-events-none' : 'opacity-100'
        ]"
        title="Show session files"
      >
        <svg class="w-5 h-5 text-neutral-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </button>

      <!-- Auto-Redirect Notification -->
      <div
        v-if="showRedirectNotification"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm"
        @click="cancelRedirect"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl p-8 max-w-md mx-4 animate-scale-in"
          @click.stop
        >
          <div class="text-center">
            <h3 class="text-2xl font-bold text-slate-900 mb-2">
              Switching to {{ redirectTarget?.name }}
            </h3>
            <p class="text-neutral-600 mb-6">
              {{ redirectTarget?.description }}
            </p>
            
            <!-- Countdown Circle -->
            <div class="relative w-32 h-32 mx-auto mb-6">
              <svg class="w-full h-full transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="60"
                  stroke="#e5e7eb"
                  stroke-width="8"
                  fill="none"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="60"
                  stroke="#0f62fe"
                  stroke-width="8"
                  fill="none"
                  :stroke-dasharray="377"
                  :stroke-dashoffset="377 * (1 - redirectCountdown / 5)"
                  class="transition-all duration-1000 ease-linear"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-4xl font-bold text-slate-900">{{ redirectCountdown }}</span>
              </div>
            </div>

            <button
              @click="cancelRedirect"
              class="w-full px-6 py-3 bg-neutral-200 hover:bg-neutral-300 text-slate-900 rounded-xl font-semibold transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import Navbar from "@/components/Navbar.vue";

const agents = ref([]);
const currentAgent = ref(null);
const chatKey = ref(0);
let watsonxInstance = null;
let isSwitching = ref(false);

// Auto-redirect state
const showRedirectNotification = ref(false);
const redirectTarget = ref(null);
const redirectCountdown = ref(5);
let redirectTimer = null;
let countdownInterval = null;

// Agent recommendation keywords mapping
const agentKeywords = {
  Job_Listing_Briefing: ['create job', 'new job', 'job listing', 'job workspace', 'new position', 'setup job'],
  Interviewer_5060SD: ['interview', 'transcribe', 'evaluate candidate', 'analyze interview', 'interview recording'],
  Reviewer_Agent: ['review cv', 'review resume', 'screen candidate', 'evaluate resume', 'cv review'],
  Applicant_Tracker: ['update status', 'track candidate', 'manage pipeline', 'applicant status', 'candidate status'],
};

// Session files management
const sessionFiles = ref([]);
const showFilesSidebar = ref(true);
const showAgentSidebar = ref(true);
let currentMessageBuffer = '';
let isInCodeBlock = false;

// Load agents from backend
const loadAgents = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/api/agents`);
    const data = await response.json();
    agents.value = data.agents;
    
    // Auto-select first agent if available
    if (agents.value.length > 0 && !currentAgent.value) {
      await switchToAgent(agents.value[0]);
    }
  } catch (error) {
    console.error("Failed to load agents:", error);
  }
};

// Clean up current chat instance
const cleanupChat = async () => {
  if (watsonxInstance) {
    try {
      console.log("Cleaning up chat instance...");
      if (typeof watsonxInstance.destroy === "function") {
        watsonxInstance.destroy();
      }
      watsonxInstance = null;
    } catch (e) {
      console.warn("Error during cleanup:", e);
    }
  }

  // Clean up orphaned React roots
  const orphanedRoots = document.querySelectorAll('[id^="WACCRoot"]');
  if (orphanedRoots.length > 0) {
    console.log(`Hiding ${orphanedRoots.length} orphaned roots...`);
    orphanedRoots.forEach((root) => {
      root.style.display = 'none';
      setTimeout(() => {
        try {
          if (root.parentNode) root.parentNode.removeChild(root);
        } catch (e) {
          // Ignore
        }
      }, 1000);
    });
  }

  // Force Vue to remount container
  chatKey.value++;
  await nextTick();
  await new Promise((resolve) => setTimeout(resolve, 300));
};

// Initialize chat with specific agent
const initChatWithAgent = async (agent) => {
  console.log(`Initializing chat with ${agent.name}...`);
  
  await new Promise((resolve) => setTimeout(resolve, 200));

  const rootElement = document.getElementById("watsonx-chat-root");
  if (!rootElement) {
    console.error("Root element not found");
    return false;
  }

  // Clear root element
  rootElement.innerHTML = "";

  // Configure watsonx with selected agent
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
      headerColor: "#0f62fe",
      userMessageBackgroundColor: "#0f62fe",
      primaryColor: "#0f62fe",
      showBackgroundGradient: false,
    },
  };

  // Initialize wxoLoader
  if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
    try {
      watsonxInstance = window.wxoLoader.init();
      
      // Intercept agent responses
      if (watsonxInstance && watsonxInstance.on) {
        // Listen to all events
        watsonxInstance.on('receive', (event) => {
          console.log('Agent response received:', event);
          
          // Handle streaming message deltas
          if (event?.event === 'message.delta') {
            const textChunk = event?.data?.delta?.content?.[0]?.text || '';
            if (textChunk) {
              currentMessageBuffer += textChunk;
              
              // Detect code block markers
              if (textChunk.includes('```')) {
                isInCodeBlock = !isInCodeBlock;
              }
            }
          }
          
          // Handle message completion
          if (event?.event === 'message.completed' || event?.event === 'run.completed') {
            console.log('Message completed, extracting files...');
            extractJsonFromBuffer();
            currentMessageBuffer = '';
            isInCodeBlock = false;
          }
        });
        
        // Also try custom event if watsonx uses different event system
        if (typeof watsonxInstance.addEventListener === 'function') {
          watsonxInstance.addEventListener('message', (event) => {
            console.log('Message event:', event);
            if (event?.data?.text) {
              currentMessageBuffer += event.data.text;
            }
          });
        }
      }
      
      console.log(`${agent.name} initialized successfully`);
      return true;
    } catch (e) {
      console.error("Error initializing wxoLoader:", e);
      return false;
    }
  } else {
    // Load script if not already loaded
    const existingScript = document.querySelector('script[src*="wxoLoader.js"]');
    if (existingScript) existingScript.remove();

    const script = document.createElement("script");
    script.src =
      "https://us-south.watson-orchestrate.cloud.ibm.com/wxochat/wxoLoader.js?embed=true";
    
    return new Promise((resolve) => {
      script.onload = () => {
        if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
          try {
            watsonxInstance = window.wxoLoader.init();
            console.log(`${agent.name} initialized successfully`);
            resolve(true);
          } catch (e) {
            console.error("Error initializing wxoLoader:", e);
            resolve(false);
          }
        } else {
          resolve(false);
        }
      };
      script.onerror = () => {
        console.error("Failed to load wxoLoader script");
        resolve(false);
      };
      document.head.appendChild(script);
    });
  }
};

// Auto-redirect with countdown
const startAutoRedirect = (targetAgentId) => {
  const targetAgent = agents.value.find(a => a.id === targetAgentId);
  if (!targetAgent) return;

  redirectTarget.value = targetAgent;
  redirectCountdown.value = 5;
  showRedirectNotification.value = true;

  // Start countdown
  countdownInterval = setInterval(() => {
    redirectCountdown.value--;
    if (redirectCountdown.value <= 0) {
      clearInterval(countdownInterval);
      executeRedirect();
    }
  }, 1000);
};

const cancelRedirect = () => {
  if (redirectTimer) clearTimeout(redirectTimer);
  if (countdownInterval) clearInterval(countdownInterval);
  showRedirectNotification.value = false;
  redirectTarget.value = null;
  redirectCountdown.value = 5;
};

const executeRedirect = async () => {
  showRedirectNotification.value = false;
  if (redirectTarget.value) {
    await switchToAgent(redirectTarget.value);
  }
  redirectTarget.value = null;
};

// Extract JSON code blocks from message buffer
const extractJsonFromBuffer = () => {
  console.log('Extracting JSON from buffer, length:', currentMessageBuffer.length);
  const jsonBlockRegex = /```(?:json)?\s*({[\s\S]*?})\s*```/g;
  let match;
  let foundMatch = false;
  
  while ((match = jsonBlockRegex.exec(currentMessageBuffer)) !== null) {
    foundMatch = true;
    try {
      const jsonContent = match[1];
      console.log('Found JSON block:', jsonContent.substring(0, 100) + '...');
      const parsed = JSON.parse(jsonContent);
      
      // Create downloadable files for job listing
      if (parsed.job_title) {
        console.log('Creating files for job:', parsed.job_title);
        const timestamp = Date.now();
        
        // Check if files already exist to avoid duplicates
        const existingFile = sessionFiles.value.find(f => f.name === 'job-listing.txt' && f.content === jsonContent);
        if (existingFile) {
          console.log('Files already exist, skipping...');
          continue;
        }
        
        // Create job-listing.txt
        const txtBlob = new Blob([jsonContent], { type: 'text/plain' });
        const txtUrl = URL.createObjectURL(txtBlob);
        
        sessionFiles.value.push({
          id: timestamp,
          name: 'job-listing.txt',
          content: jsonContent,
          url: txtUrl,
          timestamp: new Date().toISOString(),
          type: 'json'
        });
        
        console.log('Created job-listing.txt');
        
        // Create applicant-tracker.csv
        const csvContent = 'Name,Email,Phone,Submitted,Filtered,Interviewed,Tested,Status,Notes\n';
        const csvBlob = new Blob([csvContent], { type: 'text/csv' });
        const csvUrl = URL.createObjectURL(csvBlob);
        
        sessionFiles.value.push({
          id: timestamp + 1,
          name: 'applicant-tracker.csv',
          content: csvContent,
          url: csvUrl,
          timestamp: new Date().toISOString(),
          type: 'csv'
        });
        
        console.log('Created applicant-tracker.csv');
        console.log('Total files now:', sessionFiles.value.length);
      }
    } catch (e) {
      console.error('Error parsing JSON:', e);
      // Not valid JSON, skip
    }
  }
  
  if (!foundMatch) {
    console.log('No JSON blocks found in buffer');
  }
};

// Download file
const downloadFile = (file) => {
  const a = document.createElement('a');
  a.href = file.url;
  a.download = file.name;
  a.click();
};

// Delete file
const deleteFile = (fileId) => {
  const fileIndex = sessionFiles.value.findIndex(f => f.id === fileId);
  if (fileIndex !== -1) {
    URL.revokeObjectURL(sessionFiles.value[fileIndex].url);
    sessionFiles.value.splice(fileIndex, 1);
  }
};

// Detect agent recommendation in HireIT messages
const detectAgentRecommendation = (message) => {
  if (currentAgent.value?.id !== 'HireIT_Agent') return;
  
  const lowerMessage = message.toLowerCase();
  
  // Check for each agent's keywords
  for (const [agentId, keywords] of Object.entries(agentKeywords)) {
    for (const keyword of keywords) {
      if (lowerMessage.includes(keyword)) {
        // User expressed intent to do something, trigger auto-redirect
        startAutoRedirect(agentId);
        return;
      }
    }
  }
};

// Listen to chat messages (you'll need to hook this into your chat events)
// This is a placeholder - you'll integrate with wxoLoader events
const setupChatListener = () => {
  if (watsonxInstance && watsonxInstance.on) {
    watsonxInstance.on('send', (event) => {
      if (event?.message?.content) {
        detectAgentRecommendation(event.message.content);
      }
    });
  }
};

// Switch to a different agent
const switchToAgent = async (agent) => {
  if (isSwitching.value) {
    console.log("Switch already in progress, please wait...");
    return;
  }

  if (currentAgent.value?.id === agent.id) {
    console.log(`${agent.name} is already active`);
    return;
  }

  isSwitching.value = true;
  console.log(`Switching to ${agent.name}...`);

  try {
    // Clean up current chat
    await cleanupChat();
    
    // Initialize new agent
    const success = await initChatWithAgent(agent);
    
    if (success) {
      currentAgent.value = agent;
      console.log(`Successfully switched to ${agent.name}`);
      
      // Setup listener for new agent
      setTimeout(setupChatListener, 1000);
    } else {
      console.error(`Failed to switch to ${agent.name}`);
    }
  } catch (error) {
    console.error("Error during agent switch:", error);
  } finally {
    isSwitching.value = false;
  }
};

onMounted(async () => {
  await loadAgents();
});

onBeforeUnmount(async () => {
  cancelRedirect();
  await cleanupChat();
  
  // Clean up session files
  sessionFiles.value.forEach(file => {
    URL.revokeObjectURL(file.url);
  });
  sessionFiles.value = [];
  
  if (window.wxOConfiguration) {
    delete window.wxOConfiguration;
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
