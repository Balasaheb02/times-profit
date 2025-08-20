import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Author, Category, Tag, Article
from datetime import datetime, timedelta
import uuid

def add_more_dummy_data():
    """Add more comprehensive dummy data"""
    app = create_app()
    
    with app.app_context():
        print("Adding more dummy data...")
        
        # Add more authors
        existing_authors = Author.query.count()
        if existing_authors < 10:
            new_authors = [
                Author(
                    name="Alice Chen",
                    email="alice@example.com",
                    bio="AI Research Scientist and technology enthusiast",
                    avatar_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="David Rodriguez",
                    email="david@example.com",
                    bio="Sports journalist covering international football",
                    avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Emma Thompson",
                    email="emma@example.com",
                    bio="Business reporter specializing in startups and tech",
                    avatar_url="https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Robert Kim",
                    email="robert@example.com",
                    bio="Science correspondent and climate change expert",
                    avatar_url="https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Sarah Wilson",
                    email="sarah@example.com",
                    bio="Entertainment journalist and film critic",
                    avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=face"
                ),
                Author(
                    name="Marcus Johnson",
                    email="marcus@example.com",
                    bio="Political analyst and policy researcher",
                    avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face"
                )
            ]
            
            for author in new_authors:
                db.session.add(author)
            db.session.commit()
            print(f"Added {len(new_authors)} new authors")
        
        # Add more tags
        existing_tags = Tag.query.count()
        if existing_tags < 20:
            new_tags = [
                Tag(name="Blockchain", slug="blockchain"),
                Tag(name="Cryptocurrency", slug="cryptocurrency"),
                Tag(name="Climate Change", slug="climate-change"),
                Tag(name="Space", slug="space"),
                Tag(name="Health", slug="health"),
                Tag(name="Innovation", slug="innovation"),
                Tag(name="Startup", slug="startup"),
                Tag(name="Mobile", slug="mobile"),
                Tag(name="Gaming", slug="gaming"),
                Tag(name="Fashion", slug="fashion"),
                Tag(name="Travel", slug="travel"),
                Tag(name="Food", slug="food"),
                Tag(name="Education", slug="education"),
                Tag(name="Finance", slug="finance"),
                Tag(name="Security", slug="security")
            ]
            
            for tag in new_tags:
                if not Tag.query.filter_by(slug=tag.slug).first():
                    db.session.add(tag)
            db.session.commit()
            print(f"Added new tags")
        
        # Get all data for creating articles
        authors = Author.query.all()
        categories = Category.query.all()
        tags = Tag.query.all()
        
        # Add more articles
        existing_articles = Article.query.count()
        if existing_articles < 20:
            new_articles = [
                Article(
                    title="The Future of Artificial Intelligence in 2025",
                    slug="future-artificial-intelligence-2025",
                    content="""
                    <h2>AI Developments Shaping Tomorrow</h2>
                    <p>Artificial Intelligence continues to evolve at an unprecedented pace. In 2025, we're witnessing breakthrough developments in machine learning, natural language processing, and computer vision.</p>
                    
                    <h3>Key Advancements</h3>
                    <ul>
                        <li>Large Language Models becoming more efficient</li>
                        <li>AI integration in everyday applications</li>
                        <li>Ethical AI development practices</li>
                        <li>Autonomous systems reaching new capabilities</li>
                    </ul>
                    
                    <h3>Industry Impact</h3>
                    <p>From healthcare to finance, AI is transforming industries by automating complex tasks and providing insights that were previously impossible to obtain.</p>
                    
                    <p>The future looks promising as AI becomes more accessible and democratized, enabling smaller companies and developers to leverage powerful AI capabilities.</p>
                    """,
                    excerpt="Exploring the latest AI developments and their impact on various industries in 2025.",
                    image_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop",
                    image_alt="Artificial Intelligence concept visualization",
                    is_published=True,
                    views=2840,
                    author_id=authors[0].id,
                    category_id=categories[0].id,  # Technology
                    published_at=datetime.utcnow() - timedelta(hours=2)
                ),
                Article(
                    title="Climate Summit 2025: Global Leaders Unite for Action",
                    slug="climate-summit-2025-global-leaders-unite",
                    content="""
                    <h2>Historic Climate Agreement Reached</h2>
                    <p>World leaders gathered at the Climate Summit 2025 have reached a groundbreaking agreement on carbon reduction targets and renewable energy initiatives.</p>
                    
                    <h3>Key Outcomes</h3>
                    <ul>
                        <li>50% carbon reduction by 2030</li>
                        <li>$500 billion renewable energy fund</li>
                        <li>Technology sharing agreements</li>
                        <li>Forest conservation protocols</li>
                    </ul>
                    
                    <h3>Implementation Timeline</h3>
                    <p>The agreement includes specific milestones and accountability measures to ensure countries meet their commitments.</p>
                    
                    <p>Environmental groups have praised the comprehensive nature of the agreement, while industry leaders are already planning implementation strategies.</p>
                    """,
                    excerpt="World leaders reach historic climate agreement with ambitious carbon reduction targets.",
                    image_url="https://images.unsplash.com/photo-1569163139394-de4e4f43e4e5?w=800&h=400&fit=crop",
                    image_alt="Climate summit conference",
                    is_published=True,
                    views=1920,
                    author_id=authors[3].id,
                    category_id=categories[2].id,  # Politics
                    published_at=datetime.utcnow() - timedelta(hours=5)
                ),
                Article(
                    title="Quantum Computing Breakthrough: IBM Announces 1000-Qubit Processor",
                    slug="quantum-computing-breakthrough-ibm-1000-qubit",
                    content="""
                    <h2>Revolutionary Quantum Processor Unveiled</h2>
                    <p>IBM has successfully developed and tested a 1000-qubit quantum processor, marking a significant milestone in quantum computing advancement.</p>
                    
                    <h3>Technical Achievements</h3>
                    <ul>
                        <li>1000+ stable qubits</li>
                        <li>Improved error correction</li>
                        <li>Enhanced quantum coherence</li>
                        <li>Scalable architecture design</li>
                    </ul>
                    
                    <h3>Practical Applications</h3>
                    <p>This breakthrough opens doors for complex problem-solving in cryptography, drug discovery, financial modeling, and climate simulation.</p>
                    
                    <p>Industry experts predict this could accelerate the timeline for practical quantum computing applications by several years.</p>
                    """,
                    excerpt="IBM's new 1000-qubit processor represents a major leap forward in quantum computing capabilities.",
                    image_url="https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop",
                    image_alt="Quantum computing laboratory",
                    is_published=True,
                    views=3150,
                    author_id=authors[0].id,
                    category_id=categories[4].id,  # Science
                    published_at=datetime.utcnow() - timedelta(hours=8)
                ),
                Article(
                    title="World Cup 2025: Upsets and Surprises in Opening Week",
                    slug="world-cup-2025-upsets-surprises-opening-week",
                    content="""
                    <h2>Unexpected Results Shake Tournament</h2>
                    <p>The opening week of World Cup 2025 has delivered shocking upsets and memorable performances that have redefined tournament predictions.</p>
                    
                    <h3>Major Upsets</h3>
                    <ul>
                        <li>Defending champions defeated 3-1 by underdogs</li>
                        <li>Record-breaking goal scored in 12 seconds</li>
                        <li>First-time qualifier reaches knockout stage</li>
                        <li>Veteran player scores hat-trick at age 38</li>
                    </ul>
                    
                    <h3>Tournament Highlights</h3>
                    <p>Fans worldwide have been treated to exceptional football, with several matches already being called classics.</p>
                    
                    <p>The tournament's new format has created more competitive balance, leading to these surprising results.</p>
                    """,
                    excerpt="World Cup 2025 delivers shocking upsets and memorable moments in its opening week.",
                    image_url="https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=800&h=400&fit=crop",
                    image_alt="Football stadium during World Cup",
                    is_published=True,
                    views=4200,
                    author_id=authors[1].id,
                    category_id=categories[1].id,  # Sports
                    published_at=datetime.utcnow() - timedelta(hours=12)
                ),
                Article(
                    title="Electric Vehicle Sales Surge 300% as Infrastructure Expands",
                    slug="electric-vehicle-sales-surge-300-percent",
                    content="""
                    <h2>EV Revolution Gains Momentum</h2>
                    <p>Electric vehicle sales have surged 300% this year as charging infrastructure expands and battery technology improves significantly.</p>
                    
                    <h3>Market Drivers</h3>
                    <ul>
                        <li>Government incentives and subsidies</li>
                        <li>Rapid expansion of charging networks</li>
                        <li>Improved battery range and efficiency</li>
                        <li>Competitive pricing with traditional vehicles</li>
                    </ul>
                    
                    <h3>Industry Response</h3>
                    <p>Major automakers are accelerating their electric vehicle programs, with several announcing complete transitions to electric by 2030.</p>
                    
                    <p>The shift represents a fundamental change in the automotive industry and transportation sector.</p>
                    """,
                    excerpt="Electric vehicle adoption accelerates with 300% sales increase driven by infrastructure and technology improvements.",
                    image_url="https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=800&h=400&fit=crop",
                    image_alt="Electric vehicle charging station",
                    is_published=True,
                    views=2650,
                    author_id=authors[2].id,
                    category_id=categories[5].id,  # Business
                    published_at=datetime.utcnow() - timedelta(hours=18)
                ),
                Article(
                    title="New Treatment Shows Promise for Alzheimer's Disease",
                    slug="new-alzheimer-treatment-shows-promise",
                    content="""
                    <h2>Medical Breakthrough Offers Hope</h2>
                    <p>Researchers have developed a promising new treatment for Alzheimer's disease that shows significant improvement in clinical trials.</p>
                    
                    <h3>Clinical Trial Results</h3>
                    <ul>
                        <li>65% of patients showed cognitive improvement</li>
                        <li>Minimal side effects observed</li>
                        <li>Treatment targets root causes</li>
                        <li>Potential for early intervention</li>
                    </ul>
                    
                    <h3>Next Steps</h3>
                    <p>The treatment is moving to Phase III trials with hopes for FDA approval within two years.</p>
                    
                    <p>This breakthrough could transform the lives of millions of patients and families affected by Alzheimer's disease.</p>
                    """,
                    excerpt="New Alzheimer's treatment shows remarkable results in clinical trials, offering hope for millions.",
                    image_url="https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&h=400&fit=crop",
                    image_alt="Medical research laboratory",
                    is_published=True,
                    views=1800,
                    author_id=authors[3].id,
                    category_id=categories[4].id,  # Science
                    published_at=datetime.utcnow() - timedelta(days=1)
                ),
                Article(
                    title="Mars Mission 2025: Successful Landing Opens New Chapter",
                    slug="mars-mission-2025-successful-landing",
                    content="""
                    <h2>Historic Achievement in Space Exploration</h2>
                    <p>The Mars Mission 2025 has successfully landed on the Red Planet, marking humanity's most ambitious space exploration achievement to date.</p>
                    
                    <h3>Mission Objectives</h3>
                    <ul>
                        <li>Search for signs of past or present life</li>
                        <li>Collect soil and rock samples</li>
                        <li>Study atmospheric conditions</li>
                        <li>Test technologies for future human missions</li>
                    </ul>
                    
                    <h3>Advanced Technology</h3>
                    <p>The mission features cutting-edge rovers, drilling equipment, and communication systems that will operate for the next two years.</p>
                    
                    <p>This success paves the way for future human missions to Mars, potentially within the next decade.</p>
                    """,
                    excerpt="Mars Mission 2025 achieves successful landing, opening new possibilities for space exploration.",
                    image_url="https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=400&fit=crop",
                    image_alt="Mars surface exploration",
                    is_published=True,
                    views=5200,
                    author_id=authors[3].id,
                    category_id=categories[4].id,  # Science
                    published_at=datetime.utcnow() - timedelta(days=2)
                ),
                Article(
                    title="Streaming Wars Heat Up as New Platform Launches",
                    slug="streaming-wars-new-platform-launches",
                    content="""
                    <h2>Entertainment Industry Disruption Continues</h2>
                    <p>A new streaming platform has entered the competitive market with exclusive content and innovative features, intensifying the streaming wars.</p>
                    
                    <h3>Platform Features</h3>
                    <ul>
                        <li>AI-powered content recommendations</li>
                        <li>Interactive viewing experiences</li>
                        <li>Exclusive original programming</li>
                        <li>Multi-device synchronization</li>
                    </ul>
                    
                    <h3>Market Impact</h3>
                    <p>The launch has prompted existing platforms to enhance their offerings and competitive pricing strategies.</p>
                    
                    <p>Consumers benefit from increased choice and innovation in the rapidly evolving entertainment landscape.</p>
                    """,
                    excerpt="New streaming platform enters the market with innovative features, intensifying competition.",
                    image_url="https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=800&h=400&fit=crop",
                    image_alt="Streaming entertainment setup",
                    is_published=True,
                    views=1450,
                    author_id=authors[4].id,
                    category_id=categories[3].id,  # Entertainment
                    published_at=datetime.utcnow() - timedelta(days=3)
                )
            ]
            
            for article in new_articles:
                db.session.add(article)
            db.session.commit()
            
            # Add tags to articles
            article_list = Article.query.filter(Article.title.in_([a.title for a in new_articles])).all()
            for i, article in enumerate(article_list):
                if i == 0:  # AI article
                    article.tags.extend([tags[0], tags[1], tags[15]])  # AI, Machine Learning, Innovation
                elif i == 1:  # Climate article
                    article.tags.extend([tags[12]])  # Climate Change
                elif i == 2:  # Quantum article
                    article.tags.extend([tags[0], tags[15], tags[24]])  # AI, Innovation, Security
                elif i == 3:  # Sports article
                    article.tags.extend([tags[6]])  # Breaking News
                elif i == 4:  # EV article
                    article.tags.extend([tags[16], tags[15]])  # Startup, Innovation
                elif i == 5:  # Alzheimer article
                    article.tags.extend([tags[14]])  # Health
                elif i == 6:  # Mars article
                    article.tags.extend([tags[13], tags[15]])  # Space, Innovation
                elif i == 7:  # Streaming article
                    article.tags.extend([tags[18]])  # Gaming (entertainment related)
            
            db.session.commit()
            print(f"Added {len(new_articles)} new articles with tags")
        
        print("\nDummy data addition completed successfully!")
        print(f"Total Authors: {Author.query.count()}")
        print(f"Total Categories: {Category.query.count()}")
        print(f"Total Tags: {Tag.query.count()}")
        print(f"Total Articles: {Article.query.count()}")

if __name__ == "__main__":
    add_more_dummy_data()
