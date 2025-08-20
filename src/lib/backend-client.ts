import { Locale } from "@/i18n/i18n";
import { apiClient, Article } from "./api-client";

// Helper function to convert HTML content to RichText format
function parseHTMLToRichText(htmlContent: string) {
  // Simple conversion - for a production app, you'd want a proper HTML to RichText parser
  return {
    children: [
      {
        type: "paragraph",
        children: [
          {
            text: htmlContent.replace(/<[^>]*>/g, '') // Strip HTML tags for now
          }
        ]
      }
    ]
  };
}

// Backward compatibility: Convert Flask API response to match existing interface
function convertArticleToLegacyFormat(article: Article) {
  return {
    id: article.id,
    title: article.title,
    slug: article.slug,
    publishedAt: article.published_at,
    updatedAt: article.updated_at,
    locale: "en", // Default to English, you can update this based on your logic
    tags: article.tags?.map(tag => ({ tag: tag.name })) || [],
    image: article.image_url ? {
      id: `img_${article.id}`,
      data: { url: article.image_url },
      description: { text: article.image_alt || article.title },
      title: article.title
    } : null,
    author: {
      id: article.author.id,
      name: article.author.name,
      avatar: article.author.avatar_url ? { data: { url: article.author.avatar_url } } : null
    },
    content: {
      raw: article.content ? parseHTMLToRichText(article.content) : null
    },
    excerpt: article.excerpt
  };
}

// Get homepage data
export async function getHomepage(_locale: Locale) {
  try {
    // Get recent articles for hero and featured content
    const recentArticles = await apiClient.getRecentArticles({ limit: 5 });
    const trendingArticles = await apiClient.getTrendingArticles({ limit: 3 });
    const marketData = await getMarketData();
    
    return {
      heroArticle: recentArticles.length > 0 ? convertArticleToLegacyFormat(recentArticles[0]) : null,
      featuredArticles: recentArticles.slice(1).map(convertArticleToLegacyFormat),
      trendingArticles: trendingArticles.map(convertArticleToLegacyFormat),
      marketStock: marketData
    };
  } catch (error) {
    console.error('Error fetching homepage data:', error);
    // Return fallback data
    return {
      heroArticle: null,
      featuredArticles: [],
      trendingArticles: [],
      marketStock: { data: [] }
    };
  }
}

// Get homepage metadata
export async function getHomepageMetadata(_locale: Locale) {
  return {
    seoComponent: {
      title: "Next News - Latest News and Updates",
      description: {
        text: "Stay updated with the latest news and trending stories from around the world."
      }
    }
  };
}

// List articles by slugs
export async function listArticlesBySlugs({ slugs, locale: _locale }: { slugs: string[]; locale: Locale }) {
  try {
    // Since we can't fetch multiple articles by slugs in one request,
    // we'll need to fetch them individually or implement a batch endpoint
    const articles = await Promise.all(
      slugs.map(async (slug) => {
        try {
          const article = await apiClient.getArticleBySlug(slug);
          return convertArticleToLegacyFormat(article);
        } catch (error) {
          console.error(`Error fetching article ${slug}:`, error);
          return null;
        }
      })
    );
    
    return articles.filter(article => article !== null);
  } catch (error) {
    console.error('Error fetching articles by slugs:', error);
    return [];
  }
}

// Get category by slug
export async function getCategoryBySlug(slug: string, _locale: Locale) {
  try {
    const category = await apiClient.getCategoryBySlug(slug);
    return {
      id: category.id,
      name: category.name,
      slug: category.slug,
      description: category.description
    };
  } catch (error) {
    console.error(`Error fetching category ${slug}:`, error);
    return null;
  }
}

// Get category articles
export async function getCategoryArticles(slug: string, _locale: Locale, page = 1) {
  try {
    const response = await apiClient.getCategoryArticles(slug, { page, per_page: 10 });
    return {
      category: response.category,
      articles: response.articles.map(convertArticleToLegacyFormat),
      pagination: {
        total: response.total,
        pages: response.pages,
        current_page: response.current_page,
        has_next: response.has_next,
        has_prev: response.has_prev
      }
    };
  } catch (error) {
    console.error(`Error fetching category articles for ${slug}:`, error);
    return {
      category: null,
      articles: [],
      pagination: { total: 0, pages: 0, current_page: 1, has_next: false, has_prev: false }
    };
  }
}

