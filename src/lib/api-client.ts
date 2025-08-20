// API Base URL - update this to match your Flask backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

// API Client class
class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (this.token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${this.token}`,
      };
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  // Articles API
  async getArticles(params?: {
    page?: number;
    per_page?: number;
    category?: string;
    author?: string;
    published?: boolean;
  }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const query = searchParams.toString();
    return this.request<{
      articles: Article[];
      total: number;
      pages: number;
      current_page: number;
      has_next: boolean;
      has_prev: boolean;
    }>(`/articles${query ? `?${query}` : ''}`);
  }

  async getArticleBySlug(slug: string) {
    return this.request<Article>(`/articles/${slug}`);
  }

  async createArticle(article: Partial<Article>) {
    return this.request<Article>('/articles', {
      method: 'POST',
      body: JSON.stringify(article),
    });
  }

  async updateArticle(slug: string, updates: Partial<Article>) {
    return this.request<Article>(`/articles/${slug}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteArticle(slug: string) {
    return this.request<{ message: string }>(`/articles/${slug}`, {
      method: 'DELETE',
    });
  }

  async getTrendingArticles(params?: { limit?: number; days?: number }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const query = searchParams.toString();
    return this.request<Article[]>(`/articles/trending${query ? `?${query}` : ''}`);
  }

  async getRecentArticles(params?: { limit?: number }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const query = searchParams.toString();
    return this.request<Article[]>(`/articles/recent${query ? `?${query}` : ''}`);
  }

  async searchArticles(query: string) {
    return this.request<Article[]>(`/articles/search?q=${encodeURIComponent(query)}`);
  }

  // Categories API
  async getCategories() {
    return this.request<Category[]>('/categories');
  }

  async getCategoryBySlug(slug: string) {
    return this.request<Category>(`/categories/${slug}`);
  }

  async getCategoryArticles(slug: string, params?: { page?: number; per_page?: number }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const query = searchParams.toString();
    return this.request<{
      category: Category;
      articles: Article[];
      total: number;
      pages: number;
      current_page: number;
      has_next: boolean;
      has_prev: boolean;
    }>(`/categories/${slug}/articles${query ? `?${query}` : ''}`);
  }

  // Authors API
  async getAuthors() {
    return this.request<Author[]>('/authors');
  }

  async getAuthor(id: string) {
    return this.request<Author>(`/authors/${id}`);
  }

  // Auth API
  async login(username: string, password: string) {
    const response = await this.request<{
      access_token: string;
      user: User;
    }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    
    this.setToken(response.access_token);
    return response;
  }

  async register(username: string, email: string, password: string) {
    return this.request<{
      message: string;
      user: User;
    }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  async getProfile() {
    return this.request<User>('/auth/profile');
  }

  async updateProfile(updates: { username?: string; email?: string }) {
    return this.request<User>('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  // Health check
  async healthCheck() {
    return this.request<{ status: string; message: string }>('/health');
  }
}

// Types
export interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  image_url?: string;
  image_alt?: string;
  published_at: string;
  created_at: string;
  updated_at: string;
  is_published: boolean;
  views: number;
  author_id: string;
  category_id?: string;
  author: Author;
  category?: Category;
  tags: Tag[];
}

export interface Author {
  id: string;
  name: string;
  email: string;
  bio?: string;
  avatar_url?: string;
  created_at: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  created_at: string;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
  created_at: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  is_admin: boolean;
  created_at: string;
}

// Export singleton instance
export const apiClient = new ApiClient();
export default apiClient;
