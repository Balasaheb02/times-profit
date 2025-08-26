import { ArticleCard, articleToCardProps } from "../ArticleCard/ArticleCard"

type HighlightedArticlesProps = {
  title: string
  articles: any[]
}

export async function HighlightedArticles({ title, articles }: HighlightedArticlesProps) {
  // Defensive check to ensure articles is an array
  if (!articles || !Array.isArray(articles) || articles.length === 0) {
    return null
  }

  return (
    <section className="w-full">
      <h2 className="py-12 pb-8 text-3xl font-bold">{title}</h2>
      <div className="grid gap-5 md:grid-cols-2">
        {articles.map((article: any) => {
          return (
            <ArticleCard
              orientation="vertical"
              key={`highlighted-${article.id}`}
              tagsPosition="over"
              lines={"2"}
              article={articleToCardProps(article)}
            />
          )
        })}
      </div>
    </section>
  )
}
