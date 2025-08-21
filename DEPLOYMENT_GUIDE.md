# Deployment Guide for News Platform

## 📋 Pre-Deployment Checklist

### Backend Preparation
- [x] Flask app optimized with compression
- [x] Database indexes added
- [x] API caching implemented
- [x] Production configuration ready
- [x] Requirements.txt updated
- [x] Procfile created

### Frontend Preparation
- [x] Next.js optimized build
- [x] API client with caching
- [x] Environment variables configured
- [x] Production build tested

## 🚀 Deployment Steps

### Step 1: Backend Deployment (Heroku)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   cd backend
   heroku login
   heroku create your-news-backend
   ```

3. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(openssl rand -base64 32)
   heroku config:set JWT_SECRET_KEY=$(openssl rand -base64 32)
   heroku config:set CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

5. **Deploy Backend**
   ```bash
   git add .
   git commit -m "Prepare for production deployment"
   git push heroku main
   ```

6. **Run Database Migrations**
   ```bash
   heroku run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   heroku run python add_comprehensive_dummy_data.py
   ```

### Step 2: Frontend Deployment (Vercel)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Update API URL**
   ```bash
   # Edit .env.production with your Heroku backend URL
   NEXT_PUBLIC_API_URL=https://your-news-backend.herokuapp.com/api
   ```

3. **Deploy Frontend**
   ```bash
   cd ../  # Go to root directory
   vercel
   # Follow the prompts to deploy
   ```

4. **Set Environment Variables in Vercel**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   vercel env add NEXT_PUBLIC_SITE_URL
   ```

### Step 3: Alternative Deployment Options

#### Railway (Backend Alternative)
1. Connect GitHub repository
2. Select backend folder
3. Add PostgreSQL plugin
4. Deploy automatically

#### Netlify (Frontend Alternative)
1. Connect GitHub repository
2. Build command: `npm run build`
3. Publish directory: `out` or `.next`
4. Set environment variables

## 🔧 Production Optimizations

### Backend Optimizations
- ✅ Database connection pooling
- ✅ Response compression (gzip)
- ✅ Database indexes
- ✅ Query optimization with joinedload
- ✅ API response caching

### Frontend Optimizations
- ✅ API client caching (TTL cache)
- ✅ WeakMap memoization for article conversion
- ✅ Batch API processing
- ✅ Parallel data fetching
- ✅ Image optimization with Next.js

## 🌐 Custom Domain Setup

### Backend Custom Domain (Heroku)
```bash
heroku domains:add api.yournewssite.com
# Configure DNS CNAME: api.yournewssite.com -> your-news-backend.herokuapp.com
```

### Frontend Custom Domain (Vercel)
```bash
vercel domains add yournewssite.com
# Configure DNS: yournewssite.com -> Vercel's servers
```

## 📊 Monitoring & Analytics

### Backend Monitoring
- Heroku logs: `heroku logs --tail`
- Database monitoring: Heroku Postgres dashboard
- Performance: New Relic or Datadog

### Frontend Monitoring
- Vercel Analytics (built-in)
- Google Analytics (add GA_TRACKING_ID)
- Core Web Vitals monitoring

## 🔒 Security Enhancements

### Backend Security
- [x] JWT token authentication
- [x] CORS configuration
- [x] Environment variables for secrets
- [ ] Rate limiting (add Flask-Limiter)
- [ ] Input validation & sanitization
- [ ] HTTPS enforcement

### Frontend Security
- [x] Environment variables for API URLs
- [ ] Content Security Policy (CSP)
- [ ] HTTPS enforcement
- [ ] XSS protection

## 📈 Performance Metrics

### Expected Performance
- **Backend API Response**: < 200ms (with caching)
- **Frontend Load Time**: < 2s (First Contentful Paint)
- **Database Queries**: Optimized with indexes
- **Caching Hit Rate**: > 80% for repeated requests

## 🚨 Common Issues & Solutions

### Backend Issues
1. **Database Connection Errors**
   - Check DATABASE_URL environment variable
   - Verify PostgreSQL addon is attached

2. **CORS Errors**
   - Update CORS_ORIGINS with frontend domain
   - Ensure protocol (https/http) matches

### Frontend Issues
1. **API Connection Errors**
   - Verify NEXT_PUBLIC_API_URL is correct
   - Check backend is deployed and running

2. **Build Errors**
   - Run `npm run build` locally first
   - Check for TypeScript errors

## 📝 Post-Deployment Tasks

1. **Test All APIs**
   ```bash
   # Test backend health
   curl https://your-news-backend.herokuapp.com/api/health
   
   # Test frontend
   curl https://your-news-frontend.vercel.app
   ```

2. **Performance Testing**
   - Use Google PageSpeed Insights
   - Test API endpoints with Postman
   - Monitor error rates

3. **SEO Setup**
   - Submit sitemap to Google Search Console
   - Set up Google Analytics
   - Configure meta tags and structured data

4. **Backup Strategy**
   - Set up Heroku Postgres backups
   - Export database regularly
   - Version control all code changes

## 💰 Cost Estimation

### Free Tier Limits
- **Heroku**: 550-1000 dyno hours/month (free)
- **Vercel**: 100GB bandwidth/month (free)
- **PostgreSQL**: 10K rows (free)

### Paid Upgrades (when needed)
- **Heroku Hobby**: $7/month (basic dyno)
- **Heroku Postgres**: $9/month (10M rows)
- **Vercel Pro**: $20/month (unlimited)

Your application is now production-ready! 🎉
