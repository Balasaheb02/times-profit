import { useLocale } from "@/i18n/i18n"
import { cn } from "@/utils/cn"
import { getTrendingArticles } from "./getTrendingArticles"
import { ArticleCard, articleToCardProps } from "../ArticleCard/ArticleCard"
import { ArticleMinifiedCard } from "../ArticleCard/ArticleMinifiedCard"

type TrendingArticlesProps = {
  title: string
}

export async function TrendingArticles({ title }: TrendingArticlesProps) {
  const locale = useLocale()
  const trendingArticles = await getTrendingArticles(locale)

  // Add defensive check
  if (!trendingArticles || !Array.isArray(trendingArticles) || trendingArticles.length === 0) {
    return null
  }

  const [mainArticle, ...secondaryArticles] = trendingArticles.slice(0, 3)
  const minifiedArticles = trendingArticles.slice(3, 12)

  const isTwoRowLayout = minifiedArticles.length > 0

  return (
    <section className="w-full">
      {trendingArticles.length > 0 && (
        <>
          <h2 className="py-12 pb-8 text-3xl font-bold">{title}</h2>
          <div className={cn(isTwoRowLayout ? "md:grid-cols-3" : "md:grid-cols-2", "grid  grid-cols-1 gap-5")}>
            <div className="col-span-2 flex flex-col gap-5">
              {(mainArticle as any) && (
                <div className="md:h-[388px]">
                  <ArticleCard
                    article={articleToCardProps(mainArticle as any)}
                    tagsPosition="over"
                    lines={"1"}
                    isMain={true}
                  />
                </div>
              )}
              {secondaryArticles.length > 0 && (
                <div className="flex flex-col gap-5 lg:h-[490px] lg:flex-row">
                  {secondaryArticles.map((article: any) => {
                    return (
                      <ArticleCard
                        key={`trending-${article.id}`}
                        article={articleToCardProps(article)}
                        tagsPosition="under"
                      />
                    )
                  })}
                </div>
              )}
            </div>

            {minifiedArticles.length > 0 && (
              <div className="col-span-1 flex flex-col gap-[1.13rem] lg:gap-[1.17rem]">
                {minifiedArticles.map((article: any) => {
                  return (
                    <ArticleMinifiedCard
                      key={`trending-${article.id}`}
                      article={{ title: article.title, imageUrl: article.image?.data.url, slug: article.slug }}
                      locale={locale}
                    />
                  )
                })}
              </div>
            )}
          </div>
        </>
      )}
    </section>
  )
}
