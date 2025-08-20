import { Metadata } from "next"
import { unstable_setRequestLocale } from "next-intl/server"
import { articleToCardProps } from "@/components/ArticleCard/ArticleCard"
import { HeroArticleCard } from "@/components/ArticleCard/HeroArticleCard"
import { HighlightedArticles } from "@/components/HighlightedArticles/HighlightedArticles"
import { RecentArticles } from "@/components/RecentArticles/RecentArticles"
import { StockDisplay } from "@/components/StockDisplay/StockDisplay"
import { TrendingArticles } from "@/components/TrendingArticles/TrendingArticles"
import { i18n, Locale } from "@/i18n/i18n"
import { setTranslations } from "@/i18n/setTranslations"
import { getHomepage, getHomepageMetadata } from "@/lib/backend-client"
import { getMatadataObj } from "@/utils/getMetadataObj"

export const dynamicParams = false

export function generateStaticParams() {
  return i18n.locales.map((lang) => ({ lang }))
}

export async function generateMetadata({ params }: { params: { lang: Locale } }): Promise<Metadata | null> {
  const { seoComponent } = await getHomepageMetadata(params.lang)
  return getMatadataObj({ title: seoComponent?.title, description: seoComponent?.description?.text })
}

export default async function Web({ params }: { params: { lang: Locale } }) {
  unstable_setRequestLocale(params.lang)
  const homepage = await getHomepage(params.lang)
  await setTranslations(params.lang)

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
      <TrendingArticles title="Trending articles" />
      {homepage.featuredArticles && homepage.featuredArticles.length > 0 && (
        <HighlightedArticles
          title="Our picks"
          articles={homepage.featuredArticles}
        />
      )}
      <RecentArticles title="Recent articles" />
    </>
  )
}
