#!/usr/bin/env node

// Real-time testing script to verify DBeaver changes reflect in APIs
const API_BASE_URL = 'http://api.timesprofit.com'

async function monitorDatabaseChanges() {
  console.log('🔄 Real-Time Database Change Monitor')
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.log('')
  console.log('This script monitors your APIs to show real-time changes from DBeaver')
  console.log('Make changes in DBeaver and watch them appear here!')
  console.log('')

  let previousData = {}

  async function checkAPIs() {
    const apis = [
      {
        name: 'Articles Count',
        url: `${API_BASE_URL}/api/articles/count?locale=en`,
        key: 'count'
      },
      {
        name: 'Recent Articles',
        url: `${API_BASE_URL}/api/articles/recent?locale=en&limit=3`,
        key: 'length'
      },
      {
        name: 'Categories',
        url: `${API_BASE_URL}/api/categories?locale=en`,
        key: 'length'
      },
      {
        name: 'Database Stats',
        url: `${API_BASE_URL}/api/admin/stats-json`,
        key: 'table_counts'
      }
    ]

    for (const api of apis) {
      try {
        const response = await fetch(api.url)
        if (response.ok) {
          const data = await response.json()
          
          let currentValue
          if (api.key === 'count') {
            currentValue = data.count || 0
          } else if (api.key === 'length') {
            currentValue = Array.isArray(data) ? data.length : (data.data ? data.data.length : 0)
          } else if (api.key === 'table_counts') {
            currentValue = data.table_counts ? data.table_counts.articles : 0
          }

          const previousValue = previousData[api.name]
          
          if (previousValue !== undefined && previousValue !== currentValue) {
            console.log(`🔥 CHANGE DETECTED: ${api.name}`)
            console.log(`   Previous: ${previousValue}`)
            console.log(`   Current:  ${currentValue}`)
            console.log(`   Time:     ${new Date().toLocaleTimeString()}`)
            console.log('')
          }

          previousData[api.name] = currentValue
          
          if (previousValue === undefined) {
            console.log(`📊 ${api.name}: ${currentValue}`)
          }
        }
      } catch (error) {
        console.log(`❌ ${api.name}: Error - ${error.message}`)
      }
    }
  }

  // Initial check
  console.log('📊 Initial API State:')
  await checkAPIs()
  console.log('')
  console.log('👀 Monitoring for changes... (Press Ctrl+C to stop)')
  console.log('💡 Now go to DBeaver and try:')
  console.log('   • Add a new article')
  console.log('   • Update an existing article title')
  console.log('   • Add a new category')
  console.log('   • Change article view counts')
  console.log('')

  // Monitor every 5 seconds
  setInterval(async () => {
    await checkAPIs()
  }, 5000)
}

// Real-time database change examples
async function showTestQueries() {
  console.log('')
  console.log('🧪 TEST QUERIES FOR DBEAVER:')
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  console.log('')
  console.log('Copy these SQL queries into DBeaver and execute them:')
  console.log('')
  
  console.log('1. 📰 Add a new article:')
  console.log(`INSERT INTO articles (title, slug, excerpt, content, is_published, published_at, views, category_id, author_id, created_at, updated_at)
VALUES (
  'Test Article from DBeaver',
  'test-article-dbeaver-${Date.now()}',
  'This article was created in DBeaver!',
  '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Content created in DBeaver"}]}]}',
  true,
  NOW(),
  1,
  (SELECT id FROM categories LIMIT 1),
  (SELECT id FROM authors LIMIT 1),
  NOW(),
  NOW()
);`)
  console.log('')
  
  console.log('2. 📊 Update article view count:')
  console.log(`UPDATE articles SET views = views + 10 WHERE id = 1;`)
  console.log('')
  
  console.log('3. 🏷️ Add a new category:')
  console.log(`INSERT INTO categories (name, slug, description, created_at, updated_at)
VALUES ('Science', 'science', 'Science and research news', NOW(), NOW());`)
  console.log('')
  
  console.log('4. 📈 Check total counts:')
  console.log(`SELECT 
  (SELECT COUNT(*) FROM articles) as articles,
  (SELECT COUNT(*) FROM categories) as categories,
  (SELECT COUNT(*) FROM authors) as authors;`)
}

if (process.argv[2] === '--help') {
  showTestQueries()
} else {
  monitorDatabaseChanges()
}
