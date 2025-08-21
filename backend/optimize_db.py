#!/usr/bin/env python3
"""
Database optimization script to add indexes and improve query performance
"""

import os
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import create_app, db
from sqlalchemy import text

def add_database_indexes():
    """Add indexes to improve query performance"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Adding database indexes for better performance...")
            
            # Create indexes for Articles table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_published_at 
                ON articles(published_at DESC)
            """))
            
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_status 
                ON articles(status)
            """))
            
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_category_id 
                ON articles(category_id)
            """))
            
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_author_id 
                ON articles(author_id)
            """))
            
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_slug 
                ON articles(slug)
            """))
            
            db.session.commit()
            print("✅ All database indexes created successfully!")
            
            # Get actual row counts
            tables = ['articles', 'categories', 'authors']
            
            for table in tables:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"  📋 {table}: {count} rows")
                except Exception as e:
                    print(f"  ⚠️ {table}: Could not count rows - {e}")
            
            print("\n🎉 Database optimization completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during optimization: {e}")
            db.session.rollback()
            return False
        
        return True

if __name__ == "__main__":
    success = add_database_indexes()
    if success:
        print("\n🚀 Your database is now optimized for production!")
    else:
        print("\n💥 Optimization failed. Please check the errors above.")
        sys.exit(1)
