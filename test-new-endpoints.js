#!/usr/bin/env node

// Test script for the new API endpoints
const API_BASE_URL = 'http://api.timesprofit.com'

async function testNewEndpoints() {
  console.log('🧪 Testing New API Endpoints...\n')

  const tests = [
    {
      name: 'Homepage Data',
      url: `${API_BASE_URL}/api/homepage?locale=en`,
      description: 'Main homepage data with articles and categories'
    },
    {
      name: 'Homepage Metadata',
      url: `${API_BASE_URL}/api/homepage/metadata?locale=en`,
      description: 'SEO metadata for homepage'
    },
    {
      name: 'Recent Articles with Main',
      url: `${API_BASE_URL}/api/articles/recent-with-main?locale=en&skip=1&first=3`,
      description: 'Recent articles with main article structure'
    },
    {
      name: 'Articles Count',
      url: `${API_BASE_URL}/api/articles/count?locale=en`,
      description: 'Total count of published articles'
    },
    {
      name: 'Articles by Category Slug',
      url: `${API_BASE_URL}/api/articles/by-category-slug?locale=en&categorySlug=technology&first=5`,
      description: 'Articles filtered by category slug'
    },
    {
      name: 'Database Admin',
      url: `${API_BASE_URL}/api/admin/stats-json`,
      description: 'Database admin statistics'
    }
  ]

  let successCount = 0
  let detailedResults = {}

  for (const test of tests) {
    try {
      console.log(`🔍 Testing: ${test.name}`)
      const response = await fetch(test.url)
      
      if (response.ok) {
        const data = await response.json()
        console.log(`✅ SUCCESS - ${test.name}`)
        
        // Show some key details
        if (test.name === 'Homepage Data' && data.data) {
          console.log(`   📰 Found ${data.data.recent_articles?.length || 0} recent articles`)
          console.log(`   📈 Found ${data.data.trending_articles?.length || 0} trending articles`)
          console.log(`   🏷️ Found ${data.data.categories?.length || 0} categories`)
        } else if (test.name === 'Recent Articles with Main' && data.data) {
          console.log(`   📰 Main article: ${data.data.mainArticle?.title || 'None'}`)
          console.log(`   📋 Other articles: ${data.data.articles?.length || 0}`)
        } else if (test.name === 'Articles Count') {
          console.log(`   📊 Total articles: ${data.count || 0}`)
        } else if (test.name === 'Database Admin' && data.table_counts) {
          console.log(`   📊 Articles in DB: ${data.table_counts.articles || 0}`)
          console.log(`   🏷️ Categories in DB: ${data.table_counts.categories || 0}`)
        }
        
        successCount++
        detailedResults[test.name] = { status: 'success', data: data }
      } else {
        console.log(`❌ FAILED - ${test.name} (Status: ${response.status})`)
        detailedResults[test.name] = { status: 'failed', code: response.status }
      }
    } catch (error) {
      console.log(`❌ ERROR - ${test.name}: ${error.message}`)
      detailedResults[test.name] = { status: 'error', error: error.message }
    }
    console.log('')
  }

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.log(`📊 RESULTS: ${successCount}/${tests.length} endpoints working`)
  
  if (successCount === tests.length) {
    console.log('\n🎉 EXCELLENT! All new API endpoints are working!')
    console.log('🌟 Your frontend should now load real data instead of dummy data')
    console.log('✅ No more 404 errors for homepage and articles')
    console.log('\n🌐 Your full-stack application is now fully connected!')
  } else if (successCount > 0) {
    console.log('\n⚠️  Some endpoints are working, but some still need backend deployment')
    console.log('📋 Make sure to restart your Flask service: sudo systemctl restart newsapp')
  } else {
    console.log('\n❌ No new endpoints are working yet')
    console.log('🔧 Please deploy the backend changes first:')
    console.log('   1. Upload new route files to your VPS')
    console.log('   2. Restart Flask service: sudo systemctl restart newsapp')
  }
  
  console.log('\n🔗 Frontend Development Server:')
  console.log('   http://localhost:3000 - Should now show real data!')
}

testNewEndpoints().catch(console.error)
