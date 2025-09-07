import { Locale } from "@/i18n/i18n"

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://api.timesprofit.com'

class ApiClient {
  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // Test health endpoint
  async getHealth() {
    return this.request('/api/health')
  }

  // Homepage endpoints
  async getHomepage(locale: string) {
    return this.request(`/api/homepage?locale=${locale}`)
  }

  async getHomepageMetadata(locale: string) {
    return this.request(`/api/homepage/metadata?locale=${locale}`)
  }

  // Navigation endpoints
  async getNavigation(locale: string) {
    return this.request(`/api/navigation?locale=${locale}`)
  }

  async getFooter(locale: string) {
    return this.request(`/api/footer?locale=${locale}`)
  }

  // Article endpoints
  async getArticles(params: {
    locale: string
    skip?: number
    first?: number
    categorySlug?: string
  }) {
    const queryParams = new URLSearchParams({
      locale: params.locale,
      ...(params.skip && { skip: params.skip.toString() }),
      ...(params.first && { first: params.first.toString() }),
      ...(params.categorySlug && { categorySlug: params.categorySlug }),
    })
    
    return this.request(`/api/articles?${queryParams}`)
  }

  async getArticleBySlug(slug: string, locale: string) {
    return this.request(`/api/articles/${slug}?locale=${locale}`)
  }

  async getArticleMetadata(slug: string, locale: string) {
    return this.request(`/api/articles/${slug}/metadata?locale=${locale}`)
  }

  async getTrendingArticles(locale: string, first?: number) {
    const queryParams = new URLSearchParams({
      locale,
      ...(first && { first: first.toString() }),
    })
    
    return this.request(`/api/articles/trending?${queryParams}`)
  }

  async getRecentArticles(locale: string, skip?: number, first?: number) {
    const queryParams = new URLSearchParams({
      locale,
      ...(skip && { skip: skip.toString() }),
      ...(first && { first: first.toString() }),
    })
    
    return this.request(`/api/articles/recent?${queryParams}`)
  }

  async getRecentArticlesWithMain(locale: string, skip?: number, first?: number) {
    const queryParams = new URLSearchParams({
      locale,
      ...(skip && { skip: skip.toString() }),
      ...(first && { first: first.toString() }),
    })
    
    return this.request(`/api/articles/recent-with-main?${queryParams}`)
  }

  // Category endpoints
  async getCategories(locale: string) {
    return this.request(`/api/categories?locale=${locale}`)
  }

  async getArticlesByCategory(params: {
    locale: string
    categoryId: string
    skip?: number
    first?: number
  }) {
    const queryParams = new URLSearchParams({
      locale: params.locale,
      categoryId: params.categoryId,
      ...(params.skip && { skip: params.skip.toString() }),
      ...(params.first && { first: params.first.toString() }),
    })
    
    return this.request(`/api/articles/by-category?${queryParams}`)
  }

  async getArticlesByCategorySlug(params: {
    locale: string
    categorySlug: string
    skip?: number
    first?: number
  }) {
    const queryParams = new URLSearchParams({
      locale: params.locale,
      categorySlug: params.categorySlug,
      ...(params.skip && { skip: params.skip.toString() }),
      ...(params.first && { first: params.first.toString() }),
    })
    
    return this.request(`/api/articles/by-category-slug?${queryParams}`)
  }

  // Pages endpoints
  async getPageBySlug(slug: string, locale: string) {
    return this.request(`/api/pages/${slug}?locale=${locale}`)
  }

  async getPageMetadata(slug: string, locale: string) {
    return this.request(`/api/pages/${slug}/metadata?locale=${locale}`)
  }

  async getPages(locale: string) {
    return this.request(`/api/pages?locale=${locale}`)
  }

  // Utility endpoints
  async getArticlesQuantity(locale: string) {
    const result = await this.request(`/api/articles/count?locale=${locale}`)
    return result.count || 0
  }

  async getArticlesBySlugs(locale: string, slugs: string[]) {
    return this.request(`/api/articles/by-slugs`, {
      method: 'POST',
      body: JSON.stringify({
        locale,
        slugs
      })
    })
  }




  async getRecommendedArticles(articleId: string, locale: string) {
    return this.request(`/api/articles/${articleId}/recommended?locale=${locale}`)
  }

  async getTranslations(locale: string) {
    return this.request(`/api/translations?locale=${locale}`)
  }

