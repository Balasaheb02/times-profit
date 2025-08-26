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
      description: { text: "Climate summit meeting" },
      title: "Climate Summit"
    },
    author: { 
      id: "a2", 
      name: "Michael Chen", 
      avatar: { data: { url: "/icons/youtube.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "World leaders have reached a unanimous agreement on comprehensive climate action policies. The historic accord sets ambitious targets for carbon reduction and renewable energy adoption over the next decade." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Environment", slug: "environment" }],
    seoComponent: {
      title: "Climate Summit Historic Agreement - Environmental News",
      description: { text: "World leaders unite for climate action in historic summit agreement." }
    },
    recommendedArticles: []
  },
  {
    id: "3",
    title: "Championship Finals: Underdog Team Claims Victory",
    slug: "championship-finals-underdog-victory",
    publishedAt: "2025-08-17T20:00:00Z",
    updatedAt: "2025-08-17T20:00:00Z",
    locale: "en",
    tags: [{ tag: "sports" }, { tag: "championship" }, { tag: "football" }],
    image: { 
      id: "img3",
      data: { url: "/icons/facebook.svg" }, 
      description: { text: "Championship celebration" },
      title: "Championship Victory"
    },
    author: { 
      id: "a3", 
      name: "Emma Rodriguez", 
      avatar: { data: { url: "/icons/X.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "In a stunning upset, the underdog team defeated the defending champions 3-2 in an epic finale. The match showcased incredible skill and determination from both sides." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Sports", slug: "sports" }],
    seoComponent: {
      title: "Championship Finals Upset Victory - Sports News",
      description: { text: "Underdog team claims championship in thrilling finale match." }
    },
    recommendedArticles: []
  },
  {
    id: "4",
    title: "Market Analysis: Tech Stocks Surge to New Heights",
    slug: "tech-stocks-surge-new-heights",
    publishedAt: "2025-08-16T09:15:00Z",
    updatedAt: "2025-08-16T09:15:00Z",
    locale: "en",
    tags: [{ tag: "finance" }, { tag: "stocks" }, { tag: "technology" }],
    image: { 
      id: "img4",
      data: { url: "/icons/youtube.svg" }, 
      description: { text: "Stock market charts" },
      title: "Stock Market"
    },
    author: { 
      id: "a4", 
      name: "David Kim", 
      avatar: { data: { url: "/icons/instagram.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "Technology stocks experienced unprecedented growth this week, with several major companies reaching all-time highs. Analysts attribute this surge to strong quarterly earnings and optimistic future projections." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Business", slug: "business" }],
    seoComponent: {
      title: "Tech Stocks Surge Analysis - Financial News",
      description: { text: "Comprehensive analysis of the recent technology stock market surge." }
    },
    recommendedArticles: []
  },
  {
    id: "5",
    title: "Health Breakthrough: New Treatment Shows Promise",
    slug: "health-breakthrough-new-treatment",
    publishedAt: "2025-08-15T14:45:00Z",
    updatedAt: "2025-08-15T14:45:00Z",
    locale: "en",
    tags: [{ tag: "health" }, { tag: "medical" }, { tag: "research" }],
    image: { 
      id: "img5",
      data: { url: "/icons/facebook.svg" }, 
      description: { text: "Medical research laboratory" },
      title: "Medical Research"
    },
    author: { 
      id: "a5", 
      name: "Dr. Lisa Wang", 
      avatar: { data: { url: "/icons/X.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "Researchers have developed a promising new treatment that shows remarkable effectiveness in clinical trials. The breakthrough could potentially help millions of patients worldwide." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Health", slug: "health" }],
    seoComponent: {
      title: "Medical Breakthrough: New Treatment - Health News",
      description: { text: "Exciting new medical treatment shows promise in clinical trials." }
    },
    recommendedArticles: []
  },
  {
    id: "6",
    title: "Space Exploration: Mars Mission Reaches Milestone",
    slug: "mars-mission-reaches-milestone",
    publishedAt: "2025-08-14T11:30:00Z",
    updatedAt: "2025-08-14T11:30:00Z",
    locale: "en",
    tags: [{ tag: "space" }, { tag: "mars" }, { tag: "science" }],
    image: { 
      id: "img6",
      data: { url: "/icons/youtube.svg" }, 
      description: { text: "Mars exploration rover" },
      title: "Mars Mission"
    },
    author: { 
      id: "a6", 
      name: "Dr. James Mitchell", 
      avatar: { data: { url: "/icons/instagram.svg" } } 
    },
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "The latest Mars exploration mission has achieved a significant milestone with the successful deployment of advanced scientific instruments. This achievement brings us closer to understanding the red planet's potential for life." }]
          }
        ]
      }),
      references: []
    },
    categories: [{ title: "Science", slug: "science" }],
    seoComponent: {
      title: "Mars Mission Milestone - Space Exploration News",
      description: { text: "Major breakthrough in Mars exploration brings new discoveries." }
    },
    recommendedArticles: []
  }
]

