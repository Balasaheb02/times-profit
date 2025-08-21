import { Locale } from "@/i18n/i18n";
import { apiClient, Article } from "./api-client";

// Cache for frequently accessed data
const dataCache = new Map<string, { data: any; timestamp: number; ttl: number }>();

// Cache utility functions
function getCached<T>(key: string): T | null {
  const cached = dataCache.get(key);
  if (cached && Date.now() - cached.timestamp < cached.ttl) {
    return cached.data;
  }
  dataCache.delete(key);
  return null;
}

function setCache<T>(key: string, data: T, ttlMinutes = 5): T {
  dataCache.set(key, {
    data,
    timestamp: Date.now(),
    ttl: ttlMinutes * 60 * 1000
  });
  return data;
}

// Optimized HTML to RichText conversion
function parseHTMLToRichText(htmlContent: string) {
  if (!htmlContent) return null;
  
  return {
    children: [
      {
        type: "paragraph",
        children: [
          {
            text: htmlContent.replace(/<[^>]*>/g, '').trim()
          }
        ]
      }
    ]
  };
}

// Optimized article conversion with memoization
const articleConversionCache = new WeakMap<Article, any>();

function convertArticleToLegacyFormat(article: Article) {
  // Check if we've already converted this article
  if (articleConversionCache.has(article)) {
    return articleConversionCache.get(article);
  }

  const converted = {
    id: article.id,
    title: article.title,
    slug: article.slug,
    publishedAt: article.published_at,
    updatedAt: article.updated_at,
    locale: "en",
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
      raw: parseHTMLToRichText(article.content)
    },
    excerpt: article.excerpt
  };

  articleConversionCache.set(article, converted);
  return converted;
}

// Generic API call wrapper with caching and error handling
async function cachedApiCall<T>(
  cacheKey: string, 
  apiCall: () => Promise<T>, 
  ttlMinutes = 5
): Promise<T | null> {
  try {
    const cached = getCached<T>(cacheKey);
    if (cached) return cached;

    const result = await apiCall();
    return setCache(cacheKey, result, ttlMinutes);
  } catch (error) {
    console.error(`API call failed for ${cacheKey}:`, error);
    return null;
  }
}

// Optimized homepage data fetching
export async function getHomepage(_locale: Locale) {
  return cachedApiCall(
    `homepage_${_locale}`,
    async () => {
      const [recentArticles, trendingArticles, marketData] = await Promise.all([
        apiClient.getRecentArticles({ limit: 5 }),
        apiClient.getTrendingArticles({ limit: 3 }),
        getMarketData()
      ]);

      return {
        heroArticle: recentArticles.length > 0 ? convertArticleToLegacyFormat(recentArticles[0]) : null,
        featuredArticles: recentArticles.slice(1).map(convertArticleToLegacyFormat),
        trendingArticles: trendingArticles.map(convertArticleToLegacyFormat),
        marketStock: marketData || { data: [] }
      };
    },
    2 // 2-minute cache for homepage
  ) || {
    heroArticle: null,
    featuredArticles: [],
    trendingArticles: [],
    marketStock: { data: [] }
  };
}

// Optimized homepage metadata
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

// Batch article fetching for better performance
export async function listArticlesBySlugs({ slugs, locale: _locale }: { slugs: string[]; locale: Locale }) {
  if (!slugs.length) return [];
  
  const cacheKey = `articles_batch_${slugs.sort().join('_')}`;
  
  return cachedApiCall(
    cacheKey,
    async () => {
      // Process in batches to avoid overwhelming the API
      const batchSize = 10;
      const batches = [];
      
      for (let i = 0; i < slugs.length; i += batchSize) {
        const batch = slugs.slice(i, i + batchSize);
        const batchPromises = batch.map(async (slug) => {
          try {
            const article = await apiClient.getArticleBySlug(slug);
            return convertArticleToLegacyFormat(article);
          } catch (error) {
            console.error(`Error fetching article ${slug}:`, error);
            return null;
          }
        });
        batches.push(Promise.all(batchPromises));
      }
      
      const results = await Promise.all(batches);
      return results.flat().filter(Boolean);
    },
    10 // 10-minute cache for article batches
  ) || [];
}

// Optimized page fetching
export async function getPageBySlug(slug: string, _locale: Locale) {
  return cachedApiCall(
    `page_${slug}_${_locale}`,
    async () => {
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
    },
    30 // 30-minute cache for pages
  );
}

// Optimized category fetching
export async function getCategoryBySlug(slug: string, _locale: Locale) {
  return cachedApiCall(
    `category_${slug}`,
    async () => {
      const category = await apiClient.getCategoryBySlug(slug);
      return {
        id: category.id,
        name: category.name,
        slug: category.slug,
        description: category.description
      };
    },
    60 // 60-minute cache for categories
  );
}

// Rest of the functions remain the same but with caching where appropriate...
// [Continue with remaining optimized functions]
