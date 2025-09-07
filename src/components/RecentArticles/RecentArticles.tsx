import { Locale } from "@/i18n/i18n"
import { getRecentArticlesWithMain } from "@/lib/backend-client"
import { RecentArticlesInfiniteDynamic } from "./RecentArticlesInfiniteDynamic"
import { ArticleCard, articleToCardProps } from "../ArticleCard/ArticleCard"

export const RECENT_ARTICLES_PER_PAGE = 6

type RecentArticlesProps = {
  title: string
  locale?: Locale
}

export async function RecentArticles({ title, locale = 'en' }: RecentArticlesProps) {
  
  try {
    const initialArticles = await getRecentArticlesWithMain({ locale, first: 3, skip: 1 }) as any
    
    // Defensive checks
    if (!initialArticles || !initialArticles.mainArticle || !Array.isArray(initialArticles.mainArticle) || initialArticles.mainArticle.length === 0) {
      return null
    }
    
    const mainArticle = initialArticles.mainArticle[0] as any
    const recentArticles = Array.isArray(initialArticles.recentArticles) ? initialArticles.recentArticles : []

    // Additional validation
    if (!mainArticle || !mainArticle.id) {
      console.warn('RecentArticles: Invalid main article')
      return null
    }

    return (
      <section className="w-full">
        <h2 className="py-12 pb-8 text-3xl font-bold">{title}</h2>
        <div className="pb-5">
          <ArticleCard
            article={articleToCardProps(mainArticle)}
            orientation="horizontal"
            imageClassName="lg:w-1/2"
            tagsPosition="over"
          />
        </div>
        <RecentArticlesInfiniteDynamic 
          initialArticles={{ 
            articles: recentArticles, 
            count: recentArticles.length 
          }} 
        />
      </section>
    )
  } catch (error) {
    console.error('Error in RecentArticles:', error)
    return null
  }
}
