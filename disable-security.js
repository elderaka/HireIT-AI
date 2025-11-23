// Script to disable security for watsonx Orchestrate embedded chat
// This allows anonymous access for testing purposes

import dotenv from 'dotenv';
dotenv.config();

const API_KEY = process.env.WATSONX_API_KEY;
const CRN = process.env.CRN;
const AGENT_ID = '11efeaae-3f0d-4d48-9d5f-a761ccdc4ed1';
const INSTANCE_URL = 'https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376';

async function getIAMToken() {
  const response = await fetch('https://iam.cloud.ibm.com/identity/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${API_KEY}`
  });

  const data = await response.json();
  return data.access_token;
}

async function disableSecurity() {
  try {
    const token = await getIAMToken();
    console.log('Got IAM token');

    // Disable security for the agent's webchat channel
    const response = await fetch(`${INSTANCE_URL}/mfe_home_archer/api/v1/orchestrate/agents/${AGENT_ID}/channels/webchat/security`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        enabled: false
      })
    });

    if (response.ok) {
      console.log('✅ Security disabled successfully!');
      console.log('You can now use the embedded chat without authentication.');
    } else {
      const error = await response.text();
      console.error('❌ Failed to disable security:', response.status, error);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

disableSecurity();
