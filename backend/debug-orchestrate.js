/**
 * Debug script to test Orchestrate API authentication and paths
 */

import fetch from 'node-fetch';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, '..', '.env') });

async function getToken() {
  const apiKey = process.env.WATSONX_API_KEY;
  const response = await fetch("https://iam.cloud.ibm.com/identity/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    body: `grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${apiKey}`
  });
  const data = await response.json();
  return data.access_token;
}

async function testEndpoint(url, token) {
  console.log(`\n🔍 Testing: ${url}`);
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });
    
    console.log(`   Status: ${response.status} ${response.statusText}`);
    const text = await response.text();
    console.log(`   Response: ${text.substring(0, 500)}`);
    
    return response.ok;
  } catch (error) {
    console.log(`   ❌ Error: ${error.message}`);
    return false;
  }
}

async function run() {
  console.log('🔐 Getting IAM token...');
  const token = await getToken();
  console.log('✅ Token obtained');
  
  const baseUrl = process.env.SERVICE_INSTANCE_URL;
  console.log(`\n📍 Base URL: ${baseUrl}`);
  
  // Test different path combinations
  const paths = [
    '/api/v2/orchestrate/agents',
    '/v2/orchestrate/agents',
    '/api/agents',
    '/agents',
    '/api/v1/threads',
    '/v1/threads',
    '/api/threads',
    '/threads'
  ];
  
  console.log('\n🧪 Testing different API paths...\n');
  
  for (const path of paths) {
    const url = `${baseUrl}${path}`;
    const success = await testEndpoint(url, token);
    if (success) {
      console.log(`   ✅ SUCCESS! This path works!`);
    }
    await new Promise(resolve => setTimeout(resolve, 500)); // Rate limiting
  }
}

run().catch(console.error);
