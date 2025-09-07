#!/usr/bin/env node

// Quick verification script for database admin after backend restart
const API_BASE_URL = 'http://api.timesprofit.com'

async function quickTest() {
  console.log('🔍 Quick Database Admin Verification...\n')

  const tests = [
    { name: 'Health Check', url: `${API_BASE_URL}/api/health` },
    { name: 'Database Stats', url: `${API_BASE_URL}/api/admin/stats-json` },
    { name: 'Tables List', url: `${API_BASE_URL}/api/admin/tables-json` },
    { name: 'Web Dashboard', url: `${API_BASE_URL}/api/admin/db` }
  ]

  let successCount = 0

  for (const test of tests) {
    try {
      const response = await fetch(test.url)
      if (response.ok) {
        console.log(`✅ ${test.name} - Working`)
        successCount++
      } else {
        console.log(`❌ ${test.name} - Failed (${response.status})`)
      }
    } catch (error) {
      console.log(`❌ ${test.name} - Error: ${error.message}`)
    }
  }

  console.log(`\n📊 Result: ${successCount}/${tests.length} tests passed`)
  
  if (successCount === tests.length) {
    console.log('\n🎉 SUCCESS! Database admin is working perfectly!')
    console.log('\n🌐 Access your database admin at:')
    console.log(`📊 ${API_BASE_URL}/api/admin/db`)
  } else {
    console.log('\n⚠️  Some tests failed. Please restart the backend service.')
    console.log('\nRun on your VPS:')
    console.log('sudo systemctl restart newsapp')
  }
}

quickTest().catch(console.error)
