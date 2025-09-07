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
import { getHomepage, getHomepageMetadata } from "@/lib/client"
import { getMetadataObj } from "@/utils/getMetadataObj"

export async function generateMetadata({ params }: { params: Promise<{ lang: Locale }> }): Promise<Metadata | null> {
  const { lang } = await params
  const { seoComponent } = await getHomepageMetadata(lang)
  return getMetadataObj({ title: seoComponent?.title, description: seoComponent?.description?.text })
}

export default async function Web({ params }: { params: Promise<{ lang: Locale }> }) {
  const { lang } = await params
  unstable_setRequestLocale(lang)
  
  try {
    const homepage = await getHomepage(lang)
    await setTranslations(lang)

    return (
      <>
        {homepage.marketStock?.data && <StockDisplay quotes={homepage.marketStock?.data} />}

        {homepage.heroArticle && (
            <HeroArticleCard
              article={articleToCardProps(homepage.heroArticle)}
              asLink
              additionalLink="https://blazity.com/"
            />
        )}
        <TrendingArticles title="Trending articles" locale={lang} />
        {homepage.featuredArticles && Array.isArray(homepage.featuredArticles) && homepage.featuredArticles.length > 0 && (
          <HighlightedArticles
            title="Our picks"
            articles={homepage.featuredArticles}
          />
        )}
        <RecentArticles title="Recent articles" locale={lang} />
      </>
    )
  } catch (error) {
    console.error('Error in homepage:', error)
    return <div>Loading...</div>
  }
}
