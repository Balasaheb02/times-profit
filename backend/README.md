# Flask Backend Setup and Integration Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** database server
3. **Node.js** and **Yarn** (for Next.js frontend)

## Backend Setup

### 1. Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Create a new database:
```sql
CREATE DATABASE news_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE news_db TO your_username;
```

### 4. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update `.env` with your database credentials:
```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/news_db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Initialize Database

```bash
# Initialize the database with tables and sample data
python app.py deploy
```

### 6. Run the Flask Backend

```bash
python run.py
```

The backend will be available at `http://localhost:5000`

## Frontend Integration

### 1. Update Environment Variables

Create a `.env.local` file in the Next.js root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### 2. Update Import Statements

Replace the existing client imports with the new backend client. For example, in your components:

```typescript
// Old import
import { getHomepage } from "@/lib/client"

// New import
import { getHomepage } from "@/lib/backend-client"
```

## API Endpoints

### Articles
- `GET /api/articles` - Get all articles (with pagination)
- `GET /api/articles/{slug}` - Get article by slug
- `POST /api/articles` - Create new article
- `PUT /api/articles/{slug}` - Update article
- `DELETE /api/articles/{slug}` - Delete article
- `GET /api/articles/trending` - Get trending articles
- `GET /api/articles/recent` - Get recent articles
- `GET /api/articles/search?q={query}` - Search articles

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{slug}` - Get category by slug
- `GET /api/categories/{slug}/articles` - Get articles by category
- `POST /api/categories` - Create new category
- `PUT /api/categories/{slug}` - Update category
- `DELETE /api/categories/{slug}` - Delete category

### Authors
- `GET /api/authors` - Get all authors
- `GET /api/authors/{id}` - Get author by ID
- `POST /api/authors` - Create new author
- `PUT /api/authors/{id}` - Update author
- `DELETE /api/authors/{id}` - Delete author

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (requires auth)
- `PUT /api/auth/profile` - Update user profile (requires auth)

### Health Check
- `GET /api/health` - Backend health check

## Sample Data

The backend includes sample data creation. After running `python app.py deploy`, you'll have:

- Sample authors
- Sample categories (Technology, Sports, Politics, Entertainment)
- Sample tags (AI, Web Development, Python, React, Next.js)

## Testing the Integration

1. Start the Flask backend: `python run.py`
2. Start the Next.js frontend: `yarn dev`
3. Visit `http://localhost:3000` to see your integrated application

## Adding New Articles

You can add articles via the API or create a simple admin interface. Here's an example of creating an article via API:

```bash
curl -X POST http://localhost:5000/api/articles \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Article Title",
    "slug": "your-article-slug",
    "content": "Your article content here...",
    "excerpt": "Short description",
    "is_published": true,
    "author_id": "your-author-id",
    "category_id": "your-category-id"
  }'
```

## Database Migrations

If you need to modify the database schema:

```bash
# Generate migration
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

## Production Deployment

For production:

1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Configure PostgreSQL with proper security settings
4. Update CORS settings for your production domain
5. Use environment variables for all sensitive configuration

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure virtual environment is activated and dependencies are installed
2. **Database connection issues**: Check PostgreSQL is running and credentials are correct
3. **CORS errors**: Ensure Flask-CORS is properly configured
4. **404 errors**: Verify API endpoints are correctly registered

### Debug Mode

The backend runs in debug mode by default in development. Check the console output for detailed error messages.
