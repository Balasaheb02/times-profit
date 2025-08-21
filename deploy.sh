#!/bin/bash

# Production deployment script for News Platform
echo "🚀 Starting production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if required tools are installed
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is not installed. Please install it first."
        exit 1
    fi
    
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI is not installed. Installing..."
        npm install -g vercel
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install it first."
        exit 1
    fi
    
    print_status "All dependencies are installed"
}

# Deploy backend to Heroku
deploy_backend() {
    echo "🔧 Deploying backend to Heroku..."
    
    cd backend
    
    # Check if Heroku app exists
    if ! heroku apps:info $HEROKU_APP_NAME &> /dev/null; then
        print_warning "Creating new Heroku app: $HEROKU_APP_NAME"
        heroku create $HEROKU_APP_NAME
    fi
    
    # Add PostgreSQL addon if not exists
    if ! heroku addons:info heroku-postgresql --app $HEROKU_APP_NAME &> /dev/null; then
        print_warning "Adding PostgreSQL addon..."
        heroku addons:create heroku-postgresql:mini --app $HEROKU_APP_NAME
    fi
    
    # Set environment variables
    print_status "Setting environment variables..."
    heroku config:set FLASK_ENV=production --app $HEROKU_APP_NAME
    heroku config:set SECRET_KEY=$(openssl rand -base64 32) --app $HEROKU_APP_NAME
    heroku config:set JWT_SECRET_KEY=$(openssl rand -base64 32) --app $HEROKU_APP_NAME
    
    # Deploy to Heroku
    print_status "Deploying to Heroku..."
    git add .
    git commit -m "Deploy backend to production" || true
    git push heroku main
    
    # Run database setup
    print_status "Setting up database..."
    heroku run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()" --app $HEROKU_APP_NAME
    heroku run python add_comprehensive_dummy_data.py --app $HEROKU_APP_NAME
    
    # Get backend URL
    BACKEND_URL=$(heroku apps:info $HEROKU_APP_NAME --json | jq -r '.app.web_url')
    print_status "Backend deployed to: $BACKEND_URL"
    
    cd ..
}

# Deploy frontend to Vercel
deploy_frontend() {
    echo "🎨 Deploying frontend to Vercel..."
    
    # Update environment variables
    echo "NEXT_PUBLIC_API_URL=${BACKEND_URL}api" > .env.production
    echo "NEXT_PUBLIC_SITE_URL=https://your-domain.vercel.app" >> .env.production
    
    # Deploy to Vercel
    print_status "Deploying to Vercel..."
    vercel --prod
    
    print_status "Frontend deployed successfully!"
}

# Test deployment
test_deployment() {
    echo "🧪 Testing deployment..."
    
    # Test backend health
    if curl -f "${BACKEND_URL}api/health" &> /dev/null; then
        print_status "Backend health check passed"
    else
        print_error "Backend health check failed"
    fi
    
    # Test API endpoints
    if curl -f "${BACKEND_URL}api/articles" &> /dev/null; then
        print_status "Articles API working"
    else
        print_error "Articles API failed"
    fi
}

# Main deployment process
main() {
    echo "📋 Production Deployment Script"
    echo "==============================="
    
    # Get app name from user
    read -p "Enter your Heroku app name: " HEROKU_APP_NAME
    
    if [ -z "$HEROKU_APP_NAME" ]; then
        print_error "App name is required"
        exit 1
    fi
    
    check_dependencies
    deploy_backend
    deploy_frontend
    test_deployment
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "📱 Backend URL: $BACKEND_URL"
    echo "🌐 Frontend URL: Check Vercel output above"
    echo ""
    echo "📋 Next steps:"
    echo "1. Update CORS_ORIGINS in Heroku with your frontend domain"
    echo "2. Set up custom domains if needed"
    echo "3. Configure monitoring and analytics"
    echo "4. Set up automated backups"
}

# Run main function
main "$@"
