import { Metadata } from "next/types"
import { unstable_setRequestLocale } from "next-intl/server"
import { CategoryArticles } from "@/components/CategoryArticles/CategoryArticles"
import { Locale } from "@/i18n/i18n"
import { setTranslations } from "@/i18n/setTranslations"
import { getMetadataObj } from "@/utils/getMetadataObj"

type ArticlePageProps = { params: Promise<{ slug: string; lang: Locale }> }

export async function generateMetadata({ params }: { params: Promise<{ slug: string; lang: Locale }> }): Promise<Metadata | null> {
  const { slug } = await params
  return getMetadataObj({ title: `Category - ${slug}`, description: undefined })
}

export default async function Web({ params }: { params: Promise<{ slug: string; lang: Locale }> }) {
  const { slug, lang } = await params
  unstable_setRequestLocale(lang)
  await setTranslations(lang)

  return <CategoryArticles category={slug} locale={lang} />
}
