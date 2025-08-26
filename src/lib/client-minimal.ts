import { Locale } from "@/i18n/i18n"

// Minimal dummy data for fast development
const dummyArticles: any[] = [
  {
    id: "1",
    title: "Sample Article 1",
    slug: "sample-article-1",
    publishedAt: "2025-08-19T10:00:00Z",
    updatedAt: "2025-08-19T10:00:00Z",
    locale: "en",
    tags: [{ tag: "sample" }],
    image: { 
      id: "img1",
      data: { url: "/icons/facebook.svg" }, 
      description: { text: "Sample image" },
      title: "Sample"
    },
    author: { 
      id: "a1", 
      name: "John Doe", 
      avatar: { data: { url: "/icons/X.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "This is a sample article for testing." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Technology", slug: "technology" }],
    seoComponent: {
      title: "Sample Article 1",
      description: { text: "A sample article for testing." }
    },
    recommendedArticles: []
  },
  {
    id: "2",
    title: "Sample Article 2",
    slug: "sample-article-2",
    publishedAt: "2025-08-18T15:30:00Z",
    updatedAt: "2025-08-18T15:30:00Z",
    locale: "en",
    tags: [{ tag: "sample" }],
    image: { 
      id: "img2",
      data: { url: "/icons/instagram.svg" }, 
      description: { text: "Sample image 2" },
      title: "Sample 2"
    },
    author: { 
      id: "a2", 
      name: "Jane Doe", 
      avatar: { data: { url: "/icons/youtube.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "This is another sample article for testing." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "News", slug: "news" }],
    seoComponent: {
      title: "Sample Article 2",
      description: { text: "Another sample article for testing." }
    },
    recommendedArticles: []
  }
]

const dummyPages: any[] = [
  { 
    slug: "home", 
    seoComponent: { 
      title: "Home Page", 
      description: { text: "Welcome to our news site" } 
    } 
  },
  { 
    slug: "about", 
    seoComponent: { 
      title: "About Us", 
      description: { text: "Learn more about us" } 
    } 
  }
]

const dummyCategories: any[] = [
  { id: "1", title: "Technology", slug: "technology" },
  { id: "2", title: "News", slug: "news" }
]

const dummyNavigation = {
  categories: dummyCategories,
  pages: dummyPages
}

const dummyHomepage = {
  seoComponent: {
    title: "Times Profit - Latest News",
    description: { text: "Stay updated with the latest news and insights." }
  },
  marketStock: []
}

const dummyQuiz = {
  questions: []
}

const dummyTranslations = {
  "header.home": "Home",
  "header.about": "About",
  "footer.copyright": "© 2025 Times Profit"
}

// Export functions that return minimal data
export async function getHomepage(_locale: Locale) {
  return { ...dummyHomepage, marketStock: dummyHomepage.marketStock }
}

export async function getHomepageMetadata(_locale: Locale) {
  return dummyHomepage
}

export async function getNavigation(_locale: Locale) {
  return dummyNavigation
}

export async function getArticlesQuantity(_locale: Locale) {
  return dummyArticles.length
}

export async function listArticlesForSitemap(variables: { locale: Locale; skip?: number; first?: number }) {
  const { skip = 0, first = 50 } = variables
  return dummyArticles.slice(skip, skip + first)
}

export async function getCategories(_locale: Locale) {
  return dummyCategories
}

export async function getTrendingArticles(variables: { locale: Locale; skip?: number; first?: number }) {
  const { skip = 0, first = 10 } = variables
  return dummyArticles.slice(skip, skip + first)
}

export async function getRecentArticles(variables: { locale: Locale; skip?: number; first?: number }) {
  const { skip = 0, first = 50 } = variables
  return { 
    articles: dummyArticles.slice(skip, skip + first), 
    count: dummyArticles.length 
  }
}

export async function getRecentArticlesWithMain(variables: { locale: Locale; skip?: number; first?: number }) {
  const { skip = 0, first = 50 } = variables
  return { 
    articles: dummyArticles.slice(skip, skip + first), 
    count: dummyArticles.length 
  }
}

export async function getArticleBySlug(variables: { locale: Locale; slug: string }) {
  return dummyArticles.find(a => a.slug === variables.slug) || null
}

export async function getArticleMetadataBySlug(variables: { locale: Locale; slug: string }) {
  const article = dummyArticles.find(a => a.slug === variables.slug)
  return article ? article.seoComponent : null
}

export async function getPageBySlug(variables: { locale: Locale; slug: string }) {
  return dummyPages.find(p => p.slug === variables.slug) || null
}

export async function getPageMetadataBySlug(variables: { locale: Locale; slug: string }) {
  return dummyPages.find(p => p.slug === variables.slug) || null
}

export async function listPagesForSitemap(_locale: Locale) {
  return dummyPages
}

export async function listArticlesBySlugs(variables: { locale: Locale; slugs: string[] }) {
  return dummyArticles.filter(a => variables.slugs.includes(a.slug))
}

export async function listArticlesByCategory(variables: {
  locale: Locale
  categoryId: string
  skip?: number
  first?: number
}) {
  const { skip = 0, first = 50, categoryId } = variables
  const filteredArticles = dummyArticles.filter(article => 
    article.categories.some((cat: any) => cat.slug === categoryId)
  )
  return { 
    articles: filteredArticles.slice(skip, skip + first), 
    count: filteredArticles.length 
  }
}

export async function listArticlesByCategorySlug(variables: {
  locale: Locale
  categorySlug: string
  skip?: number
  first?: number
}) {
  const { skip = 0, first = 50, categorySlug } = variables
  const filteredArticles = dummyArticles.filter(article => 
    article.categories.some((cat: any) => cat.slug === categorySlug)
  )
  return { 
    articles: filteredArticles.slice(skip, skip + first), 
    count: filteredArticles.length 
  }
}

export async function getQuizQuestionsById(_variables: { locale: Locale; id: string; skip: number }) {
  return dummyQuiz
}

export async function getGlobalTranslations(_variables: { locale: Locale }) {
  return dummyTranslations
}
