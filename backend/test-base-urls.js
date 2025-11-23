/**
 * Test with different base URL formats
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
    
    if (response.ok) {
      const data = await response.json();
      console.log(`   ✅ SUCCESS!`);
      console.log(`   Data:`, JSON.stringify(data, null, 2).substring(0, 500));
      return true;
    } else {
      const text = await response.text();
      console.log(`   Response: ${text.substring(0, 200)}`);
      return false;
    }
  } catch (error) {
    console.log(`   ❌ Error: ${error.message}`);
    return false;
  }
}

async function run() {
  console.log('🔐 Getting IAM token...');
  const token = await getToken();
  console.log('✅ Token obtained\n');
  
  // Try different base URL formats
  const baseUrls = [
    'https://api.us-south.watson-orchestrate.cloud.ibm.com',
    'https://us-south.watson-orchestrate.cloud.ibm.com',
    'https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/ee108010-e155-409a-a2b5-2dfe15fb2376'
  ];
  
  const paths = [
    '/api/v2/orchestrate/agents',
    '/v2/orchestrate/agents',
    '/api/v1/threads',
    '/v1/threads'
  ];
  
  for (const baseUrl of baseUrls) {
    console.log(`\n📍 Testing base URL: ${baseUrl}`);
    console.log('='.repeat(80));
    
    for (const path of paths) {
      const url = `${baseUrl}${path}`;
      const success = await testEndpoint(url, token);
      if (success) {
        console.log(`\n🎉 FOUND WORKING ENDPOINT!`);
        console.log(`   Base URL: ${baseUrl}`);
        console.log(`   Path: ${path}`);
        return;
      }
      await new Promise(resolve => setTimeout(resolve, 300));
    }
  }
  
  console.log('\n❌ No working endpoints found.');
  console.log('\n💡 Suggestion: These APIs might not be available for your instance.');
  console.log('   Check your IBM watsonx Orchestrate documentation or instance settings.');
}

run().catch(console.error);
