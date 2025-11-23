<template>
  <div class="h-screen w-full flex flex-col overflow-hidden font-ibm bg-gradient-to-br from-slate-50 to-neutral-100">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <div class="flex-1 flex items-stretch overflow-hidden min-h-0">
      <!-- Watsonx Chat Container -->
      <div id="watsonx-chat-root" class="flex-1 relative"></div>

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
let watsonxInstance = null;

// Initialize watsonx chat with HireIT orchestrator agent
const initWatsonxChat = async () => {
  console.log("Initializing HireIT Agent...");
  
  // Wait for DOM to be ready
  await new Promise((resolve) => setTimeout(resolve, 300));

  const rootElement = document.getElementById("watsonx-chat-root");
  if (!rootElement) {
    console.error("Root element not found");
    return;
  }
  
  // Ensure root element is clean
  rootElement.innerHTML = "";

  // Get HireIT agent configuration from backend
  let agentConfig;
  try {
    const response = await fetch("http://localhost:3001/api/agents");
    const data = await response.json();
    
    // Find the HireIT agent (formerly AskOrchestrate)
    agentConfig = data.agents.find(
      (a) => a.id === "HireIT_Agent" || a.name === "HireIT"
    );
    
    if (!agentConfig) {
      console.error("HireIT agent not found in configuration");
      return;
    }
    
    console.log("HireIT agent loaded:", agentConfig);
  } catch (error) {
    console.error("Failed to load agent configuration:", error);
    return;
  }

  // Configure watsonx with HireIT orchestrator
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
      showResetButton: true,
      showAiDisclaimer: true,
    },
    chatOptions: {
      agentId: agentConfig.agentId,
      agentEnvironmentId: agentConfig.environmentId,
    },
    style: {
      headerColor: "#0f62fe",
      userMessageBackgroundColor: "#0f62fe",
      primaryColor: "#0f62fe",
      showBackgroundGradient: true,
    },
  };

  // Load watsonx script
  if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
    try {
      console.log("Initializing existing wxoLoader...");
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

    console.log("Loading wxoLoader script...");
    const script = document.createElement("script");
    script.src =
      "https://us-south.watson-orchestrate.cloud.ibm.com/wxochat/wxoLoader.js?embed=true";
    script.onload = () => {
      console.log("wxoLoader script loaded");
      if (window.wxoLoader && typeof window.wxoLoader.init === "function") {
        try {
          watsonxInstance = window.wxoLoader.init();
          console.log("HireIT chat initialized successfully");
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

onMounted(async () => {
  await initWatsonxChat();
});

onBeforeUnmount(() => {
  if (watsonxInstance) {
    try {
      if (typeof watsonxInstance.destroy === "function") {
        watsonxInstance.destroy();
      }
    } catch (e) {
      console.error("Error during unmount cleanup:", e);
    }
    watsonxInstance = null;
  }
  
  // Clean up global configuration
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
