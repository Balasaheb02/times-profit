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
            
            # Create indexes for Categories table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_categories_slug 
                ON categories(slug)
            """))
            
            # Create indexes for Authors table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_authors_slug 
                ON authors(slug)
            """))
            
            # Create indexes for Quizzes table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_quizzes_published_at 
                ON quizzes(created_at DESC)
            """))
            
            # Create indexes for Questions table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_questions_quiz_id 
                ON questions(quiz_id)
            """))
            
            # Create indexes for Answers table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_answers_question_id 
                ON answers(question_id)
            """))
            
            # Create indexes for Pages table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_pages_slug 
                ON pages(slug)
            """))
            
            # Create indexes for Menu Items table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_menu_items_parent_id 
                ON menu_items(parent_id)
            """))
            
            # Create indexes for Stock Quotes table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_stock_quotes_symbol 
                ON stock_quotes(symbol)
            """))
            
            # Create indexes for Site Settings table
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_site_settings_key 
                ON site_settings("key")
            """))
            
            # Composite indexes for common queries
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_articles_status_published_at 
                ON articles(status, published_at DESC)
            """))
            
            db.session.commit()
            print("✅ All database indexes created successfully!")
            
            # Get table row counts
            tables = ['articles', 'categories', 'authors', 'quizzes', 'questions', 
                     'answers', 'pages', 'menu_items', 'stock_quotes', 'site_settings']
            
            print("\n📊 Database Statistics:")
            for table in tables:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"  📋 {table}: {count} rows")
                except Exception as e:
                    print(f"  ⚠️ {table}: Could not count rows - {e}")
            
            # Test query performance
            print("\n⚡ Testing query performance...")
            
            # Test article queries
            import time
            
            start_time = time.time()
            try:
                result = db.session.execute(text("""
                    SELECT a.*, c.name as category_name, au.name as author_name
                    FROM articles a
                    LEFT JOIN categories c ON a.category_id = c.id
                    LEFT JOIN authors au ON a.author_id = au.id
                    WHERE a.status = 'published'
                    ORDER BY a.published_at DESC
                    LIMIT 10
                """))
                articles = result.fetchall()
                end_time = time.time()
                
                print(f"  ✅ Article query with joins: {(end_time - start_time)*1000:.2f}ms ({len(articles)} results)")
            except Exception as e:
                print(f"  ❌ Article query failed: {e}")
            
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
        print("📈 Expected performance improvements:")
        print("  • Faster article queries by category/author")
        print("  • Improved pagination performance") 
        print("  • Optimized search by slug")
        print("  • Better quiz and page loading times")
    else:
        print("\n💥 Database optimization failed!")