// Set up recommended articles relationships (DISABLED - causing circular references)
// These are no longer used since we moved to backend-client.ts
// dummyArticles[0].recommendedArticles = [dummyArticles[1], dummyArticles[3], dummyArticles[5]]
// dummyArticles[1].recommendedArticles = [dummyArticles[0], dummyArticles[2], dummyArticles[4]]
// dummyArticles[2].recommendedArticles = [dummyArticles[1], dummyArticles[4], dummyArticles[5]]
// dummyArticles[3].recommendedArticles = [dummyArticles[0], dummyArticles[2], dummyArticles[5]]
// dummyArticles[4].recommendedArticles = [dummyArticles[1], dummyArticles[3], dummyArticles[0]]
// dummyArticles[5].recommendedArticles = [dummyArticles[0], dummyArticles[2], dummyArticles[4]]

const dummyPages: any[] = [
  { 
    slug: "home", 
    title: "Home Page", 
    locale: "en",
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "Welcome to our comprehensive news platform. Stay informed with the latest updates from around the world." }]
          }
        ]
      })
    },
    seoComponent: {
      title: "Home - Global News Platform",
      description: { text: "Your trusted source for breaking news, technology updates, sports, and more." }
    }
  },
  { 
    slug: "about", 
    title: "About Us", 
    locale: "en",
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "We are a dedicated team of journalists and editors committed to delivering accurate, timely, and engaging news content." }]
          }
        ]
      })
    },
    seoComponent: {
      title: "About Us - Global News Platform",
      description: { text: "Learn more about our mission and the team behind our news platform." }
    }
  },
  { 
    slug: "contact", 
    title: "Contact Us", 
    locale: "en",
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "Get in touch with our editorial team. We value your feedback and story suggestions." }]
          }
        ]
      })
    },
    seoComponent: {
      title: "Contact Us - Global News Platform",
      description: { text: "Contact our editorial team for news tips, feedback, or inquiries." }
    }
  },
  { 
    slug: "privacy", 
    title: "Privacy Policy", 
    locale: "en",
    content: { 
      raw: JSON.stringify({
        children: [
          {
            type: "paragraph",
            children: [{ text: "Your privacy is important to us. This policy explains how we collect, use, and protect your personal information." }]
          }
        ]
      })
    },
    seoComponent: {
      title: "Privacy Policy - Global News Platform",
      description: { text: "Learn about our privacy practices and data protection policies." }
    }
  }
]

const dummyQuiz: any[] = [
  { 
    id: "q1", 
    question: "What is the capital of France?", 
    answer: [
      { id: "a1", text: "Paris", isCorrect: true },
      { id: "a2", text: "London", isCorrect: false },
      { id: "a3", text: "Berlin", isCorrect: false },
      { id: "a4", text: "Madrid", isCorrect: false }
    ] 
  },
  { 
    id: "q2", 
    question: "Which programming language is known for web development?", 
    answer: [
      { id: "a5", text: "Python", isCorrect: false },
      { id: "a6", text: "JavaScript", isCorrect: true },
      { id: "a7", text: "C++", isCorrect: false },
      { id: "a8", text: "Java", isCorrect: false }
    ] 
  },
  { 
    id: "q3", 
    question: "What year was the first iPhone released?", 
    answer: [
      { id: "a9", text: "2005", isCorrect: false },
      { id: "a10", text: "2007", isCorrect: true },
      { id: "a11", text: "2008", isCorrect: false },
      { id: "a12", text: "2009", isCorrect: false }
    ] 
  }
]

const dummyCategories: any[] = [
  { id: "cat1", title: "Technology", slug: "technology" },
  { id: "cat2", title: "Sports", slug: "sports" },
  { id: "cat3", title: "Environment", slug: "environment" },
  { id: "cat4", title: "Business", slug: "business" },
  { id: "cat5", title: "Health", slug: "health" },
  { id: "cat6", title: "Science", slug: "science" }
]

