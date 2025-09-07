import { Locale } from "@/i18n/i18n"
import { getTrendingArticles as getBackendTrendingArticles } from "@/lib/client"

export const getTrendingArticles = async (lang: Locale) => {
  try {
    // Get trending articles from local dummy data
    const articles = await getBackendTrendingArticles({ locale: lang, skip: 0, first: 10 })
    
    // Add extra defensive check
    if (!articles || !Array.isArray(articles)) {
      console.warn('getTrendingArticles: Invalid articles data:', articles)
      return []
    }
    
    return articles
  } catch (error) {
    console.warn('Failed to get trending articles:', error)
    // Return empty array as fallback
    return []
  }
}
