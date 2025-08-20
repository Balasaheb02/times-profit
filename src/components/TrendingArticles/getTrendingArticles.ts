import { Locale } from "@/i18n/i18n"
import { getTrendingArticles as getBackendTrendingArticles } from "@/lib/backend-client"

export const getTrendingArticles = async (lang: Locale) => {
  try {
    // Try to get trending articles from the new backend
    const articles = await getBackendTrendingArticles(lang, 10)
    return articles
  } catch (error) {
    console.warn('Failed to get trending articles from backend:', error)
    // Return empty array as fallback
    return []
  }
}
