# Watsonx Orchestrate Embedded Chat Integration Guide

## Overview
This guide shows how to integrate watsonx Orchestrate agents into your Vue.js application using the embedded webchat widget.

## Prerequisites
1. IBM watsonx Orchestrate instance (Cloud or On-premises v5.2.2+)
2. At least one agent deployed (moved from Draft to Live)
3. Orchestration ID and Host URL from your watsonx Orchestrate instance

## Step 1: Get Your Embed Script

### Option A: From watsonx Orchestrate UI
1. Log into your watsonx Orchestrate instance
2. Navigate to your agent
3. Go to **Channels** → **Embedded agent**
4. Select **Live** tab (requires deployed agent)
5. Click **Copy to clipboard** to get the embed script

### Option B: Using ADK CLI
```bash
orchestrate channels webchat embed --agent-name=your_agent_name
```

The script will look like this:
```javascript
<script>
window.wxOConfiguration = {
  orchestrationID: "your-orgID_orchestrationID",
  hostURL: "https://dl.watson-orchestrate.ibm.com",
  rootElementID: "root",
  showLauncher: false,
  deploymentPlatform: "ibmcloud"
};
</script>
<script src="https://cdn.watson-orchestrate.ibm.com/embed-chat.js"></script>
```

## Step 2: Configure Environment Variables

Create/update `frontend/.env`:
```env
VITE_WATSONX_ORCHESTRATION_ID=your-orgID_orchestrationID
VITE_WATSONX_HOST_URL=https://dl.watson-orchestrate.ibm.com
VITE_WATSONX_DEPLOYMENT_PLATFORM=ibmcloud
```

## Step 3: Security Configuration

### Default Behavior
- Security is **enabled** by default but **not configured**
- The embedded chat will NOT work until you complete security setup OR disable it

### Option A: Enable Security (Recommended for Production)

1. Download the security configuration tool from IBM docs
2. Run the automated setup:
```bash
chmod +x wxO-embed-chat-security-tool.sh
./wxO-embed-chat-security-tool.sh
```

3. The tool generates:
   - IBM key pair (for encryption)
   - Client key pair (for JWT signing)
   - Configuration in `wxo_security_config/` directory

4. Set up a JWT token generation endpoint (see backend implementation)

### Option B: Disable Security (Development/Demo Only)
⚠️ **Not recommended for production or sensitive data**

Contact IBM support or use the security tool to explicitly disable security.

## Step 4: Frontend Implementation

The Vue component is already created at `src/components/WatsonxChat.vue`

### Usage in ChatPage.vue:
```vue
<script setup>
import WatsonxChat from '@/components/WatsonxChat.vue';
</script>

<template>
  <div class="chat-page">
    <!-- Your existing UI -->
    <WatsonxChat />
  </div>
</template>
```

## Step 5: Testing

### Test with Draft Agent (Development)
1. Use Draft mode in watsonx Orchestrate UI
2. Copy the Draft embed script
3. Test locally before deployment

### Test with Live Agent (Production)
1. Deploy your agent in watsonx Orchestrate
2. Use the Live embed script
3. Test in production environment

## Configuration Options

### Layout Modes

**Float (Default)**
```javascript
layout: {
  form: 'float',
  width: '30rem',
  height: '40rem'
}
```

**Fullscreen Overlay**
```javascript
layout: {
  form: 'fullscreen-overlay',
  rootElementID: 'root',
  showLauncher: true
}
```

**Custom Element**
```javascript
layout: {
  form: 'custom',
  customElement: document.getElementById('my-chat-container')
}
```

### Styling

```javascript
style: {
  headerColor: '#0F62FE',
  userMessageBackgroundColor: '#0F62FE',
  primaryColor: '#0F62FE',
  showBackgroundGradient: true
}
```

### Header Options

```javascript
header: {
  showResetButton: true,
  showAiDisclaimer: true
}
```

## Context Variables

Pass data to your agent using JWT tokens:

```javascript
// Your backend generates JWT with context
{
  user_payload: {
    sub: 'user-id-123',
    context_variables: {
      job_id: 'job-12345',
      user_role: 'recruiter',
      company: 'Acme Corp'
    }
  }
}
```

## Events

Handle chat events:

```javascript
chatOptions: {
  onEvent: [
    {
      type: 'chat:ready',
      handler: (event) => {
        console.log('Chat is ready!');
      }
    },
    {
      type: 'receive',
      handler: (event) => {
        console.log('Received message:', event);
      }
    }
  ]
}
```

## Troubleshooting

### Chat widget doesn't appear
- Check browser console for errors
- Verify `rootElementID` matches your HTML element
- Ensure security is properly configured or disabled

### "Security not configured" error
- Complete security setup using the tool
- OR explicitly disable security for testing

### Agent not responding
- Verify agent is deployed (Live mode)
- Check orchestrationID is correct
- Ensure security JWT token is valid

### CORS errors
- Check hostURL matches your watsonx instance
- Verify your domain is whitelisted in watsonx Orchestrate

## API Endpoints Structure

Your backend should provide:

```
POST /api/watsonx/token
- Generate JWT token for security
- Include user context variables

GET /api/watsonx/config
- Return embed configuration
- Environment-specific settings
```

## Production Checklist

- [ ] Security properly configured with key pairs
- [ ] JWT token generation endpoint secured
- [ ] Agent deployed to Live mode
- [ ] Environment variables configured
- [ ] CORS domains whitelisted
- [ ] Error handling implemented
- [ ] User feedback enabled
- [ ] Custom styling applied
- [ ] Context variables working
- [ ] Tested in production environment

## Resources

- [Watsonx Orchestrate Documentation](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)
- [ADK Developer Guide](https://developer.watson-orchestrate.ibm.com)
- Your agents in `/agents` directory
- Your tools in `/tools` directory
