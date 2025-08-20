#!/usr/bin/env python
import os
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Author, Category, Tag, Article

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Author': Author, 'Category': Category, 'Tag': Tag, 'Article': Article}

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Create database tables
    db.create_all()

    # Create some sample data
    create_sample_data()

def create_sample_data():
    """Create sample data for testing"""
    # Create sample author
    if not Author.query.first():
        author = Author(
            name="John Doe",
            email="john@example.com",
            bio="Tech writer and blogger",
            avatar_url="https://example.com/avatar.jpg"
        )
        db.session.add(author)
    
    # Create sample categories
    if not Category.query.first():
        categories = [
            Category(name="Technology", slug="technology", description="Latest in tech"),
            Category(name="Sports", slug="sports", description="Sports news and updates"),
            Category(name="Politics", slug="politics", description="Political news"),
            Category(name="Entertainment", slug="entertainment", description="Entertainment news")
        ]
        for category in categories:
            db.session.add(category)
    
    # Create sample tags
    if not Tag.query.first():
        tags = [
            Tag(name="AI", slug="ai"),
            Tag(name="Web Development", slug="web-development"),
            Tag(name="Python", slug="python"),
            Tag(name="React", slug="react"),
            Tag(name="Next.js", slug="nextjs")
        ]
        for tag in tags:
            db.session.add(tag)
    
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == '__main__':
    app.run()
