#!/usr/bin/env python3

# Diagnostic script to check Flask app configuration
# Run this on your VPS in the backend directory

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, '/home/newsapp/times-profit/backend')

try:
    # Import the Flask app
    from app import create_app
    
    print("🔍 Flask App Diagnostic")
    print("━" * 50)
    
    # Create app instance
    app = create_app()
    
    print("✅ Flask app created successfully")
    print(f"📱 App name: {app.name}")
    print(f"🔧 Config: {app.config.get('ENV', 'unknown')}")
    
    # Check registered blueprints
    print("\n📋 Registered Blueprints:")
    for blueprint_name, blueprint in app.blueprints.items():
        print(f"   {blueprint_name}: {blueprint.url_prefix or '/'}")
    
    # Check if db_admin blueprint is registered
    if 'db_admin' in app.blueprints:
        print("\n✅ db_admin blueprint is registered!")
        
        # Check routes
        print("\n🔗 Database Admin Routes:")
        with app.app_context():
            for rule in app.url_map.iter_rules():
                if 'admin' in rule.rule:
                    print(f"   {rule.methods} {rule.rule}")
    else:
        print("\n❌ db_admin blueprint is NOT registered!")
        print("   Available blueprints:", list(app.blueprints.keys()))
    
    # Test database connection
    print("\n🗄️  Testing Database Connection:")
    try:
        from app import db
        with app.app_context():
            result = db.session.execute("SELECT 1").fetchone()
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    print("\n🎯 If db_admin blueprint is missing, restart the service:")
    print("   sudo systemctl restart newsapp")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the correct directory and virtual environment is activated")
except Exception as e:
    print(f"❌ Error: {e}")
