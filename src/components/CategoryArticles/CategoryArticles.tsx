import { notFound } from "next/navigation"
import { Locale } from "@/i18n/i18n"
import { getTranslations } from "@/i18n/setTranslations"
import { listArticlesByCategorySlug } from "@/lib/backend-client"
import { CategoryArticlesInfiniteDynamic } from "./CategoryArticlesInfiniteDynamic"

export const CATEGORY_ARTICLES_PER_PAGE = 4

type CategoryArticlesProps = {
  category: string
  locale: Locale
}

export async function CategoryArticles({ category, locale }: CategoryArticlesProps) {
  const translations = getTranslations()
  const articles = await listArticlesByCategorySlug({
    locale: locale,
    categorySlug: category,
    skip: 0,
    first: CATEGORY_ARTICLES_PER_PAGE,
  }) as any

  if (!articles || !articles.articles) return notFound()
  
  return (
    <section className="w-full">
      <div className="mb-10 w-full border-b-[1px] py-14">
        <h2 className="mb-6 text-3xl font-bold">{translations.searchCategory}</h2>
        <p className="mb-2 text-xs">{`${translations.showing} ${articles.count || 0} ${translations.resultsFor}`}</p>
        <p className="text-xl font-bold">&quot;{category}&quot;</p>
      </div>
      <div className="mx-auto w-full">
        <CategoryArticlesInfiniteDynamic 
          category={category} 
          initialArticles={{ articles: articles.articles || [], count: articles.count || 0 }} 
        />
      </div>
    </section>
  )
}
