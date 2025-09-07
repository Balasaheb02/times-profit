#!/usr/bin/env node

// Test script for database admin functionality
const API_BASE_URL = 'http://api.timesprofit.com'

async function testDatabaseAdmin() {
  console.log('🔍 Testing Database Admin Interface...\n')

  const tests = [
    {
      name: 'Database Health Check',
      url: `${API_BASE_URL}/api/health`,
      description: 'Test basic API health'
    },
    {
      name: 'Database Statistics (JSON)',
      url: `${API_BASE_URL}/api/admin/stats-json`,
      description: 'Get database statistics in JSON format'
    },
    {
      name: 'Database Tables List (JSON)',
      url: `${API_BASE_URL}/api/admin/tables-json`,
      description: 'Get list of all database tables'
    },
    {
      name: 'Articles Table Data (JSON)',
      url: `${API_BASE_URL}/api/admin/table-json/articles?limit=5`,
      description: 'Get sample articles data'
    },
    {
      name: 'Database Dashboard (Web)',
      url: `${API_BASE_URL}/api/admin/db`,
      description: 'Web interface dashboard'
    }
  ]

  for (const test of tests) {
    try {
      console.log(`📊 ${test.name}`)
      console.log(`   ${test.description}`)
      console.log(`   URL: ${test.url}`)
      
      const response = await fetch(test.url)
      
      if (response.ok) {
        const isJson = response.headers.get('content-type')?.includes('application/json')
        
        if (isJson) {
          const data = await response.json()
          console.log(`   ✅ SUCCESS - Status: ${response.status}`)
          
          if (test.name.includes('Statistics')) {
            console.log(`   📈 Database Size: ${data.database_size || 'Unknown'}`)
            if (data.table_counts) {
              console.log(`   📋 Table Counts:`)
              Object.entries(data.table_counts).forEach(([table, count]) => {
                console.log(`      ${table}: ${count}`)
              })
            }
          } else if (test.name.includes('Tables List')) {
            console.log(`   📋 Found ${data.tables?.length || 0} tables`)
            if (data.tables && data.tables.length > 0) {
              console.log(`   📝 Tables: ${data.tables.slice(0, 5).join(', ')}${data.tables.length > 5 ? '...' : ''}`)
            }
          } else if (test.name.includes('Articles Table')) {
            console.log(`   📰 Found ${data.total || 0} total articles`)
            console.log(`   📊 Showing ${data.data?.length || 0} records`)
            if (data.data && data.data.length > 0) {
              console.log(`   📝 Sample article: "${data.data[0].title || 'No title'}"`)
            }
          }
        } else {
          console.log(`   ✅ SUCCESS - Status: ${response.status} (HTML Response)`)
        }
      } else {
        console.log(`   ❌ FAILED - Status: ${response.status}`)
        const errorText = await response.text()
        console.log(`   📝 Error: ${errorText.substring(0, 100)}...`)
      }
    } catch (error) {
      console.log(`   ❌ ERROR - ${error.message}`)
    }
    
    console.log('')
  }

  console.log('🎯 Direct Access URLs:')
  console.log(`   📊 Dashboard: ${API_BASE_URL}/api/admin/db`)
  console.log(`   📋 Tables: ${API_BASE_URL}/api/admin/db/tables`)
  console.log(`   📰 Articles: ${API_BASE_URL}/api/admin/db/table/articles`)
  console.log(`   📈 Statistics: ${API_BASE_URL}/api/admin/db/stats`)
  console.log('')
  console.log('🔧 JSON API Endpoints:')
  console.log(`   ${API_BASE_URL}/api/admin/stats-json`)
  console.log(`   ${API_BASE_URL}/api/admin/tables-json`)
  console.log(`   ${API_BASE_URL}/api/admin/table-json/articles`)
}

// Only run if this script is executed directly
if (require.main === module) {
  testDatabaseAdmin().catch(console.error)
}

module.exports = { testDatabaseAdmin }