const dummyNavigation: any = {
  navigation: { 
    elements: [
      {
        element: {
          __typename: "Category",
          title: "Technology",
          slug: "technology"
        }
      },
      {
        element: {
          __typename: "Category",
          title: "Sports", 
          slug: "sports"
        }
      },
      {
        element: {
          __typename: "Category",
          title: "Environment", 
          slug: "environment"
        }
      },
      {
        element: {
          __typename: "Category",
          title: "Business", 
          slug: "business"
        }
      },
      {
        element: {
          __typename: "Category",
          title: "Health", 
          slug: "health"
        }
      },
      {
        element: {
          __typename: "Category",
          title: "Science", 
          slug: "science"
        }
      },
      {
        element: {
          __typename: "Page",
          title: "About",
          slug: "about"
        }
      },
      {
        element: {
          __typename: "Page",
          title: "Contact",
          slug: "contact"
        }
      }
    ], 
    logo: { url: "/icons/youtube.svg" } 
  },
  footer: { 
    logo: { url: "/icons/youtube.svg" }, 
    additionalLogo: { url: "/icons/facebook.svg" },
    companyName: "Global News Platform",
    ownershipAndCredits: "© 2025 Global News Platform. All rights reserved.",
    youtubeLink: "https://youtube.com/globalnews",
    twitterLink: "https://twitter.com/globalnews",
    instagramLink: "https://instagram.com/globalnews",
    facebookLink: "https://facebook.com/globalnews",
    contactSection: {
      country: "USA",
      city: "New York",
      postCode: "10001",
      street: "123 News Avenue"
    },
    links: [
      {
        element: {
          __typename: "Page",
          title: "About",
          slug: "about"
        }
      },
      {
        element: {
          __typename: "Page",
          title: "Contact",
          slug: "contact"
        }
      },
      {
        element: {
          __typename: "Page",
          title: "Privacy Policy",
          slug: "privacy"
        }
      }
    ]
  }
}

const dummyHomepage: any = {
  heroArticle: dummyArticles[0],
  recentSectionTitle: "Latest News",
  trendingSectionTitle: "Trending Stories", 
  highlightedCategoryTitle: "Featured Technology",
  highlightedCategory: dummyCategories[0],
  highlightedSectionTitle: "Editor's Choice",
  highlightedArticles: [dummyArticles[1], dummyArticles[2], dummyArticles[3]],
  marketStock: {
    data: [
      { symbol: "AAPL", price: 182.50, change: 3.25 },
      { symbol: "GOOGL", price: 2834.75, change: -12.80 },
      { symbol: "MSFT", price: 378.90, change: 8.15 },
      { symbol: "TSLA", price: 265.45, change: -5.30 },
      { symbol: "NVDA", price: 445.20, change: 15.75 },
      { symbol: "META", price: 312.85, change: 2.90 }
    ]
  },
  seoComponent: {
    title: "Global News Platform - Your Source for Breaking News",
    description: { text: "Stay informed with the latest breaking news, technology updates, sports coverage, and in-depth analysis from around the world." }
  }
}

const dummyTranslations: any = {
  hello: "Hello",
  welcome: "Welcome",
  readMore: "Read More",
  search: "Search",
  categories: "Categories",
  recent: "Recent",
  trending: "Trending",
  featured: "Featured",
  showMore: "Show More",
  loadMore: "Load More",
  newsletter: "Newsletter",
  subscribe: "Subscribe",
  contact: "Contact",
  about: "About",
  privacy: "Privacy Policy",
  terms: "Terms of Service",
  copyright: "All rights reserved"
}

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

export async function getRecentArticlesByCategory(variables: {
  locale: Locale
  skip?: number
  first?: number
  categoryId: string
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
    count: dummyArticles.length, 
    mainArticle: dummyArticles[0] 
  }
}

export async function getArticleRecommendedArticles(variables: { locale: Locale; id: string }) {
  const article = dummyArticles.find(a => a.id === variables.id)
  return article ? article.recommendedArticles : []
}

export async function getArticleBySlug(variables: { locale: Locale; slug: string }) {
  return dummyArticles.find(a => a.slug === variables.slug) || null
}

export async function getArticleMetadataBySlug(variables: { locale: Locale; slug: string }) {
  return dummyArticles.find(a => a.slug === variables.slug) || null
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
