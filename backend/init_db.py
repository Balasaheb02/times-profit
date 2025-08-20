import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Author, Category, Tag, Article
from datetime import datetime
import uuid

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create sample authors
        if Author.query.count() == 0:
            authors = [
                Author(
                    name="John Doe",
                    email="john@example.com",
                    bio="Senior Technology Writer with 10+ years of experience",
                    avatar_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Jane Smith",
                    email="jane@example.com",
                    bio="Sports journalist and former Olympic athlete",
                    avatar_url="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Mike Johnson",
                    email="mike@example.com",
                    bio="Political correspondent and policy analyst",
                    avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face"
                )
            ]
            
            for author in authors:
                db.session.add(author)
            db.session.commit()
            print(f"Created {len(authors)} sample authors")
        
        # Create sample categories
        if Category.query.count() == 0:
            categories = [
                Category(name="Technology", slug="technology", description="Latest technology news and updates"),
                Category(name="Sports", slug="sports", description="Sports news, scores, and analysis"),
                Category(name="Politics", slug="politics", description="Political news and government updates"),
                Category(name="Entertainment", slug="entertainment", description="Entertainment news and celebrity updates"),
                Category(name="Science", slug="science", description="Scientific discoveries and research"),
                Category(name="Business", slug="business", description="Business news and market updates")
            ]
            
            for category in categories:
                db.session.add(category)
            db.session.commit()
            print(f"Created {len(categories)} sample categories")
        
        # Create sample tags
        if Tag.query.count() == 0:
            tags = [
                Tag(name="AI", slug="ai"),
                Tag(name="Machine Learning", slug="machine-learning"),
                Tag(name="Web Development", slug="web-development"),
                Tag(name="Python", slug="python"),
                Tag(name="React", slug="react"),
                Tag(name="Next.js", slug="nextjs"),
                Tag(name="Breaking News", slug="breaking-news"),
                Tag(name="Analysis", slug="analysis"),
                Tag(name="Interview", slug="interview"),
                Tag(name="Review", slug="review")
            ]
            
            for tag in tags:
                db.session.add(tag)
            db.session.commit()
            print(f"Created {len(tags)} sample tags")
        
        # Create sample articles
        if Article.query.count() == 0:
            # Get created data for references
            authors = Author.query.all()
            categories = Category.query.all()
            tags = Tag.query.all()
            
            articles = [
                Article(
                    title="Revolutionary AI Technology Transforms Healthcare",
                    slug="revolutionary-ai-technology-transforms-healthcare",
                    content="""
                    <h2>Breakthrough in Medical AI</h2>
                    <p>Scientists have developed a groundbreaking artificial intelligence system that can diagnose diseases with unprecedented accuracy. This revolutionary technology promises to transform healthcare delivery worldwide.</p>
                    
                    <h3>Key Features</h3>
                    <ul>
                        <li>99.8% diagnostic accuracy</li>
                        <li>Real-time analysis capabilities</li>
                        <li>Integration with existing medical systems</li>
                        <li>Cost-effective implementation</li>
                    </ul>
                    
                    <p>The system has been tested in over 100 hospitals worldwide and has shown remarkable results in early disease detection and treatment planning.</p>
                    """,
                    excerpt="Scientists unveil AI system with 99.8% diagnostic accuracy, revolutionizing healthcare delivery.",
                    image_url="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=400&fit=crop",
                    image_alt="AI technology in healthcare",
                    is_published=True,
                    views=1250,
                    author_id=authors[0].id,
                    category_id=categories[0].id,  # Technology
                    published_at=datetime.utcnow()
                ),
                Article(
                    title="Championship Finals: Record-Breaking Performance",
                    slug="championship-finals-record-breaking-performance",
                    content="""
                    <h2>Historic Championship Victory</h2>
                    <p>In a thrilling final match, the championship saw record-breaking performances that will be remembered for years to come.</p>
                    
                    <h3>Game Highlights</h3>
                    <p>The final quarter was particularly intense, with both teams displaying exceptional skill and determination. The winning goal came in the last two minutes, securing a 3-2 victory.</p>
                    
                    <h3>Player Statistics</h3>
                    <p>Several players achieved personal bests during the championship, with the MVP scoring a tournament-record 25 points.</p>
                    """,
                    excerpt="Championship finals deliver record-breaking performances in thrilling 3-2 victory.",
                    image_url="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=400&fit=crop",
                    image_alt="Championship sports event",
                    is_published=True,
                    views=890,
                    author_id=authors[1].id,
                    category_id=categories[1].id,  # Sports
                    published_at=datetime.utcnow()
                ),
                Article(
                    title="New Climate Policy Aims to Reduce Emissions by 50%",
                    slug="new-climate-policy-reduce-emissions-50-percent",
                    content="""
                    <h2>Ambitious Climate Legislation</h2>
                    <p>Government announces comprehensive climate policy targeting 50% emission reduction over the next decade.</p>
                    
                    <h3>Policy Details</h3>
                    <ul>
                        <li>Renewable energy incentives</li>
                        <li>Carbon tax implementation</li>
                        <li>Green technology investments</li>
                        <li>International cooperation agreements</li>
                    </ul>
                    
                    <p>Environmental groups have praised the initiative while industry leaders express mixed reactions to the proposed changes.</p>
                    """,
                    excerpt="Government unveils climate policy targeting 50% emission reduction through renewable energy and carbon taxation.",
                    image_url="https://images.unsplash.com/photo-1569163139394-de4e4f43e4e5?w=800&h=400&fit=crop",
                    image_alt="Climate policy and environment",
                    is_published=True,
                    views=670,
                    author_id=authors[2].id,
                    category_id=categories[2].id,  # Politics
                    published_at=datetime.utcnow()
                ),
                Article(
                    title="Next.js 14 Released with Revolutionary App Router",
                    slug="nextjs-14-released-revolutionary-app-router",
                    content="""
                    <h2>Next.js 14: A Game Changer</h2>
                    <p>The latest version of Next.js introduces significant improvements to performance and developer experience.</p>
                    
                    <h3>New Features</h3>
                    <ul>
                        <li>Enhanced App Router with server components</li>
                        <li>Improved build performance</li>
                        <li>Better TypeScript support</li>
                        <li>Advanced caching mechanisms</li>
                    </ul>
                    
                    <p>Developers worldwide are already migrating to take advantage of these powerful new features.</p>
                    """,
                    excerpt="Next.js 14 introduces enhanced App Router and improved performance for modern web development.",
                    image_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop",
                    image_alt="Web development and coding",
                    is_published=True,
                    views=2100,
                    author_id=authors[0].id,
                    category_id=categories[0].id,  # Technology
                    published_at=datetime.utcnow()
                )
            ]
            
            for article in articles:
                db.session.add(article)
            db.session.commit()
            
            # Add tags to articles
            articles[0].tags.extend([tags[0], tags[1]])  # AI, Machine Learning
            articles[1].tags.extend([tags[6], tags[7]])  # Breaking News, Analysis
            articles[2].tags.extend([tags[6], tags[7]])  # Breaking News, Analysis
            articles[3].tags.extend([tags[2], tags[4], tags[5]])  # Web Development, React, Next.js
            
            db.session.commit()
            print(f"Created {len(articles)} sample articles with tags")
        
        print("\nDatabase initialization completed successfully!")
        print("You can now start the Flask backend with: python run.py")

if __name__ == "__main__":
    init_database()
