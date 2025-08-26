"use client"

import { useInfiniteQuery } from "@tanstack/react-query"
import { Button } from "@/components/ui/Button/Button"
import { useLocale } from "@/i18n/i18n"
import { useTranslations } from "@/i18n/useTranslations"
import { getRecentArticles } from "@/lib/client"
import { RECENT_ARTICLES_PER_PAGE } from "./RecentArticles"
import { ArticleCard, articleToCardProps } from "../ArticleCard/ArticleCard"

export type RecentArticlesInfiniteProps = {
  initialArticles: { articles: any[]; count: number }
}

export function RecentArticlesInfinite({ initialArticles }: RecentArticlesInfiniteProps) {
  const locale = useLocale()
  const translations = useTranslations()

  const {
    data: recentArticlesQuery,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useInfiniteQuery({
    queryKey: ["recent-articles"],
    queryFn: async ({ pageParam = 0 }) => {
      const result = await getRecentArticles({
        locale,
        skip: RECENT_ARTICLES_PER_PAGE * pageParam + 1,
        first: RECENT_ARTICLES_PER_PAGE,
      });
      // Ensure we return the correct structure
      return result as { articles: any[]; count: number };
    },
    getNextPageParam: (lastPage, pages) => {
      if (lastPage.count <= pages.length * RECENT_ARTICLES_PER_PAGE) return undefined
      return pages.length
    },
    initialData: {
      pages: [initialArticles],
      pageParams: [0],
    },
  })

  const articles = recentArticlesQuery?.pages.flatMap((page) => page.articles)
  if (!articles) return null
  const [...otherArticles] = articles

  return (
    <section className="flex flex-col gap-5">
      <div className="grid gap-5 md:grid-cols-3">
        {otherArticles
          .filter(article => article && article.id && article.title && article.slug)
          .map((article) => {
            try {
              return <ArticleCard key={`recent-${article.id}`} article={articleToCardProps(article)} />
            } catch (error) {
              console.error('Error rendering article card:', error, article);
              return null;
            }
          })
          .filter(Boolean)
        }
      </div>
      {hasNextPage && (
        <Button className="w-full rounded-xl border p-4" disabled={isFetchingNextPage} onClick={() => fetchNextPage()}>
          {translations.showMore}
        </Button>
      )}
    </section>
  )
}

export default RecentArticlesInfinite
