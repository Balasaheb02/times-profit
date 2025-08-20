from flask import Blueprint, request, jsonify
from app import db
from app.models import Page
from app.schemas import page_schema, pages_schema

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/', methods=['GET'])
def get_pages():
    """Get all pages"""
    page_num = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    published_only = request.args.get('published', 'true').lower() == 'true'
    
    query = Page.query
    if published_only:
        query = query.filter(Page.is_published == True)
    
    pages = query.paginate(
        page=page_num, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'pages': pages_schema.dump(pages.items),
        'total': pages.total,
        'total_pages': pages.pages,
        'current_page': page_num
    })

@pages_bp.route('/<page_id>', methods=['GET'])
def get_page_by_id(page_id):
    """Get a specific page by ID"""
    page = Page.query.get_or_404(page_id)
    return jsonify(page_schema.dump(page))

@pages_bp.route('/slug/<slug>', methods=['GET'])
def get_page_by_slug(slug):
    """Get a specific page by slug"""
    page = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    return jsonify(page_schema.dump(page))

@pages_bp.route('/', methods=['POST'])
def create_page():
    """Create a new page"""
    data = request.get_json()
    
    page = Page(
        title=data['title'],
        slug=data['slug'],
        content=data.get('content'),
        meta_title=data.get('meta_title'),
        meta_description=data.get('meta_description'),
        is_published=data.get('is_published', True)
    )
    
    db.session.add(page)
    db.session.commit()
    
    return jsonify(page_schema.dump(page)), 201

@pages_bp.route('/<page_id>', methods=['PUT'])
def update_page(page_id):
    """Update an existing page"""
    page = Page.query.get_or_404(page_id)
    data = request.get_json()
    
    page.title = data.get('title', page.title)
    page.slug = data.get('slug', page.slug)
    page.content = data.get('content', page.content)
    page.meta_title = data.get('meta_title', page.meta_title)
    page.meta_description = data.get('meta_description', page.meta_description)
    page.is_published = data.get('is_published', page.is_published)
    
    db.session.commit()
    
    return jsonify(page_schema.dump(page))

@pages_bp.route('/<page_id>', methods=['DELETE'])
def delete_page(page_id):
    """Delete a page"""
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    
    return jsonify({'message': 'Page deleted successfully'}), 200
