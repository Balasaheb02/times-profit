from flask import Blueprint, request, jsonify
from app import db
from app.models import SiteSettings
from app.schemas import site_settings_schema, site_settings_list_schema
import json

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET'])
def get_all_settings():
    """Get all site settings"""
    settings = SiteSettings.query.all()
    
    # Convert to a more usable format
    settings_dict = {}
    for setting in settings:
        if setting.setting_type == 'json':
            try:
                settings_dict[setting.setting_key] = json.loads(setting.setting_value or '{}')
            except:
                settings_dict[setting.setting_key] = {}
        elif setting.setting_type == 'boolean':
            settings_dict[setting.setting_key] = setting.setting_value.lower() == 'true'
        elif setting.setting_type == 'number':
            try:
                settings_dict[setting.setting_key] = float(setting.setting_value)
            except:
                settings_dict[setting.setting_key] = 0
        else:
            settings_dict[setting.setting_key] = setting.setting_value
    
    return jsonify({
        'settings': settings_dict,
        'raw_settings': site_settings_list_schema.dump(settings)
    })

@settings_bp.route('/<setting_key>', methods=['GET'])
def get_setting(setting_key):
    """Get a specific setting by key"""
    setting = SiteSettings.query.filter_by(setting_key=setting_key).first_or_404()
    
    # Parse the value based on type
    if setting.setting_type == 'json':
        try:
            value = json.loads(setting.setting_value or '{}')
        except:
            value = {}
    elif setting.setting_type == 'boolean':
        value = setting.setting_value.lower() == 'true' if setting.setting_value else False
    elif setting.setting_type == 'number':
        try:
            value = float(setting.setting_value) if setting.setting_value else 0
        except:
            value = 0
    else:
        value = setting.setting_value
    
    return jsonify({
        'key': setting_key,
        'value': value,
        'type': setting.setting_type,
        'description': setting.description
    })

@settings_bp.route('/navigation', methods=['GET'])
def get_navigation_settings():
    """Get navigation-specific settings"""
    nav_settings = SiteSettings.query.filter(
        SiteSettings.setting_key.like('nav_%')
    ).all()
    
    return jsonify(site_settings_list_schema.dump(nav_settings))

@settings_bp.route('/footer', methods=['GET'])
def get_footer_settings():
    """Get footer-specific settings"""
    footer_settings = SiteSettings.query.filter(
        SiteSettings.setting_key.like('footer_%')
    ).all()
    
    return jsonify(site_settings_list_schema.dump(footer_settings))

@settings_bp.route('/seo', methods=['GET'])
def get_seo_settings():
    """Get SEO-specific settings"""
    seo_settings = SiteSettings.query.filter(
        SiteSettings.setting_key.like('seo_%')
    ).all()
    
    return jsonify(site_settings_list_schema.dump(seo_settings))

@settings_bp.route('/', methods=['POST'])
def create_setting():
    """Create a new setting"""
    data = request.get_json()
    
    # Convert value to string based on type
    setting_value = data.get('value', '')
    setting_type = data.get('type', 'text')
    
    if setting_type == 'json' and isinstance(setting_value, (dict, list)):
        setting_value = json.dumps(setting_value)
    elif setting_type == 'boolean':
        setting_value = str(bool(setting_value)).lower()
    elif setting_type == 'number':
        setting_value = str(float(setting_value))
    else:
        setting_value = str(setting_value)
    
    setting = SiteSettings(
        setting_key=data['key'],
        setting_value=setting_value,
        setting_type=setting_type,
        description=data.get('description')
    )
    
    db.session.add(setting)
    db.session.commit()
    
    return jsonify(site_settings_schema.dump(setting)), 201

@settings_bp.route('/<setting_key>', methods=['PUT'])
def update_setting(setting_key):
    """Update an existing setting"""
    setting = SiteSettings.query.filter_by(setting_key=setting_key).first_or_404()
    data = request.get_json()
    
    # Convert value to string based on type
    if 'value' in data:
        setting_value = data['value']
        if setting.setting_type == 'json' and isinstance(setting_value, (dict, list)):
            setting.setting_value = json.dumps(setting_value)
        elif setting.setting_type == 'boolean':
            setting.setting_value = str(bool(setting_value)).lower()
        elif setting.setting_type == 'number':
            setting.setting_value = str(float(setting_value))
        else:
            setting.setting_value = str(setting_value)
    
    if 'description' in data:
        setting.description = data['description']
    
    db.session.commit()
    
    return jsonify(site_settings_schema.dump(setting))

@settings_bp.route('/<setting_key>', methods=['DELETE'])
def delete_setting(setting_key):
    """Delete a setting"""
    setting = SiteSettings.query.filter_by(setting_key=setting_key).first_or_404()
    db.session.delete(setting)
    db.session.commit()
    
    return jsonify({'message': f'Setting {setting_key} deleted successfully'}), 200
