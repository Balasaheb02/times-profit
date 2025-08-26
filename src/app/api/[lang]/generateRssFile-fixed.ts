import { Feed } from "feed"
import { env } from "@/env.mjs"
import { Locale } from "@/i18n/i18n"
import { getRecentArticles } from "@/lib/client"

export default async function generateRssFeed(locale: Locale) {
  const SITE_URL = env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'

  const articlesResponse = await getRecentArticles({ locale, skip: 0, first: 100 })
  
  // Handle both array and object with articles property
  const articles = Array.isArray(articlesResponse) ? articlesResponse : articlesResponse.articles

  const feedOptions = {
    title: "Articles | RSS Feed",
    description: "Welcome to this Articles!",
    id: SITE_URL,
    link: SITE_URL,
    language: locale,
    image: `${SITE_URL}/logo.png`,
    favicon: `${SITE_URL}/favicon.ico`,
    copyright: `All rights reserved ${new Date().getFullYear()}`,
    generator: "Feed for Node.js",
    feedLinks: {
      rss2: `${SITE_URL}/api/${locale}`,
    },
  }

  const feed = new Feed(feedOptions)

  articles.forEach((article: {
    title?: string;
    slug?: string;
    updatedAt?: string;
    author?: { name?: string };
    image?: { data?: { url?: string } };
  }) => {
    const date = article?.updatedAt ? new Date(article.updatedAt) : new Date()
    feed.addItem({
      title: article?.title || 'Untitled',
      id: `${SITE_URL}/${locale}/article/${article?.slug}`,
      link: `${SITE_URL}/${locale}/article/${article?.slug}`,
      description: "test",
      copyright: `All rights reserved ${new Date().getFullYear()}`,
      date,
      author: [{ name: article?.author?.name || 'Anonymous' }],
      image: article?.image?.data?.url,
    })
  })

  return feed
}
