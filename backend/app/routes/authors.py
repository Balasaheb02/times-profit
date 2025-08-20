from flask import Blueprint, request, jsonify
from app import db
from app.models import Author
from app.schemas import author_schema, authors_schema

authors_bp = Blueprint('authors', __name__)

@authors_bp.route('/', methods=['GET'])
def get_authors():
    """Get all authors"""
    authors = Author.query.all()
    return jsonify(authors_schema.dump(authors))

@authors_bp.route('/<author_id>', methods=['GET'])
def get_author(author_id):
    """Get a single author by ID"""
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    
    return jsonify(author_schema.dump(author))

@authors_bp.route('/', methods=['POST'])
def create_author():
    """Create a new author"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        author = author_schema.load(json_data)
        db.session.add(author)
        db.session.commit()
        
        return jsonify(author_schema.dump(author)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@authors_bp.route('/<author_id>', methods=['PUT'])
def update_author(author_id):
    """Update an existing author"""
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        for key, value in json_data.items():
            if hasattr(author, key):
                setattr(author, key, value)
        
        db.session.commit()
        return jsonify(author_schema.dump(author))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@authors_bp.route('/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    """Delete an author"""
    author = Author.query.get(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    
    db.session.delete(author)
    db.session.commit()
    
    return jsonify({'message': 'Author deleted successfully'})