  async getQuizQuestions(quizId: string, locale: string, skip?: number) {
    const queryParams = new URLSearchParams({
      locale,
      ...(skip && { skip: skip.toString() })
    })
    
    return this.request(`/api/quiz/${quizId}?${queryParams}`)
  }

  // Database Admin endpoints
  async getDatabaseStats() {
    return this.request('/api/admin/stats-json')
  }

  async getDatabaseTables() {
    return this.request('/api/admin/tables-json')
  }

  async getTableData(tableName: string, limit = 20, offset = 0) {
    const queryParams = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString()
    })
    return this.request(`/api/admin/table-json/${tableName}?${queryParams}`)
  }
}

const apiClient = new ApiClient()

// Import fallback dummy data
import * as dummyClient from './client'

async function withFallback<T>(
  apiCall: () => Promise<T>,
  fallbackCall: () => Promise<T>,
  endpointName: string
): Promise<T> {
  try {
    const result = await apiCall()
    console.log(`✅ API Success: ${endpointName}`)
    return result
  } catch (error) {
    console.warn(`⚠️ API Failed: ${endpointName}, using dummy data`, error)
    return fallbackCall()
  }
}

// Export all functions with fallback to dummy data
export async function getHomepage(locale: Locale) {
  return withFallback(
    async () => {
      // Test health first
      await apiClient.getHealth()
      // Try to get homepage, if endpoint doesn't exist, use dummy data
      try {
        return await apiClient.getHomepage(locale)
      } catch (error) {
        // If homepage endpoint doesn't exist yet, use dummy data
        console.log('Homepage endpoint not implemented yet, using dummy data')
        return dummyClient.getHomepage(locale)
      }
    },
    () => dummyClient.getHomepage(locale),
    'homepage'
  )
}

export async function getHomepageMetadata(locale: Locale) {
  return withFallback(
    async () => {
      try {
        return await apiClient.getHomepageMetadata(locale)
      } catch (error) {
        return dummyClient.getHomepageMetadata(locale)
      }
    },
    () => dummyClient.getHomepageMetadata(locale),
    'homepage metadata'
  )
}

export async function getNavigation(locale: Locale) {
  return withFallback(
    async () => {
      try {
        const [navigation, footer] = await Promise.all([
          apiClient.getNavigation(locale),
          apiClient.getFooter(locale)
        ])
        return { navigation, footer }
      } catch (error) {
        return dummyClient.getNavigation(locale)
      }
    },
    () => dummyClient.getNavigation(locale),
    'navigation'
  )
}

export async function getArticlesQuantity(locale: Locale) {
  return withFallback(
    () => apiClient.getArticlesQuantity(locale),
    () => dummyClient.getArticlesQuantity(locale),
    'articles quantity'
  )
}

export async function listArticlesForSitemap(variables: { locale: Locale; skip?: number; first?: number }) {
  return withFallback(
    () => apiClient.getArticles({
      locale: variables.locale,
      skip: variables.skip,
      first: variables.first
    }),
    () => dummyClient.listArticlesForSitemap(variables),
    'articles for sitemap'
  )
}

export async function getCategories(locale: Locale) {
  return withFallback(
    () => apiClient.getCategories(locale),
    () => dummyClient.getCategories(locale),
    'categories'
  )
}

export async function getTrendingArticles(variables: { locale: Locale; skip?: number; first?: number }) {
  return withFallback(
    () => apiClient.getTrendingArticles(variables.locale, variables.first),
    () => dummyClient.getTrendingArticles(variables),
    'trending articles'
  )
}

export async function getRecentArticles(variables: { locale: Locale; skip?: number; first?: number }) {
  return withFallback(
    () => apiClient.getRecentArticles(variables.locale, variables.skip, variables.first),
    () => dummyClient.getRecentArticles(variables),
    'recent articles'
  )
}

export async function getRecentArticlesWithMain(variables: { locale: Locale; skip?: number; first?: number }) {
  return withFallback(
    () => apiClient.getRecentArticlesWithMain(variables.locale, variables.skip, variables.first),
    () => dummyClient.getRecentArticlesWithMain(variables),
    'recent articles with main'
  )
}

export async function getArticleBySlug(variables: { locale: Locale; slug: string }) {
  return withFallback(
    () => apiClient.getArticleBySlug(variables.slug, variables.locale),
    () => dummyClient.getArticleBySlug(variables),
    `article ${variables.slug}`
  )
}

export async function getArticleMetadataBySlug(variables: { locale: Locale; slug: string }) {
  return withFallback(
    () => apiClient.getArticleMetadata(variables.slug, variables.locale),
    () => dummyClient.getArticleMetadataBySlug(variables),
    `article metadata ${variables.slug}`
  )
}

