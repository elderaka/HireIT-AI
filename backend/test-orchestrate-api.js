/**
 * Test script for Orchestrate API endpoints
 * Run with: node test-orchestrate-api.js
 * Backend is running on port 3001
 */

const BASE_URL = 'http://localhost:3001/api/orchestrate';

async function testEndpoint(name, url) {
  console.log(`\n📡 Testing: ${name}`);
  console.log(`   URL: ${url}`);
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (response.ok) {
      console.log(`   ✅ Success (${response.status})`);
      console.log(`   Data:`, JSON.stringify(data, null, 2).substring(0, 500));
    } else {
      console.log(`   ❌ Error (${response.status})`);
      console.log(`   Error:`, data);
    }
  } catch (error) {
    console.log(`   ❌ Failed: ${error.message}`);
  }
}

async function runTests() {
  console.log('🚀 Testing Orchestrate API Endpoints');
  console.log('=====================================');
  
  // Test 1: Get all agents
  await testEndpoint(
    'Get All Agents',
    `${BASE_URL}/agents`
  );
  
  // Test 2: Search agents
  await testEndpoint(
    'Search Agents (query)',
    `${BASE_URL}/agents?query=interview&limit=5`
  );
  
  // Test 3: Get all threads
  await testEndpoint(
    'Get All Threads',
    `${BASE_URL}/threads`
  );
  
  // Test 4: Get threads with limit
  await testEndpoint(
    'Get Threads (limited)',
    `${BASE_URL}/threads?limit=10`
  );
  
  console.log('\n=====================================');
  console.log('✨ All tests completed!');
  console.log('\n📖 For detailed usage, see ORCHESTRATE_API_GUIDE.md');
}

// Run tests
runTests().catch(console.error);