// Get recent articles
export async function getRecentArticles(variables: { locale: Locale; skip?: number; first?: number; } | Locale, limit = 10) {
  try {
    // Handle both old signature (locale only) and new signature (object with parameters)
    let actualLimit = limit;
    let actualSkip = 0;
    
    if (typeof variables === 'object' && 'locale' in variables) {
      actualLimit = variables.first || limit;
      actualSkip = variables.skip || 0;
    }
    
    console.log('getRecentArticles called with:', { actualLimit, actualSkip });
    
    const response = await apiClient.getArticles({ 
      per_page: actualLimit + actualSkip, 
      published: true 
    });
    
    console.log('API response received:', { totalArticles: response.articles.length, total: response.total });
    
    // Skip the first 'actualSkip' articles and take 'actualLimit' articles
    const articles = response.articles
      .slice(actualSkip)
      .slice(0, actualLimit)
      .map(convertArticleToLegacyFormat);
    
    console.log('Converted articles:', articles.map(a => ({ id: a.id, title: a.title })));
    
    // For infinite query, return the expected structure
    if (typeof variables === 'object' && 'locale' in variables) {
      const result = {
        articles,
        count: response.total // Total count of articles available
      };
      console.log('Returning for infinite query:', { articlesCount: result.articles.length, totalCount: result.count });
      return result;
    }
    
    // For simple calls, return just the articles array
    console.log('Returning simple array:', { articlesCount: articles.length });
    return articles;
  } catch (error) {
    console.error('Error fetching recent articles:', error);
    // Return appropriate structure based on call type
    if (typeof variables === 'object' && 'locale' in variables) {
      return { articles: [], count: 0 };
    }
    return [];
  }
}

// Get trending articles
export async function getTrendingArticles(_locale: Locale, limit = 10) {
  try {
    const articles = await apiClient.getTrendingArticles({ limit });
    return articles.map(convertArticleToLegacyFormat);
  } catch (error) {
    console.error('Error fetching trending articles:', error);
    return [];
  }
}

// Search articles
export async function searchArticles(query: string, _locale: Locale) {
  try {
    const articles = await apiClient.searchArticles(query);
    return articles.map(convertArticleToLegacyFormat);
  } catch (error) {
    console.error('Error searching articles:', error);
    return [];
  }
}

