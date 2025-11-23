<template>
  <div>
    <!-- Root element for watsonx Orchestrate chat -->
    <div id="watsonx-chat-root"></div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  orchestrationId: {
    type: String,
    default: import.meta.env.VITE_WATSONX_ORCHESTRATION_ID
  },
  hostURL: {
    type: String,
    default: import.meta.env.VITE_WATSONX_HOST_URL || 'https://dl.watson-orchestrate.ibm.com'
  },
  deploymentPlatform: {
    type: String,
    default: import.meta.env.VITE_WATSONX_DEPLOYMENT_PLATFORM || 'ibmcloud'
  },
  showLauncher: {
    type: Boolean,
    default: true
  },
  layout: {
    type: Object,
    default: () => ({
      form: 'float',
      width: '30rem',
      height: '40rem'
    })
  },
  style: {
    type: Object,
    default: () => ({
      headerColor: '#000000',
      userMessageBackgroundColor: '#0F62FE',
      primaryColor: '#0F62FE',
      showBackgroundGradient: true
    })
  },
  header: {
    type: Object,
    default: () => ({
      showResetButton: true,
      showAiDisclaimer: true
    })
  }
});

const emit = defineEmits(['chat-ready', 'message-received', 'message-sent', 'error']);

let chatInstance = null;

// Function to get IAM token from backend (avoids CORS issues)
const getIAMToken = async () => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';
  const response = await fetch(`${apiUrl}/api/watsonx/token`);

  if (!response.ok) {
    throw new Error(`Failed to get IAM token: ${response.statusText}`);
  }

  const data = await response.json();
  return data.access_token;
};

const initializeChat = async () => {
  if (!props.orchestrationId) {
    console.error('VITE_WATSONX_ORCHESTRATION_ID is not configured');
    emit('error', { message: 'Orchestration ID not configured' });
    return;
  }

  // Get initial IAM token
  let initialToken;
  try {
    console.log('Fetching initial IAM token...');
    initialToken = await getIAMToken();
    console.log('Initial IAM token received');
  } catch (error) {
    console.error('Failed to get initial IAM token:', error);
    emit('error', { message: 'Failed to authenticate with IBM Cloud' });
    return;
  }

  // Configure watsonx Orchestrate (matches IBM's embed script format)
  const config = {
    orchestrationID: props.orchestrationId,
    hostURL: props.hostURL,
    rootElementID: 'watsonx-chat-root',
    showLauncher: props.showLauncher,
    crn: import.meta.env.VITE_WATSONX_CRN,
    deploymentPlatform: props.deploymentPlatform,
    identityToken: initialToken,
    layout: props.layout,
    style: props.style,
    header: props.header,
    chatOptions: {
      agentId: import.meta.env.VITE_WATSONX_AGENT_ID,
      agentEnvironmentId: import.meta.env.VITE_WATSONX_AGENT_ENV_ID,
      onEvent: [
        {
          type: 'chat:ready',
          handler: (event) => {
            console.log('Watsonx chat ready', event);
            chatInstance = event.instance;
            emit('chat-ready', event);
          }
        },
        {
          type: 'receive',
          handler: (event) => {
            console.log('Message received', event);
            emit('message-received', event);
          }
        },
        {
          type: 'send',
          handler: (event) => {
            console.log('Message sent', event);
            emit('message-sent', event);
          }
        },
        {
          type: 'authTokenNeeded',
          handler: async (event) => {
            console.log('Auth token refresh needed, fetching new IAM token...');
            try {
              const token = await getIAMToken();
              console.log('New IAM token received, setting on event');
              // Set the token on the event object
              event.authToken = token;
            } catch (error) {
              console.error('Failed to refresh IAM token', error);
              emit('error', { message: 'Failed to refresh authentication' });
            }
          }
        }
      ]
    }
  };

  window.wxOConfiguration = config;

  // Load the watsonx Orchestrate embed script (matches IBM's format)
  setTimeout(() => {
    const script = document.createElement('script');
    script.src = `${window.wxOConfiguration.hostURL}/wxochat/wxoLoader.js?embed=true`;
    script.addEventListener('load', () => {
      console.log('Watsonx Orchestrate loader loaded');
      if (window.wxoLoader) {
        window.wxoLoader.init();
      }
    });
    script.addEventListener('error', () => {
      console.error('Failed to load Watsonx Orchestrate embed script');
      emit('error', { message: 'Failed to load chat widget' });
    });
    document.head.appendChild(script);
  }, 0);
};

onMounted(() => {
  initializeChat();
});

onBeforeUnmount(() => {
  // Cleanup
  if (chatInstance) {
    chatInstance = null;
  }
  delete window.wxOConfiguration;
});

// Expose methods to parent component
defineExpose({
  getChatInstance: () => chatInstance
});
</script>

<style scoped>
/* Watsonx chat will inject its own styles */
</style>
