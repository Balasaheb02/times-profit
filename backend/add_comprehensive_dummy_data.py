#!/usr/bin/env python3
"""
Extended dummy data generator for the Flask backend
Adds 20+ entries for each entity type including quizzes, pages, menu items, stocks, and settings
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    Article, Author, Category, Tag, User, article_tags,
    Quiz, Question, Answer, Page, MenuItem, StockQuote, SiteSettings
)
from datetime import datetime, timedelta
import uuid
import json

def create_dummy_data():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()
        
        print("Creating comprehensive dummy data...")
        
        # Create Authors (20)
        authors = []
        author_data = [
            ("John Smith", "john.smith@news.com", "Senior tech journalist with 10+ years experience", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"),
            ("Sarah Johnson", "sarah.j@news.com", "Breaking news specialist covering global events", "https://images.unsplash.com/photo-1494790108755-2616b612b8bd?w=150"),
            ("Mike Chen", "mike.chen@news.com", "Sports correspondent and former athlete", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"),
            ("Emily Davis", "emily.davis@news.com", "Business and finance reporter", "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150"),
            ("Robert Wilson", "robert.w@news.com", "Political analyst and investigative journalist", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"),
            ("Lisa Garcia", "lisa.garcia@news.com", "Health and science writer", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150"),
            ("David Brown", "david.brown@news.com", "Entertainment and culture critic", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150"),
            ("Jessica Lee", "jessica.lee@news.com", "Environmental and climate change reporter", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150"),
            ("Mark Thompson", "mark.t@news.com", "Automotive and technology specialist", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"),
            ("Amanda Rodriguez", "amanda.r@news.com", "Fashion and lifestyle correspondent", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150"),
            ("Kevin Park", "kevin.park@news.com", "Cryptocurrency and fintech expert", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"),
            ("Rachel Green", "rachel.green@news.com", "Food and travel writer", "https://images.unsplash.com/photo-1494790108755-2616b612b8bd?w=150"),
            ("Steven Clark", "steven.clark@news.com", "Gaming and esports journalist", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"),
            ("Natalie White", "natalie.white@news.com", "Education and social policy reporter", "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150"),
            ("Jason Martinez", "jason.m@news.com", "Real estate and urban development specialist", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"),
            ("Nicole Adams", "nicole.adams@news.com", "AI and machine learning correspondent", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150"),
            ("Tom Johnson", "tom.johnson@news.com", "Space and astronomy writer", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150"),
            ("Linda Taylor", "linda.taylor@news.com", "Legal affairs and court reporter", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150"),
            ("Chris Anderson", "chris.anderson@news.com", "International affairs correspondent", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"),
            ("Maria Lopez", "maria.lopez@news.com", "Art and museum curator turned journalist", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150")
        ]
        
        for name, email, bio, avatar in author_data:
            author = Author(
                name=name,
                email=email,
                bio=bio,
                avatar_url=avatar
            )
            authors.append(author)
            db.session.add(author)
        
        # Create Categories (20)
        categories = []
        category_data = [
            ("Technology", "technology", "Latest tech news, gadgets, and innovations"),
            ("Business", "business", "Financial markets, startups, and corporate news"),
            ("Sports", "sports", "Sports news, scores, and athlete profiles"),
            ("Politics", "politics", "Political developments and government updates"),
            ("Health", "health", "Medical breakthroughs and wellness tips"),
            ("Science", "science", "Scientific discoveries and research"),
            ("Entertainment", "entertainment", "Movies, TV shows, and celebrity news"),
            ("Environment", "environment", "Climate change and environmental issues"),
            ("Automotive", "automotive", "Car reviews and automotive industry news"),
            ("Fashion", "fashion", "Fashion trends and style guides"),
            ("Food", "food", "Recipes, restaurant reviews, and culinary trends"),
            ("Travel", "travel", "Travel guides and destination reviews"),
            ("Gaming", "gaming", "Video game news and reviews"),
            ("Education", "education", "Educational policy and learning innovations"),
            ("Real Estate", "real-estate", "Property market and housing trends"),
            ("Cryptocurrency", "cryptocurrency", "Digital currency and blockchain news"),
            ("Artificial Intelligence", "artificial-intelligence", "AI developments and machine learning"),
            ("Space", "space", "Space exploration and astronomy"),
            ("Legal", "legal", "Legal developments and court cases"),
            ("Art", "art", "Art exhibitions and cultural events")
        ]
        
        for name, slug, description in category_data:
            category = Category(
                name=name,
                slug=slug,
                description=description
            )
            categories.append(category)
            db.session.add(category)
        
        # Create Tags (25)
        tags = []
        tag_names = [
            "breaking-news", "trending", "featured", "exclusive", "analysis",
            "interview", "review", "guide", "tutorial", "opinion",
            "investigation", "update", "announcement", "launch", "development",
            "research", "study", "report", "innovation", "breakthrough",
            "controversy", "debate", "emergency", "alert", "milestone"
        ]
        
        for tag_name in tag_names:
            tag = Tag(
                name=tag_name.replace('-', ' ').title(),
                slug=tag_name
            )
            tags.append(tag)
            db.session.add(tag)
        
        db.session.commit()
        
        # Create Articles (25)
        article_data = [
            ("Next.js 14 Released: Revolutionary App Router", "nextjs-14-released-revolutionary-app-router", """
            <h2>Revolutionary Changes in Next.js 14</h2>
            <p>The latest version of Next.js brings groundbreaking improvements to the App Router, making it faster and more intuitive for developers.</p>
            <h3>Key Features</h3>
            <ul>
            <li>Enhanced performance with Turbopack</li>
            <li>Improved Server Components</li>
            <li>Better TypeScript support</li>
            <li>Advanced caching mechanisms</li>
            </ul>
            <p>These updates represent a significant leap forward in React-based web development.</p>
            """, "Next.js 14 introduces major improvements to the App Router with enhanced performance and developer experience.", "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800", "Next.js 14 App Router"),
            
            ("AI Revolution: ChatGPT-5 Leaked Features", "ai-revolution-chatgpt-5-leaked-features", """
            <h2>The Future of AI Conversation</h2>
            <p>Leaked information suggests ChatGPT-5 will feature multimodal capabilities, real-time learning, and unprecedented reasoning abilities.</p>
            <h3>Expected Improvements</h3>
            <ul>
            <li>Video and audio understanding</li>
            <li>Real-time web browsing</li>
            <li>Enhanced coding capabilities</li>
            <li>Emotional intelligence</li>
            </ul>
            <p>These features could revolutionize how we interact with AI systems.</p>
            """, "Exclusive leak reveals ChatGPT-5's groundbreaking features that could change AI forever.", "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800", "AI Robot"),
            
            ("Stock Market Soars: Tech Giants Lead Rally", "stock-market-soars-tech-giants-lead-rally", """
            <h2>Market Recovery Continues</h2>
            <p>Technology stocks led a broad market rally today, with major indices posting significant gains.</p>
            <h3>Top Performers</h3>
            <ul>
            <li>Apple (AAPL): +5.2%</li>
            <li>Microsoft (MSFT): +4.8%</li>
            <li>Google (GOOGL): +6.1%</li>
            <li>Tesla (TSLA): +7.3%</li>
            </ul>
            <p>Analysts cite strong earnings and positive economic indicators as key drivers.</p>
            """, "Technology stocks surge as investors show renewed confidence in the sector.", "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800", "Stock market charts"),
            
            ("Climate Change: Arctic Ice Hits Record Low", "climate-change-arctic-ice-record-low", """
            <h2>Alarming Environmental Data</h2>
            <p>New satellite data reveals Arctic sea ice has reached its lowest level since records began, raising urgent climate concerns.</p>
            <h3>Key Statistics</h3>
            <ul>
            <li>15% below historical average</li>
            <li>Fastest decline rate recorded</li>
            <li>Impact on global weather patterns</li>
            <li>Threat to Arctic wildlife</li>
            </ul>
            <p>Scientists call for immediate action to address climate change.</p>
            """, "Arctic sea ice reaches record low levels, highlighting urgent need for climate action.", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800", "Arctic ice"),
            
            ("Space Breakthrough: Mars Colony Plans Revealed", "space-breakthrough-mars-colony-plans-revealed", """
            <h2>Humanity's Next Giant Leap</h2>
            <p>SpaceX and NASA unveil detailed plans for the first permanent human settlement on Mars by 2030.</p>
            <h3>Mission Details</h3>
            <ul>
            <li>100-person initial colony</li>
            <li>Self-sustaining life support</li>
            <li>In-situ resource utilization</li>
            <li>Advanced transportation systems</li>
            </ul>
            <p>The project represents the largest space endeavor in human history.</p>
            """, "Ambitious plans for Mars colonization take shape with detailed timelines and technology roadmaps.", "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800", "Mars surface"),
            
            # Continue with 20 more articles...
            ("Quantum Computing: IBM's 1000-Qubit Milestone", "quantum-computing-ibm-1000-qubit-milestone", """
            <h2>Quantum Supremacy Achieved</h2>
            <p>IBM's latest quantum processor breaks the 1000-qubit barrier, opening new possibilities for computational science.</p>
            """, "IBM achieves quantum computing milestone with 1000-qubit processor.", "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800", "Quantum computer"),
            
            ("Electric Vehicle Sales Double in 2024", "electric-vehicle-sales-double-2024", """
            <h2>EV Revolution Accelerates</h2>
            <p>Global electric vehicle sales have doubled compared to last year, signaling a major shift in transportation.</p>
            """, "Electric vehicle adoption accelerates with sales doubling year-over-year.", "https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=800", "Electric car charging"),
            
            ("Breakthrough Gene Therapy Cures Blindness", "breakthrough-gene-therapy-cures-blindness", """
            <h2>Medical Miracle</h2>
            <p>Revolutionary gene therapy successfully restores sight to patients with inherited blindness.</p>
            """, "Gene therapy breakthrough offers hope for treating inherited blindness.", "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800", "Eye examination"),
            
            ("Cryptocurrency Market Reaches New Highs", "cryptocurrency-market-reaches-new-highs", """
            <h2>Digital Gold Rush</h2>
            <p>Bitcoin and other cryptocurrencies surge to record highs amid institutional adoption.</p>
            """, "Cryptocurrency market soars as institutional investors embrace digital assets.", "https://images.unsplash.com/photo-1605792657660-596af9009e82?w=800", "Bitcoin coin"),
            
            ("5G Network Coverage Reaches 80% Globally", "5g-network-coverage-reaches-80-globally", """
            <h2>Connectivity Revolution</h2>
            <p>Global 5G coverage reaches 80% milestone, enabling new technologies and applications.</p>
            """, "5G networks achieve 80% global coverage, accelerating digital transformation.", "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800", "5G tower"),
            
            ("Artificial Meat Industry Valued at $290 Billion", "artificial-meat-industry-290-billion", """
            <h2>Food Revolution</h2>
            <p>Lab-grown meat industry reaches massive valuation as consumers embrace sustainable alternatives.</p>
            """, "Lab-grown meat industry explodes to $290 billion valuation.", "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=800", "Lab grown meat"),
            
            ("Virtual Reality Transforms Education System", "virtual-reality-transforms-education", """
            <h2>Learning Revolution</h2>
            <p>VR technology revolutionizes classroom experiences with immersive educational content.</p>
            """, "Virtual reality technology transforms traditional education with immersive learning.", "https://images.unsplash.com/photo-1592478411213-6153e4ebc696?w=800", "VR headset"),
            
            ("Renewable Energy Surpasses Fossil Fuels", "renewable-energy-surpasses-fossil-fuels", """
            <h2>Green Energy Milestone</h2>
            <p>Renewable energy sources now generate more electricity than fossil fuels globally.</p>
            """, "Renewable energy achieves historic milestone, surpassing fossil fuel generation.", "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800", "Wind turbines"),
            
            ("Autonomous Vehicles Get Government Approval", "autonomous-vehicles-government-approval", """
            <h2>Self-Driving Future</h2>
            <p>Government approves fully autonomous vehicles for public roads nationwide.</p>
            """, "Autonomous vehicles receive government approval for nationwide deployment.", "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800", "Self driving car"),
            
            ("Brain-Computer Interface Clinical Trial Success", "brain-computer-interface-trial-success", """
            <h2>Mind-Machine Connection</h2>
            <p>Clinical trials show breakthrough results for brain-computer interface technology.</p>
            """, "Brain-computer interface trials show promising results for paralyzed patients.", "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800", "Brain scan"),
            
            ("Social Media Platforms Face Major Regulation", "social-media-platforms-major-regulation", """
            <h2>Digital Accountability</h2>
            <p>New regulations target social media platforms to improve user safety and data privacy.</p>
            """, "Social media companies face comprehensive new regulations for user protection.", "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800", "Social media icons"),
            
            ("Robotic Surgery Reduces Recovery Time by 70%", "robotic-surgery-reduces-recovery-time", """
            <h2>Medical Innovation</h2>
            <p>Advanced robotic surgery systems dramatically reduce patient recovery times and complications.</p>
            """, "Robotic surgery technology cuts patient recovery time by 70%.", "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800", "Surgical robot"),
            
            ("Vertical Farming Feeds Urban Populations", "vertical-farming-feeds-urban-populations", """
            <h2>Agricultural Revolution</h2>
            <p>Vertical farming technology provides sustainable food solutions for growing urban areas.</p>
            """, "Vertical farming emerges as solution for sustainable urban food production.", "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800", "Vertical farm"),
            
            ("Quantum Internet Connects Three Cities", "quantum-internet-connects-three-cities", """
            <h2>Ultra-Secure Communications</h2>
            <p>First quantum internet network successfully connects three major cities with unhackable communication.</p>
            """, "Quantum internet achieves milestone with three-city network connection.", "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800", "Quantum network"),
            
            ("DNA Storage Technology Stores Entire Internet", "dna-storage-technology-stores-internet", """
            <h2>Biological Data Storage</h2>
            <p>DNA storage breakthrough could store the entire internet in a space the size of a sugar cube.</p>
            """, "DNA storage technology could revolutionize data storage capacity.", "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800", "DNA helix"),
            
            ("Fusion Power Plant Generates Net Energy", "fusion-power-plant-generates-net-energy", """
            <h2>Clean Energy Breakthrough</h2>
            <p>First commercial fusion power plant achieves net energy gain, promising unlimited clean power.</p>
            """, "Fusion power achieves net energy gain milestone in clean energy breakthrough.", "https://images.unsplash.com/photo-1614837240775-5bbe4e4f94ed?w=800", "Fusion reactor"),
            
            ("Smart Cities Reduce Carbon Emissions by 50%", "smart-cities-reduce-carbon-emissions", """
            <h2>Urban Innovation</h2>
            <p>Smart city technologies help major metropolitan areas cut carbon emissions in half.</p>
            """, "Smart city initiatives achieve 50% reduction in urban carbon emissions.", "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800", "Smart city"),
            
            ("Personalized Medicine Based on DNA Analysis", "personalized-medicine-dna-analysis", """
            <h2>Precision Healthcare</h2>
            <p>Personalized medicine revolution uses DNA analysis to create targeted treatments for patients.</p>
            """, "DNA-based personalized medicine offers targeted treatments for individual patients.", "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800", "DNA analysis"),
            
            ("Space Elevator Project Receives Funding", "space-elevator-project-receives-funding", """
            <h2>Revolutionary Transportation</h2>
            <p>Multi-billion dollar space elevator project receives international funding approval.</p>
            """, "Space elevator project secures funding for revolutionary space transportation.", "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800", "Space elevator concept"),
            
            ("Holographic Displays Replace Traditional Screens", "holographic-displays-replace-screens", """
            <h2>Display Technology Revolution</h2>
            <p>Holographic display technology begins replacing traditional screens in consumer devices.</p>
            """, "Holographic displays emerge as the next generation of screen technology.", "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800", "Hologram display")
        ]
        
        for i, (title, slug, content, excerpt, image_url, image_alt) in enumerate(article_data):
            article = Article(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                image_url=image_url,
                image_alt=image_alt,
                published_at=datetime.utcnow() - timedelta(days=i),
                is_published=True,
                views=1000 - (i * 30),
                author_id=authors[i % len(authors)].id,
                category_id=categories[i % len(categories)].id
            )
            
            # Add random tags to articles
            import random
            num_tags = random.randint(2, 5)
            selected_tags = random.sample(tags, num_tags)
            article.tags = selected_tags
            
            db.session.add(article)
        
        db.session.commit()
        
        # Create Quizzes (20)
        quizzes = []
        quiz_data = [
            ("Technology Knowledge Quiz", "tech-knowledge-quiz", "Test your knowledge of the latest technology trends"),
            ("Business Fundamentals", "business-fundamentals", "Essential business concepts and practices"),
            ("Sports Trivia Challenge", "sports-trivia-challenge", "Ultimate sports knowledge test"),
            ("Science Discovery Quiz", "science-discovery-quiz", "Explore fascinating scientific discoveries"),
            ("World Politics Quiz", "world-politics-quiz", "Test your political knowledge"),
            ("Health and Wellness", "health-wellness-quiz", "Health tips and medical knowledge"),
            ("Environmental Awareness", "environmental-awareness", "Climate and environmental quiz"),
            ("Space Exploration", "space-exploration-quiz", "Journey through space knowledge"),
            ("Artificial Intelligence", "ai-knowledge-quiz", "AI and machine learning concepts"),
            ("Cryptocurrency Basics", "crypto-basics-quiz", "Digital currency fundamentals"),
            ("History Champions", "history-champions-quiz", "Historical events and figures"),
            ("Geography Challenge", "geography-challenge", "World geography and capitals"),
            ("Literature Masters", "literature-masters-quiz", "Classic and modern literature"),
            ("Movie Buff Quiz", "movie-buff-quiz", "Cinema and entertainment knowledge"),
            ("Music Knowledge", "music-knowledge-quiz", "Musical genres and artists"),
            ("Art and Culture", "art-culture-quiz", "Art history and cultural movements"),
            ("Food and Cooking", "food-cooking-quiz", "Culinary knowledge and recipes"),
            ("Travel Explorer", "travel-explorer-quiz", "World destinations and cultures"),
            ("Gaming Universe", "gaming-universe-quiz", "Video game history and culture"),
            ("Future Technology", "future-tech-quiz", "Emerging technologies and innovations")
        ]
        
        for title, slug, description in quiz_data:
            quiz = Quiz(
                title=title,
                slug=slug,
                description=description,
                is_active=True
            )
            quizzes.append(quiz)
            db.session.add(quiz)
        
        db.session.commit()
        
        # Create Questions and Answers for each Quiz (5 questions per quiz)
        question_data = {
            "tech-knowledge-quiz": [
                ("What does AI stand for?", ["Artificial Intelligence", "Automated Information", "Advanced Integration", "Algorithmic Implementation"], 0),
                ("Which company developed React?", ["Facebook", "Google", "Microsoft", "Apple"], 0),
                ("What is the latest version of JavaScript called?", ["ES2023", "JS 2023", "JavaScript 15", "Node.js 20"], 0),
                ("What does GPU stand for?", ["Graphics Processing Unit", "General Processing Unit", "Global Processing Unit", "Game Processing Unit"], 0),
                ("Which programming language is known for AI development?", ["Python", "Java", "C++", "JavaScript"], 0)
            ],
            "business-fundamentals": [
                ("What does ROI stand for?", ["Return on Investment", "Rate of Interest", "Revenue of Income", "Risk of Investment"], 0),
                ("What is a startup's initial funding round called?", ["Seed Round", "Series A", "Angel Round", "Bootstrap"], 0),
                ("What does B2B mean?", ["Business to Business", "Business to Buyer", "Brand to Business", "Buy to Business"], 0),
                ("What is the break-even point?", ["When revenue equals costs", "When profit is maximized", "When growth starts", "When market share increases"], 0),
                ("What does KPI stand for?", ["Key Performance Indicator", "Key Profit Indicator", "Key Process Indicator", "Key Product Indicator"], 0)
            ]
        }
        
        # Create questions for first two quizzes as examples
        for quiz_slug, questions in question_data.items():
            quiz = next((q for q in quizzes if q.slug == quiz_slug), None)
            if quiz:
                for i, (question_text, answers, correct_idx) in enumerate(questions):
                    question = Question(
                        quiz_id=quiz.id,
                        question_text=question_text,
                        question_order=i
                    )
                    db.session.add(question)
                    db.session.flush()  # Get the question ID
                    
                    # Create answers
                    for j, answer_text in enumerate(answers):
                        answer = Answer(
                            question_id=question.id,
                            answer_text=answer_text,
                            is_correct=(j == correct_idx),
                            answer_order=j
                        )
                        db.session.add(answer)
        
        # Create Pages (20)
        page_data = [
            ("About Us", "about-us", "Learn about our mission and team", "About Our News Platform", "Discover our commitment to delivering accurate, timely news and analysis."),
            ("Privacy Policy", "privacy-policy", "Our privacy policy and data protection", "Privacy Policy", "How we protect and handle your personal information."),
            ("Terms of Service", "terms-of-service", "Terms and conditions of use", "Terms of Service", "Legal terms governing your use of our platform."),
            ("Contact Us", "contact-us", "Get in touch with our team", "Contact Information", "Reach out to our editorial team for news tips and inquiries."),
            ("Advertise With Us", "advertise", "Advertising opportunities", "Advertising Opportunities", "Partner with us to reach our engaged audience."),
            ("Careers", "careers", "Join our growing team", "Career Opportunities", "Explore exciting opportunities in digital journalism."),
            ("FAQ", "faq", "Frequently asked questions", "Frequently Asked Questions", "Find answers to common questions about our platform."),
            ("Editorial Guidelines", "editorial-guidelines", "Our editorial standards", "Editorial Standards", "Our commitment to journalistic integrity and accuracy."),
            ("Newsletter Signup", "newsletter", "Subscribe to our newsletter", "Stay Informed", "Get the latest news delivered to your inbox."),
            ("RSS Feeds", "rss", "RSS feed information", "RSS Feeds", "Access our content through RSS feeds."),
            ("API Documentation", "api-docs", "Developer API information", "API Documentation", "Technical documentation for developers."),
            ("Accessibility", "accessibility", "Accessibility statement", "Accessibility Commitment", "Our commitment to making news accessible to everyone."),
            ("Cookie Policy", "cookies", "Cookie usage policy", "Cookie Policy", "How we use cookies to improve your experience."),
            ("Community Guidelines", "community", "Community participation rules", "Community Guidelines", "Rules for respectful participation in our community."),
            ("Press Releases", "press", "Official press releases", "Press Releases", "Official announcements and press statements."),
            ("Investor Relations", "investors", "Information for investors", "Investor Relations", "Financial information and corporate updates."),
            ("Site Map", "sitemap", "Complete site navigation", "Site Map", "Navigate our entire website structure."),
            ("Mobile App", "mobile-app", "Download our mobile app", "Mobile Application", "Access news on the go with our mobile app."),
            ("Archive", "archive", "News archive by date", "News Archive", "Browse our complete news archive by date and category."),
            ("Weather", "weather", "Local weather information", "Weather Updates", "Current weather conditions and forecasts.")
        ]
        
        for title, slug, content, meta_title, meta_description in page_data:
            page = Page(
                title=title,
                slug=slug,
                content=f"<h1>{title}</h1><p>{content}</p><p>This is a comprehensive page covering all aspects of {title.lower()}.</p>",
                meta_title=meta_title,
                meta_description=meta_description,
                is_published=True
            )
            db.session.add(page)
        
        # Create Menu Items (25)
        menu_data = [
            # Header menu items
            ("Home", "/", 1, True, "header"),
            ("Technology", "/category/technology", 2, True, "header"),
            ("Business", "/category/business", 3, True, "header"),
            ("Sports", "/category/sports", 4, True, "header"),
            ("Politics", "/category/politics", 5, True, "header"),
            ("Health", "/category/health", 6, True, "header"),
            ("Science", "/category/science", 7, True, "header"),
            ("Entertainment", "/category/entertainment", 8, True, "header"),
            ("Environment", "/category/environment", 9, True, "header"),
            ("More Categories", "/categories", 10, True, "header"),
            
            # Footer menu items
            ("About", "/about-us", 1, True, "footer"),
            ("Contact", "/contact-us", 2, True, "footer"),
            ("Privacy Policy", "/privacy-policy", 3, True, "footer"),
            ("Terms of Service", "/terms-of-service", 4, True, "footer"),
            ("Careers", "/careers", 5, True, "footer"),
            ("Advertise", "/advertise", 6, True, "footer"),
            ("Newsletter", "/newsletter", 7, True, "footer"),
            ("RSS", "/rss", 8, True, "footer"),
            ("API", "/api-docs", 9, True, "footer"),
            ("Accessibility", "/accessibility", 10, True, "footer"),
            ("Sitemap", "/sitemap", 11, True, "footer"),
            ("Archive", "/archive", 12, True, "footer"),
            ("Mobile App", "/mobile-app", 13, True, "footer"),
            ("Press", "/press", 14, True, "footer"),
            ("Investors", "/investors", 15, True, "footer")
        ]
        
        for title, url, order, active, menu_type in menu_data:
            menu_item = MenuItem(
                title=title,
                url=url,
                menu_order=order,
                is_active=active,
                menu_type=menu_type
            )
            db.session.add(menu_item)
        
        # Create Stock Quotes (25)
        stock_data = [
            ("AAPL", "Apple Inc.", 182.50, 3.25, 1.81, 75000000, 2890000000000),
            ("GOOGL", "Alphabet Inc.", 2834.75, -12.80, -0.45, 25000000, 1780000000000),
            ("MSFT", "Microsoft Corporation", 378.90, 8.15, 2.20, 45000000, 2820000000000),
            ("TSLA", "Tesla Inc.", 265.45, -5.30, -1.96, 95000000, 843000000000),
            ("AMZN", "Amazon.com Inc.", 151.20, 2.15, 1.44, 60000000, 1560000000000),
            ("META", "Meta Platforms Inc.", 312.85, 7.90, 2.59, 35000000, 793000000000),
            ("NVDA", "NVIDIA Corporation", 445.20, 15.75, 3.67, 55000000, 1100000000000),
            ("NFLX", "Netflix Inc.", 442.60, -8.45, -1.87, 12000000, 196000000000),
            ("BABA", "Alibaba Group", 89.32, 1.85, 2.11, 22000000, 236000000000),
            ("SPOT", "Spotify Technology", 178.45, 4.20, 2.41, 8000000, 35000000000),
            ("UBER", "Uber Technologies", 62.10, -1.25, -1.97, 28000000, 127000000000),
            ("SNAP", "Snap Inc.", 11.85, 0.65, 5.80, 45000000, 18500000000),
            ("TWTR", "Twitter Inc.", 54.20, 2.30, 4.43, 35000000, 43000000000),
            ("ZOOM", "Zoom Video Communications", 68.75, -2.15, -3.03, 15000000, 20500000000),
            ("SQ", "Block Inc.", 78.90, 3.45, 4.56, 18000000, 45000000000),
            ("SHOP", "Shopify Inc.", 65.30, 1.80, 2.84, 12000000, 82000000000),
            ("CRM", "Salesforce Inc.", 214.85, 5.60, 2.68, 8000000, 211000000000),
            ("ADBE", "Adobe Inc.", 564.30, 12.45, 2.26, 6000000, 262000000000),
            ("INTC", "Intel Corporation", 43.25, -0.85, -1.93, 42000000, 177000000000),
            ("AMD", "Advanced Micro Devices", 108.60, 4.35, 4.17, 38000000, 175000000000),
            ("COIN", "Coinbase Global", 156.80, 8.90, 6.02, 15000000, 37000000000),
            ("RBLX", "Roblox Corporation", 42.15, -1.35, -3.10, 20000000, 26000000000),
            ("PLTR", "Palantir Technologies", 18.75, 1.25, 7.14, 55000000, 39000000000),
            ("SNOW", "Snowflake Inc.", 195.40, 6.80, 3.61, 7000000, 62000000000),
            ("NET", "Cloudflare Inc.", 87.20, 2.90, 3.44, 9000000, 29000000000)
        ]
        
        for symbol, company, price, change, percent_change, volume, market_cap in stock_data:
            stock = StockQuote(
                symbol=symbol,
                company_name=company,
                current_price=price,
                price_change=change,
                percent_change=percent_change,
                volume=volume,
                market_cap=market_cap
            )
            db.session.add(stock)
        
        # Create Site Settings (30)
        settings_data = [
            ("site_title", "Next News Platform", "text", "Main website title"),
            ("site_description", "Your trusted source for breaking news and analysis", "text", "Site meta description"),
            ("site_keywords", "news, breaking news, analysis, technology, business", "text", "SEO keywords"),
            ("contact_email", "contact@nextnews.com", "text", "Primary contact email"),
            ("support_email", "support@nextnews.com", "text", "Support email address"),
            ("social_twitter", "https://twitter.com/nextnews", "text", "Twitter profile URL"),
            ("social_facebook", "https://facebook.com/nextnews", "text", "Facebook page URL"),
            ("social_instagram", "https://instagram.com/nextnews", "text", "Instagram profile URL"),
            ("social_youtube", "https://youtube.com/nextnews", "text", "YouTube channel URL"),
            ("social_linkedin", "https://linkedin.com/company/nextnews", "text", "LinkedIn company page"),
            ("footer_copyright", "© 2024 Next News Platform. All rights reserved.", "text", "Footer copyright text"),
            ("footer_address", "123 News Street, Media City, NY 10001", "text", "Company address"),
            ("footer_phone", "+1 (555) 123-4567", "text", "Contact phone number"),
            ("analytics_id", "GA-123456789", "text", "Google Analytics tracking ID"),
            ("ads_enabled", "true", "boolean", "Enable advertisements"),
            ("newsletter_enabled", "true", "boolean", "Enable newsletter signup"),
            ("comments_enabled", "true", "boolean", "Enable article comments"),
            ("search_enabled", "true", "boolean", "Enable search functionality"),
            ("dark_mode_enabled", "true", "boolean", "Enable dark mode toggle"),
            ("max_articles_per_page", "10", "number", "Articles per page limit"),
            ("featured_articles_count", "3", "number", "Number of featured articles"),
            ("trending_articles_count", "5", "number", "Number of trending articles"),
            ("related_articles_count", "4", "number", "Number of related articles"),
            ("cache_duration", "300", "number", "Cache duration in seconds"),
            ("api_rate_limit", "100", "number", "API requests per minute limit"),
            ("nav_menu", json.dumps({"logo": {"title": "Next News", "url": "/"}, "items": []}), "json", "Navigation menu configuration"),
            ("footer_menu", json.dumps({"sections": [], "social_links": []}), "json", "Footer menu configuration"),
            ("seo_meta", json.dumps({"title": "Next News", "description": "Breaking news and analysis"}), "json", "SEO metadata"),
            ("theme_colors", json.dumps({"primary": "#3B82F6", "secondary": "#64748B"}), "json", "Theme color scheme"),
            ("feature_flags", json.dumps({"breaking_news_banner": True, "live_updates": False}), "json", "Feature toggles")
        ]
        
        for key, value, setting_type, description in settings_data:
            setting = SiteSettings(
                setting_key=key,
                setting_value=value,
                setting_type=setting_type,
                description=description
            )
            db.session.add(setting)
        
        db.session.commit()
        
        print("✅ Successfully created comprehensive dummy data:")
        print(f"   - {len(authors)} Authors")
        print(f"   - {len(categories)} Categories") 
        print(f"   - {len(tags)} Tags")
        print(f"   - {len(article_data)} Articles")
        print(f"   - {len(quiz_data)} Quizzes")
        print(f"   - Questions and Answers for sample quizzes")
        print(f"   - {len(page_data)} Pages")
        print(f"   - {len(menu_data)} Menu Items")
        print(f"   - {len(stock_data)} Stock Quotes")
        print(f"   - {len(settings_data)} Site Settings")
        
        print("\n🚀 Backend is ready with comprehensive dummy data!")
        print("🌐 Available APIs:")
        print("   - /api/articles - Article management")
        print("   - /api/categories - Category management")
        print("   - /api/authors - Author management")
        print("   - /api/quizzes - Quiz and questions")
        print("   - /api/pages - Static pages")
        print("   - /api/menu - Navigation menus")
        print("   - /api/stocks - Stock market data")
        print("   - /api/settings - Site configuration")

if __name__ == '__main__':
    create_dummy_data()