// Get all categories
export async function getCategories(_locale: Locale) {
  try {
    const categories = await apiClient.getCategories();
    return categories.map(category => ({
      id: category.id,
      name: category.name,
      slug: category.slug,
      description: category.description
    }));
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}

// Get navigation data
export async function getNavigation(_locale: Locale) {
  try {
    const categories = await getCategories(_locale);
    const headerMenu = await apiClient.getHeaderMenu();
    const settings = await getSiteSettings();
    
    return {
      navigation: {
        logo: {
          title: settings.site_title || "Next News",
          href: `/${_locale}`
        },
        elements: [
          // Add header menu items first
          ...headerMenu.map(item => ({
            element: {
              __typename: "Page",
              slug: item.url?.replace('/', '') || item.title.toLowerCase().replace(/\s+/g, '-'),
              title: item.title
            }
          })),
          // Then add categories
          ...categories.map(category => ({
            element: {
              __typename: "Category",
              slug: category.slug,
              title: category.name
            }
          }))
        ]
      },
      footer: await getFooterData(_locale).then(data => data.footer)
    };
  } catch (error) {
    console.error('Error fetching navigation:', error);
    return {
      navigation: {
        logo: {
          title: "Next News",
          href: `/${_locale}`
        },
        elements: []
      },
      footer: {
        legalLinks: [],
        socialLinks: []
      }
    };
  }
}

// Health check
export async function checkBackendHealth() {
  try {
    const health = await apiClient.healthCheck();
    return health;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return { status: 'unhealthy', message: 'Backend is not responding' };
  }
}

// Export the API client for direct use
export { apiClient };

// Legacy exports for backward compatibility
export const getQuizData = async () => ({ questions: [] });
export const getQuizzes = async () => [];

// Quiz functions
export async function getQuizQuestionsById({ locale: _locale, id, skip: _skip }: { locale: Locale; id: string; skip: number }) {
  try {
    const response = await apiClient.getQuizQuestions(id);
    
    // Convert to legacy format expected by frontend
    return response.questions.map(question => ({
      id: question.id,
      question: question.question_text,
      content: {
        raw: question.question_text
      },
      answer: question.answers?.map(answer => ({
        id: answer.id,
        text: answer.answer_text,
        content: {
          raw: answer.answer_text
        },
        isCorrect: answer.is_correct,
        isValid: answer.is_correct
      })) || []
    }));
  } catch (error) {
    console.error('Error fetching quiz questions:', error);
    return [];
  }
}

export async function getAllQuizzes(_locale: Locale) {
  try {
    const response = await apiClient.getQuizzes();
    return response.quizzes.map(quiz => ({
      id: quiz.id,
      title: quiz.title,
      slug: quiz.slug,
      description: quiz.description,
      isActive: quiz.is_active
    }));
  } catch (error) {
    console.error('Error fetching quizzes:', error);
    return [];
  }
}

// Page functions
export async function getPageBySlug(slug: string, _locale: Locale) {
  try {
    const page = await apiClient.getPageBySlug(slug);
    return {
      id: page.id,
      title: page.title,
      slug: page.slug,
      content: {
        raw: page.content
      },
      seoComponent: {
        title: page.meta_title || page.title,
        description: {
          text: page.meta_description || ''
        }
      }
    };
  } catch (error) {
    console.error('Error fetching page:', error);
    return null;
  }
}

export async function getPageMetadataBySlug(slug: string, _locale: Locale) {
  try {
    const page = await apiClient.getPageBySlug(slug);
    return {
      seoComponent: {
        title: page.meta_title || page.title,
        description: {
          text: page.meta_description || ''
        }
      }
    };
  } catch (error) {
    console.error('Error fetching page metadata:', error);
    return null;
  }
}

export async function listPagesForSitemap(_locale: Locale) {
  try {
    const response = await apiClient.getPages({ published: true });
    return response.pages.map(page => ({
      slug: page.slug,
      title: page.title
    }));
  } catch (error) {
    console.error('Error fetching pages for sitemap:', error);
    return [];
  }
}

// Stock market functions
export async function getMarketData() {
  try {
    const response = await apiClient.getStockQuotes({ limit: 10 });
    return {
      data: response.stocks.map(stock => ({
        id: stock.id,
        name: stock.symbol,
        change: `${stock.percent_change || 0}%`,
        symbol: stock.symbol,
        price: stock.current_price,
        percentChange: stock.percent_change,
        volume: stock.volume
      }))
    };
  } catch (error) {
    console.error('Error fetching market data:', error);
    return { data: [] };
  }
}

export async function getTrendingStocks(limit = 5) {
  try {
    const response = await apiClient.getTrendingStocks({ limit });
    return response.trending_stocks.map(stock => ({
      symbol: stock.symbol,
      company: stock.company_name,
      price: stock.current_price,
      change: stock.price_change,
      percentChange: stock.percent_change
    }));
  } catch (error) {
    console.error('Error fetching trending stocks:', error);
    return [];
  }
}

// Site settings functions
export async function getSiteSettings() {
  try {
    const response = await apiClient.getAllSettings();
    return response.settings;
  } catch (error) {
    console.error('Error fetching site settings:', error);
    return {};
  }
}

export async function getFooterData(_locale: Locale) {
  try {
    const settings = await getSiteSettings();
    const footerMenu = await apiClient.getFooterMenu();
    
    return {
      footer: {
        companyName: settings.site_title || 'Next News',
        contactSection: {
          street: settings.footer_address?.split(',')[0] || '123 News Street',
          city: settings.footer_address?.split(',')[1] || 'Media City',
          country: settings.footer_address?.split(',')[2] || 'NY 10001',
          postCode: '10001'
        },
        logo: {
          url: '/logo.png',
          title: settings.site_title || 'Next News'
        },
        links: footerMenu.map(item => ({
          element: {
            __typename: 'Page',
            slug: item.url?.replace('/', '') || item.title.toLowerCase().replace(/\s+/g, '-'),
            title: item.title
          }
        })),
        instagramLink: settings.social_instagram,
        facebookLink: settings.social_facebook,
        twitterLink: settings.social_twitter,
        youtubeLink: settings.social_youtube
      }
    };
  } catch (error) {
    console.error('Error fetching footer data:', error);
    return {
      footer: {
        companyName: 'Next News',
        contactSection: {
          street: '123 News Street',
          city: 'Media City',
          country: 'NY 10001',
          postCode: '10001'
        },
        logo: { url: '/logo.png', title: 'Next News' },
        links: [],
        instagramLink: '',
        facebookLink: '',
        twitterLink: '',
        youtubeLink: ''
      }
    };
  }
}
export const getStock = async () => ({ quotes: [] });

export async function getArticleRecommendedArticles(variables: { locale: Locale; id: string }) {
  try {
    // Get articles from the backend (up to 10 articles)
    const response = await apiClient.getArticles({ per_page: 10, published: true });
    
    // Filter out the current article and get up to 3 recommendations
    const recommended = response.articles
      .filter((article) => article.id !== variables.id)
      .slice(0, 3)
      .map(convertArticleToLegacyFormat);
    
    return recommended;
  } catch (error) {
    console.error('Error fetching recommended articles:', error);
    return [];
  }
}

export async function getArticleBySlug(variables: { locale: Locale; slug: string }) {
  try {
    console.log('getArticleBySlug called with slug:', variables.slug);
    
    // Use the specific endpoint for getting article by slug
    const article = await apiClient.getArticleBySlug(variables.slug);
    console.log('Article fetched from API:', { id: article.id, title: article.title, slug: article.slug });
    
    const convertedArticle = convertArticleToLegacyFormat(article);
    console.log('Converted article:', { id: convertedArticle.id, title: convertedArticle.title });
    
    return convertedArticle;
  } catch (error) {
    console.error('Error fetching article by slug:', error);
    return null;
  }
}

export async function getArticleMetadataBySlug(variables: { locale: Locale; slug: string }) {
  return getArticleBySlug(variables);
}

// Additional functions for backward compatibility
export async function getGlobalTranslations(_locale: Locale) {
  // Return default translations - this would normally come from a CMS
  return {
    readMore: "Read more",
    relatedArticles: "Related articles",
    publishedOn: "Published on",
    byAuthor: "by",
    search: "Search",
    searchPlaceholder: "Search articles...",
    close: "Close",
    loading: "Loading...",
    noResults: "No results found",
    categories: "Categories",
    recent: "Recent",
    trending: "Trending"
  };
}

export async function getRecentArticlesByCategory(variables: { locale: Locale; categoryId: string; limit: number }) {
  try {
    const response = await apiClient.getArticles({ 
      per_page: variables.limit, 
      published: true,
      category: variables.categoryId 
    });
    return response.articles.map(convertArticleToLegacyFormat);
  } catch (error) {
    console.error('Error fetching recent articles by category:', error);
    return [];
  }
}

export async function listArticlesByCategory(variables: { locale: Locale; categorySlug: string; page: number; perPage: number }) {
  try {
    const response = await apiClient.getArticles({ 
      page: variables.page,
      per_page: variables.perPage, 
      published: true 
    });
    return {
      articles: response.articles.map(convertArticleToLegacyFormat),
      totalCount: response.total,
      hasNextPage: response.current_page < response.pages
    };
  } catch (error) {
    console.error('Error listing articles by category:', error);
    return { articles: [], totalCount: 0, hasNextPage: false };
  }
}

export async function listArticlesForSitemap(_locale: Locale, _page = 1) {
  try {
    const response = await apiClient.getArticles({ per_page: 100, published: true });
    return response.articles.map(article => ({
      slug: article.slug,
      updatedAt: article.updated_at
    }));
  } catch (error) {
    console.error('Error fetching articles for sitemap:', error);
    return [];
  }
}

export async function getArticlesQuantity(_locale: Locale) {
  try {
    const response = await apiClient.getArticles({ per_page: 1, published: true });
    return response.total;
  } catch (error) {
    console.error('Error getting articles quantity:', error);
    return 0;
  }
}

export async function getRecentArticlesWithMain(variables: { locale: Locale; first: number; skip: number }) {
  try {
    const response = await apiClient.getArticles({ 
      per_page: variables.first + variables.skip + 1, 
      published: true 
    });
    
    const articles = response.articles.map(convertArticleToLegacyFormat);
    
    return {
      mainArticle: articles.slice(0, 1), // First article as main
      recentArticles: articles.slice(variables.skip, variables.skip + variables.first) // Next articles as recent
    };
  } catch (error) {
    console.error('Error fetching recent articles with main:', error);
    return {
      mainArticle: [],
      recentArticles: []
    };
  }
}
