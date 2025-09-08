import { Metadata } from "next"
import { unstable_setRequestLocale } from "next-intl/server"
import { articleToCardProps } from "@/components/ArticleCard/ArticleCard"
import { HeroArticleCard } from "@/components/ArticleCard/HeroArticleCard"
import { HighlightedArticles } from "@/components/HighlightedArticles/HighlightedArticles"
import { RecentArticles } from "@/components/RecentArticles/RecentArticles"
import { StockDisplay } from "@/components/StockDisplay/StockDisplay"
import { TrendingArticles } from "@/components/TrendingArticles/TrendingArticles"
import { Locale } from "@/i18n/i18n"
import { setTranslations } from "@/i18n/setTranslations"
import { getHomepage, getHomepageMetadata, testBackendConnection } from "@/lib/backend-client"
import { getMetadataObj } from "@/utils/getMetadataObj"

export async function generateMetadata({ params }: { params: Promise<{ lang: Locale }> }): Promise<Metadata | null> {
  const { lang } = await params
  const homepageMetadata = await getHomepageMetadata(lang) as any
  return getMetadataObj({ title: homepageMetadata?.seoComponent?.title, description: homepageMetadata?.seoComponent?.description?.text })
}

export default async function Web({ params }: { params: Promise<{ lang: Locale }> }) {
  const { lang } = await params
  unstable_setRequestLocale(lang)
  
  try {
    // Test backend connection first
    console.log('🔍 Testing backend connection...')
    await testBackendConnection()
    console.log('✅ Backend connection successful')
    
    console.log('🔍 Fetching homepage data...')
    const homepage = await getHomepage(lang) as any
    console.log('✅ Homepage data fetched:', { 
      hasData: !!homepage, 
      heroArticle: !!homepage?.heroArticle,
      featuredArticles: homepage?.featuredArticles?.length || 0,
      marketStock: !!homepage?.marketStock?.data
    })
    
    await setTranslations(lang)

    // Handle backend data structure vs dummy data structure
    const heroArticle = homepage?.heroArticle || homepage?.data?.featured_articles?.[0]
    const featuredArticles = homepage?.featuredArticles || homepage?.data?.featured_articles

    console.log('🔍 Processed data:', {
      heroArticle: !!heroArticle,
      featuredArticlesCount: featuredArticles?.length || 0
    })

    return (
      <>
        {homepage?.marketStock?.data && Array.isArray(homepage.marketStock.data) && homepage.marketStock.data.length > 0 && (
          <StockDisplay quotes={homepage.marketStock.data} />
        )}

        {heroArticle && (
            <HeroArticleCard
              article={articleToCardProps(heroArticle)}
              asLink
              additionalLink="https://blazity.com/"
            />
        )}
        <TrendingArticles title="Trending articles" locale={lang} />
        {featuredArticles && Array.isArray(featuredArticles) && featuredArticles.length > 0 && (
          <HighlightedArticles
            title="Our picks"
            articles={featuredArticles}
          />
        )}
        <RecentArticles title="Recent articles" locale={lang} />
      </>
    )
  } catch (error) {
    console.error('💥 Error in homepage:', error)
    console.error('💥 Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : 'No stack trace',
      name: error instanceof Error ? error.name : 'Unknown error type'
    })
    
    // Return a fallback UI instead of throwing
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Unable to load content</h1>
          <p className="text-gray-600">We're experiencing technical difficulties. Please try again later.</p>
          <p className="text-sm text-gray-400 mt-2">Error: {error instanceof Error ? error.message : 'Unknown error'}</p>
        </div>
      </div>
    )
  }
}
