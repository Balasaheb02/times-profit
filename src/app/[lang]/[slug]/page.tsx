import { Metadata } from "next"
import { notFound } from "next/navigation"
import { unstable_setRequestLocale } from "next-intl/server"
import { hygraphLocaleToStandardNotation, i18n, Locale } from "@/i18n/i18n"
import { getPageBySlug, getPageMetadataBySlug, listPagesForSitemap } from "@/lib/client"
import { getMetadataObj } from "@/utils/getMetadataObj"

// Force dynamic rendering to avoid static generation issues
export const dynamic = 'force-dynamic'

type CustomPageProps = {
  params: Promise<{ slug: string; lang: Locale }>
}

export async function generateStaticParams() {
  const pages = await Promise.all(i18n.locales.map((locale) => listPagesForSitemap(locale)))
  const flatPages = pages.flatMap((pages) => pages)
  
  // Generate params for each locale and slug combination
  const staticParams = []
  for (const locale of i18n.locales) {
    for (const page of flatPages) {
      staticParams.push({
        lang: hygraphLocaleToStandardNotation(locale),
        slug: page.slug,
      })
    }
  }
  
  return staticParams
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string; lang: Locale }> }): Promise<Metadata | null> {
  const { slug, lang } = await params
  const metaData = await getPageMetadataBySlug({ locale: lang, slug })
  if (!metaData) return null

  const { seoComponent } = metaData

  return getMetadataObj({ title: seoComponent?.title, description: seoComponent?.description?.text })
}

export default async function Web({ params }: { params: Promise<{ slug: string; lang: Locale }> }) {
  const { slug, lang } = await params
  unstable_setRequestLocale(lang)
  const page = await getPageBySlug({ locale: lang, slug })

  if (!page) notFound()
  return (
    <section className="w-full px-4 pb-16 pt-8">
      <h1 className="mb-8 text-2xl font-semibold">{page.title}</h1>
      {page.content?.raw && (
        <div 
          className="prose prose-gray max-w-none"
          dangerouslySetInnerHTML={{ 
            __html: typeof page.content.raw === 'string' 
              ? page.content.raw 
              : JSON.stringify(page.content.raw)
          }} 
        />
      )}
    </section>
  )
}
