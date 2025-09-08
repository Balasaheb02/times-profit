#!/bin/bash

echo "📊 Database Schema and Sample Data Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Run these SQL commands to ensure your database has proper structure:"
echo ""

cat << 'EOF'
-- Connect to your database first:
-- psql -h localhost -U newsuser -d newsdb

-- 1. Check existing tables
\dt

-- 2. View table structures
\d articles
\d categories
\d authors

-- 3. Sample data for testing (if tables are empty)

-- Insert sample categories
INSERT INTO categories (name, slug, description, created_at, updated_at) VALUES
('Technology', 'technology', 'Latest technology news and updates', NOW(), NOW()),
('Business', 'business', 'Business and financial news', NOW(), NOW()),
('Sports', 'sports', 'Sports news and updates', NOW(), NOW()),
('Entertainment', 'entertainment', 'Entertainment and celebrity news', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- Insert sample authors
INSERT INTO authors (name, email, bio, avatar_url, created_at, updated_at) VALUES
('John Smith', 'john@timesprofit.com', 'Senior Technology Reporter', '/images/authors/john.jpg', NOW(), NOW()),
('Sarah Johnson', 'sarah@timesprofit.com', 'Business Analyst', '/images/authors/sarah.jpg', NOW(), NOW()),
('Mike Wilson', 'mike@timesprofit.com', 'Sports Editor', '/images/authors/mike.jpg', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

-- Insert sample articles
INSERT INTO articles (title, slug, excerpt, content, featured_image, is_published, published_at, views, category_id, author_id, created_at, updated_at)
SELECT 
    'Breaking: New Technology Trends for 2025',
    'new-technology-trends-2025',
    'Discover the latest technology trends that will shape the future in 2025.',
    '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"This article explores the emerging technology trends..."}]}]}',
    '/images/articles/tech-2025.jpg',
    true,
    NOW(),
    150,
    c.id,
    a.id,
    NOW(),
    NOW()
FROM categories c, authors a 
WHERE c.slug = 'technology' AND a.email = 'john@timesprofit.com'
AND NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'new-technology-trends-2025');

INSERT INTO articles (title, slug, excerpt, content, featured_image, is_published, published_at, views, category_id, author_id, created_at, updated_at)
SELECT 
    'Market Analysis: Stock Predictions for Q4',
    'market-analysis-stock-predictions-q4',
    'Expert analysis on stock market trends and predictions for the fourth quarter.',
    '{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Financial experts analyze market trends..."}]}]}',
    '/images/articles/market-analysis.jpg',
    true,
    NOW(),
    89,
    c.id,
    a.id,
    NOW(),
    NOW()
FROM categories c, authors a 
WHERE c.slug = 'business' AND a.email = 'sarah@timesprofit.com'
AND NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'market-analysis-stock-predictions-q4');

-- Check if data was inserted
SELECT 
    a.title,
    a.slug,
    c.name as category,
    au.name as author,
    a.views,
    a.published_at
FROM articles a
JOIN categories c ON a.category_id = c.id
JOIN authors au ON a.author_id = au.id
ORDER BY a.published_at DESC;

-- Check total counts
SELECT 
    (SELECT COUNT(*) FROM articles) as total_articles,
    (SELECT COUNT(*) FROM categories) as total_categories,
    (SELECT COUNT(*) FROM authors) as total_authors;

EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 TIP: Save the SQL commands above to a file and run them in DBeaver!"
echo "📋 You can also run: psql -h localhost -U newsuser -d newsdb -f setup.sql"
