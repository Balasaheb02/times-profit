from flask import Blueprint, request, jsonify
from app import db
from app.models import Category, Article
from app.schemas import category_schema, categories_schema

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories))

@categories_bp.route('/<slug>', methods=['GET'])
def get_category_by_slug(slug):
    """Get a single category by slug"""
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    return jsonify(category_schema.dump(category))

@categories_bp.route('/<slug>/articles', methods=['GET'])
def get_category_articles(slug):
    """Get articles by category"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    articles = Article.query.filter(
        Article.category_id == category.id,
        Article.is_published == True
    ).order_by(Article.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    from app.schemas import articles_schema
    return jsonify({
        'category': category_schema.dump(category),
        'articles': articles_schema.dump(articles.items),
        'total': articles.total,
        'pages': articles.pages,
        'current_page': page,
        'has_next': articles.has_next,
        'has_prev': articles.has_prev
    })

@categories_bp.route('/', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        category = category_schema.load(json_data)
        db.session.add(category)
        db.session.commit()
        
        return jsonify(category_schema.dump(category)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@categories_bp.route('/<slug>', methods=['PUT'])
def update_category(slug):
    """Update an existing category"""
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        for key, value in json_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        db.session.commit()
        return jsonify(category_schema.dump(category))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@categories_bp.route('/<slug>', methods=['DELETE'])
def delete_category(slug):
    """Delete a category"""
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'})
