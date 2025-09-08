from flask import Blueprint, request, jsonify
from app import db
from app.models import Article, Author, Category, Tag
from app.schemas import article_schema, articles_schema
from sqlalchemy import desc, func
from datetime import datetime, timedelta

# Create homepage blueprint
homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/api/homepage', methods=['GET'])
def get_homepage():
    """Get homepage data with featured articles and sections"""
    try:
        locale = request.args.get('locale', 'en')
        
        # Get trending articles (based on views)
        trending = Article.query.filter(
            Article.is_published == True
        ).order_by(desc(Article.views)).limit(5).all()
        
        # Get recent articles
        recent = Article.query.filter(
            Article.is_published == True
        ).order_by(desc(Article.published_at)).limit(6).all()
        
        # Get featured articles (you can add a featured flag to Article model)
        featured = Article.query.filter(
            Article.is_published == True
        ).order_by(desc(Article.published_at)).limit(3).all()
        
        # Get categories with article counts
        categories = db.session.query(
            Category.id,
            Category.name,
            Category.slug,
            Category.description,
            func.count(Article.id).label('article_count')
        ).join(Article, Article.category_id == Category.id)\
         .filter(Article.is_published == True)\
         .group_by(Category.id)\
         .limit(6).all()
        
        categories_data = [
            {
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'description': cat.description,
                'articleCount': cat.article_count
            }
            for cat in categories
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'trending_articles': articles_schema.dump(trending),
                'recent_articles': articles_schema.dump(recent),
                'featured_articles': articles_schema.dump(featured),
                'categories': categories_data,
                'total_articles': Article.query.filter(Article.is_published == True).count(),
                'locale': locale
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load homepage data'
        }), 500

@homepage_bp.route('/api/homepage/metadata', methods=['GET'])
def get_homepage_metadata():
    """Get homepage metadata for SEO"""
    try:
        locale = request.args.get('locale', 'en')
        
        # Get latest article for dynamic metadata
        latest_article = Article.query.filter(
            Article.is_published == True
        ).order_by(desc(Article.published_at)).first()
        
        # Get total counts for metadata
        total_articles = Article.query.filter(Article.is_published == True).count()
        total_categories = Category.query.count()
        
        return jsonify({
            'success': True,
            'metadata': {
                'title': 'Times Profit - Latest News and Financial Updates',
                'description': f'Stay updated with the latest news, financial insights, and market trends. Read from {total_articles} articles across {total_categories} categories.',
                'keywords': 'news, finance, market updates, business, economy, stocks, trading',
                'locale': locale,
                'lastUpdated': latest_article.published_at.isoformat() if latest_article else None,
                'articleCount': total_articles,
                'categoryCount': total_categories,
                'ogImage': latest_article.featured_image if latest_article and latest_article.featured_image else '/images/default-og.jpg',
                'canonical': f'https://timesprofit.com/{locale}' if locale != 'en' else 'https://timesprofit.com'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load homepage metadata'
        }), 500
