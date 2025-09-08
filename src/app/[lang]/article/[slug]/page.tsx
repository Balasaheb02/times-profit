import { RichTextContent } from "@graphcms/rich-text-types"
import { notFound } from "next/navigation"
import { Metadata } from "next/types"
import { HeroArticleCard } from "@/components/ArticleCard/HeroArticleCard"
import { RecommendedArticles } from "@/components/RecommendedArticles/RecommendedArticles"
import { RichText } from "@/components/RichText/RichText"
import { ShareOnSocial } from "@/components/ShareOnSocial/ShareOnSocial"
import { env } from "@/env.mjs"
import { Locale } from "@/i18n/i18n"
import { getArticleBySlug, getArticleMetadataBySlug } from "@/lib/backend-client"
import { getMetadataObj } from "@/utils/getMetadataObj"

type ArticlePageProps = { params: Promise<{ slug: string; lang: Locale }> }

export async function generateMetadata({ params }: { params: Promise<{ slug: string; lang: Locale }> }): Promise<Metadata | null> {
  const { slug, lang } = await params
  const article = await getArticleMetadataBySlug({ locale: lang, slug })
  if (!article) return null
  const { seoComponent } = article

  const description = seoComponent?.description?.text
  const title = seoComponent?.title

  return getMetadataObj({ description, title })
}

export default async function Web({ params }: { params: Promise<{ slug: string; lang: Locale }> }) {
  const { slug, lang } = await params
  const article = await getArticleBySlug({ locale: lang, slug })
  const articleUrl = `${env.NEXT_PUBLIC_SITE_URL}/article/${slug}`
  const initialQuiz = article?.content?.references?.[0] || null

  if (!article) return notFound()

  const { image, publishedAt, title, tags, author } = article
  return (
    <>
      <article className="w-full pb-16 pt-8">
        <HeroArticleCard
          article={{
            imageAlt: image?.description?.text,
            imageUrl: image?.data?.url,
            publicationDate: publishedAt,
            title,
            author: { name: author?.name ?? "Anonymous", imageUrl: author?.avatar?.data?.url },
            tags: tags.map(({ tag }: { tag: string }) => tag),
            slug,
          }}
          asLink={false}
        />
        <ShareOnSocial articleUrl={articleUrl} articleTitle={title} />
        {article.content && article.content.raw && (
          <section className="flex w-full flex-col pt-8">
            <RichText 
              references={initialQuiz ? [initialQuiz] : []} 
              raw={typeof article.content.raw === 'string' ? JSON.parse(article.content.raw) as RichTextContent : article.content.raw as RichTextContent} 
            />
          </section>
        )}
      </article>
      <div className="mb-5 border-t py-5">
        <ShareOnSocial articleUrl={articleUrl} articleTitle={title} />
      </div>
      <RecommendedArticles id={article.id} />
    </>
  )
}
