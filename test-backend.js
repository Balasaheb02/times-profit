/**
 * Backend Connection Test Script
 * 
 * This script tests the connection to your Hostinger VPS backend
 * Run with: node test-backend.js
 */

const { testBackendConnection } = require('./src/lib/backend-client.ts')

async function runTests() {
  console.log('🚀 Testing Backend Connection...')
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  
  try {
    // Test 1: Health Check
    console.log('1. Testing health endpoint...')
    const response = await fetch('http://api.timesprofit.com/api/health')
    
    if (response.ok) {
      const data = await response.json()
      console.log('✅ Health Check Success:', data)
    } else {
      console.log('❌ Health Check Failed:', response.status)
    }
    
    // Test 2: Full Backend Client
    console.log('\n2. Testing backend client integration...')
    const isConnected = await testBackendConnection()
    
    if (isConnected) {
      console.log('✅ Backend Client Connected Successfully!')
    } else {
      console.log('⚠️  Backend Client using fallback data')
    }
    
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    console.log('🎉 Test Complete!')
    console.log('\n📋 Next Steps:')
    console.log('1. Deploy frontend to Render')
    console.log('2. Frontend will automatically connect to your VPS backend')
    console.log('3. Site will show real data from your PostgreSQL database')
    
  } catch (error) {
    console.error('❌ Test Failed:', error)
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests()
}

module.exports = { runTests }
