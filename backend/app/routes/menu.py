from flask import Blueprint, request, jsonify
from app import db
from app.models import MenuItem
from app.schemas import menu_item_schema, menu_items_schema

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu_items():
    """Get all menu items"""
    menu_type = request.args.get('type', 'header')  # header or footer
    active_only = request.args.get('active', 'true').lower() == 'true'
    
    query = MenuItem.query.filter_by(menu_type=menu_type)
    if active_only:
        query = query.filter(MenuItem.is_active == True)
    
    menu_items = query.order_by(MenuItem.menu_order).all()
    
    return jsonify({
        'menu_type': menu_type,
        'items': menu_items_schema.dump(menu_items)
    })

@menu_bp.route('/header', methods=['GET'])
def get_header_menu():
    """Get header menu items"""
    menu_items = MenuItem.query.filter_by(
        menu_type='header', 
        is_active=True
    ).order_by(MenuItem.menu_order).all()
    
    return jsonify(menu_items_schema.dump(menu_items))

@menu_bp.route('/footer', methods=['GET'])
def get_footer_menu():
    """Get footer menu items"""
    menu_items = MenuItem.query.filter_by(
        menu_type='footer', 
        is_active=True
    ).order_by(MenuItem.menu_order).all()
    
    return jsonify(menu_items_schema.dump(menu_items))

@menu_bp.route('/<item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get a specific menu item by ID"""
    menu_item = MenuItem.query.get_or_404(item_id)
    return jsonify(menu_item_schema.dump(menu_item))

@menu_bp.route('/', methods=['POST'])
def create_menu_item():
    """Create a new menu item"""
    data = request.get_json()
    
    menu_item = MenuItem(
        title=data['title'],
        url=data.get('url'),
        menu_order=data.get('menu_order', 0),
        is_active=data.get('is_active', True),
        menu_type=data.get('menu_type', 'header')
    )
    
    db.session.add(menu_item)
    db.session.commit()
    
    return jsonify(menu_item_schema.dump(menu_item)), 201

@menu_bp.route('/<item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update an existing menu item"""
    menu_item = MenuItem.query.get_or_404(item_id)
    data = request.get_json()
    
    menu_item.title = data.get('title', menu_item.title)
    menu_item.url = data.get('url', menu_item.url)
    menu_item.menu_order = data.get('menu_order', menu_item.menu_order)
    menu_item.is_active = data.get('is_active', menu_item.is_active)
    menu_item.menu_type = data.get('menu_type', menu_item.menu_type)
    
    db.session.commit()
    
    return jsonify(menu_item_schema.dump(menu_item))

@menu_bp.route('/<item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """Delete a menu item"""
    menu_item = MenuItem.query.get_or_404(item_id)
    db.session.delete(menu_item)
    db.session.commit()
    
    return jsonify({'message': 'Menu item deleted successfully'}), 200