export async function getPageBySlug(variables: { locale: Locale; slug: string }) {
  return withFallback(
    () => apiClient.getPageBySlug(variables.slug, variables.locale),
    () => dummyClient.getPageBySlug(variables),
    `page ${variables.slug}`
  )
}

export async function getPageMetadataBySlug(variables: { locale: Locale; slug: string }) {
  return withFallback(
    () => apiClient.getPageMetadata(variables.slug, variables.locale),
    () => dummyClient.getPageMetadataBySlug(variables),
    `page metadata ${variables.slug}`
  )
}

export async function listPagesForSitemap(locale: Locale) {
  return withFallback(
    () => apiClient.getPages(locale),
    () => dummyClient.listPagesForSitemap(locale),
    'pages for sitemap'
  )
}

export async function listArticlesBySlugs(variables: { locale: Locale; slugs: string[] }) {
  return withFallback(
    () => apiClient.getArticlesBySlugs(variables.locale, variables.slugs),
    () => dummyClient.listArticlesBySlugs(variables),
    'articles by slugs'
  )
}

export async function listArticlesByCategory(variables: {
  locale: Locale
  categoryId: string
  skip?: number
  first?: number
}) {
  return withFallback(
    () => apiClient.getArticlesByCategory({
      locale: variables.locale,
      categoryId: variables.categoryId,
      skip: variables.skip,
      first: variables.first
    }),
    () => dummyClient.listArticlesByCategory(variables),
    `articles by category ${variables.categoryId}`
  )
}

export async function listArticlesByCategorySlug(variables: {
  locale: Locale
  categorySlug: string
  skip?: number
  first?: number
}) {
  return withFallback(
    () => apiClient.getArticlesByCategorySlug({
      locale: variables.locale,
      categorySlug: variables.categorySlug,
      skip: variables.skip,
      first: variables.first
    }),
    () => dummyClient.listArticlesByCategorySlug(variables),
    `articles by category slug ${variables.categorySlug}`
  )
}

export async function getQuizQuestionsById(variables: { locale: Locale; id: string; skip: number }) {
  return withFallback(
    () => apiClient.getQuizQuestions(variables.id, variables.locale, variables.skip),
    () => dummyClient.getQuizQuestionsById(variables),
    `quiz ${variables.id}`
  )
}

export async function getGlobalTranslations(variables: { locale: Locale }) {
  return withFallback(
    () => apiClient.getTranslations(variables.locale),
    () => dummyClient.getGlobalTranslations(variables),
    'global translations'
  )
}

export async function getArticleRecommendedArticles(variables: { locale: Locale; id: string }) {
  return withFallback(
    () => apiClient.getRecommendedArticles(variables.id, variables.locale),
    () => dummyClient.getArticleRecommendedArticles(variables),
    `recommended articles for ${variables.id}`
  )
}

export async function getRecentArticlesByCategory(variables: { locale: Locale; categorySlug: string; skip?: number; first?: number }) {
  return withFallback(
    () => apiClient.getArticlesByCategorySlug({
      locale: variables.locale,
      categorySlug: variables.categorySlug,
      skip: variables.skip,
      first: variables.first
    }),
    () => dummyClient.getRecentArticlesByCategory(variables),
    `recent articles by category ${variables.categorySlug}`
  )
}

// Export health check function for testing
export async function testBackendConnection() {
  try {
    console.log('Testing backend connection...')
    const healthResponse = await apiClient.getHealth()
    console.log('✅ Backend connection successful!', healthResponse)
    return true
  } catch (error) {
    console.error('❌ Backend connection failed:', error)
    return false
  }
}

// Database Admin Functions
export async function getDatabaseStats() {
  try {
    return await apiClient.getDatabaseStats()
  } catch (error) {
    console.error('Database stats error:', error)
    return { error: 'Failed to get database statistics', status: 'error' }
  }
}

export async function getDatabaseTables() {
  try {
    return await apiClient.getDatabaseTables()
  } catch (error) {
    console.error('Database tables error:', error)
    return { error: 'Failed to get database tables', status: 'error' }
  }
}

export async function getTableData(tableName: string, limit = 20, offset = 0) {
  try {
    return await apiClient.getTableData(tableName, limit, offset)
  } catch (error) {
    console.error(`Table ${tableName} data error:`, error)
    return { error: `Failed to get data from table ${tableName}`, status: 'error' }
  }
}
