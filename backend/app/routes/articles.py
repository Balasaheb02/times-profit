from flask import Blueprint, request, jsonify
from app import db
from app.models import Article, Author, Category, Tag
from app.schemas import article_schema, articles_schema
from sqlalchemy import desc, func
from datetime import datetime, timedelta

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/', methods=['GET'])
def get_articles():
    """Get all articles with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    author = request.args.get('author')
    published_only = request.args.get('published', 'true').lower() == 'true'
    
    query = Article.query
    
    if published_only:
        query = query.filter(Article.is_published == True)
    
    if category:
        query = query.join(Category).filter(Category.slug == category)
    
    if author:
        query = query.join(Author).filter(Author.name.ilike(f'%{author}%'))
    
    query = query.order_by(desc(Article.published_at))
    
    articles = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'articles': articles_schema.dump(articles.items),
        'total': articles.total,
        'pages': articles.pages,
        'current_page': page,
        'has_next': articles.has_next,
        'has_prev': articles.has_prev
    })

@articles_bp.route('/<slug>', methods=['GET'])
def get_article_by_slug(slug):
    """Get a single article by slug"""
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    # Increment view count
    article.views += 1
    db.session.commit()
    
    return jsonify(article_schema.dump(article))

@articles_bp.route('/', methods=['POST'])
def create_article():
    """Create a new article"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate and deserialize input
        article = article_schema.load(json_data)
        db.session.add(article)
        db.session.commit()
        
        return jsonify(article_schema.dump(article)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@articles_bp.route('/<slug>', methods=['PUT'])
def update_article(slug):
    """Update an existing article"""
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Update article fields
        for key, value in json_data.items():
            if hasattr(article, key):
                setattr(article, key, value)
        
        article.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(article_schema.dump(article))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@articles_bp.route('/<slug>', methods=['DELETE'])
def delete_article(slug):
    """Delete an article"""
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    
    db.session.delete(article)
    db.session.commit()
    
    return jsonify({'message': 'Article deleted successfully'})

@articles_bp.route('/trending', methods=['GET'])
def get_trending_articles():
    """Get trending articles based on views in the last 7 days"""
    limit = request.args.get('limit', 10, type=int)
    days = request.args.get('days', 7, type=int)
    
    since_date = datetime.utcnow() - timedelta(days=days)
    
    articles = Article.query.filter(
        Article.is_published == True,
        Article.published_at >= since_date
    ).order_by(desc(Article.views)).limit(limit).all()
    
    return jsonify(articles_schema.dump(articles))

@articles_bp.route('/recent', methods=['GET'])
def get_recent_articles():
    """Get recent articles"""
    limit = request.args.get('limit', 10, type=int)
    
    articles = Article.query.filter(
        Article.is_published == True
    ).order_by(desc(Article.published_at)).limit(limit).all()
    
    return jsonify(articles_schema.dump(articles))

@articles_bp.route('/search', methods=['GET'])
def search_articles():
    """Search articles by title and content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    articles = Article.query.filter(
        Article.is_published == True,
        db.or_(
            Article.title.ilike(f'%{query}%'),
            Article.content.ilike(f'%{query}%')
        )
    ).order_by(desc(Article.published_at)).all()
    
    return jsonify(articles_schema.dump(articles))

@articles_bp.route('/recent-with-main', methods=['GET'])
def get_recent_articles_with_main():
    """Get recent articles with a main article (first one) and others"""
    try:
        locale = request.args.get('locale', 'en')
        skip = request.args.get('skip', 0, type=int)
        first = request.args.get('first', 4, type=int)
        
        # Get recent articles, skipping the specified number
        articles = Article.query.filter(
            Article.is_published == True
        ).order_by(desc(Article.published_at)).offset(skip).limit(first).all()
        
        if not articles:
            return jsonify({
                'success': True,
                'data': {
                    'mainArticle': None,
                    'articles': []
                }
            })
        
        # First article is the main article, rest are regular articles
        main_article = articles[0] if articles else None
        other_articles = articles[1:] if len(articles) > 1 else []
        
        return jsonify({
            'success': True,
            'data': {
                'mainArticle': article_schema.dump(main_article) if main_article else None,
                'articles': articles_schema.dump(other_articles)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load recent articles'
        }), 500

@articles_bp.route('/by-category-slug', methods=['GET'])
def get_articles_by_category_slug():
    """Get articles by category slug"""
    try:
        locale = request.args.get('locale', 'en')
        category_slug = request.args.get('categorySlug')
        skip = request.args.get('skip', 0, type=int)
        first = request.args.get('first', 10, type=int)
        
        if not category_slug:
            return jsonify({'error': 'categorySlug is required'}), 400
        
        # Find category by slug
        category = Category.query.filter_by(slug=category_slug).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Get articles in this category
        articles = Article.query.filter(
            Article.is_published == True,
            Article.category_id == category.id
        ).order_by(desc(Article.published_at)).offset(skip).limit(first).all()
        
        return jsonify({
            'success': True,
            'data': {
                'articles': articles_schema.dump(articles),
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'slug': category.slug,
                    'description': category.description
                },
                'total': Article.query.filter(
                    Article.is_published == True,
                    Article.category_id == category.id
                ).count()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load articles by category'
        }), 500

@articles_bp.route('/count', methods=['GET'])
def get_articles_count():
    """Get total count of published articles"""
    try:
        locale = request.args.get('locale', 'en')
        
        count = Article.query.filter(Article.is_published == True).count()
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'count': 0
        }), 500

@articles_bp.route('/by-slugs', methods=['POST'])
def get_articles_by_slugs():
    """Get articles by multiple slugs"""
    try:
        data = request.get_json()
        if not data or 'slugs' not in data:
            return jsonify({'error': 'slugs array is required'}), 400
        
        locale = data.get('locale', 'en')
        slugs = data['slugs']
        
        articles = Article.query.filter(
            Article.is_published == True,
            Article.slug.in_(slugs)
        ).all()
        
        return jsonify({
            'success': True,
            'data': articles_schema.dump(articles)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load articles by slugs'
        }), 500
