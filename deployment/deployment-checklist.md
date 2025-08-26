# 🚀 Complete Hostinger Deployment Checklist

## Pre-Deployment Preparation

### ✅ Backend Checklist
- [ ] Flask app is working locally
- [ ] All dependencies are in requirements.txt
- [ ] Database models are finalized
- [ ] Environment variables are configured
- [ ] CORS settings are updated for production domain
- [ ] Security headers are implemented
- [ ] API endpoints are tested

### ✅ Frontend Checklist
- [ ] Next.js app builds successfully
- [ ] API calls point to production backend URL
- [ ] Environment variables are set
- [ ] Static assets are optimized
- [ ] SEO metadata is configured
- [ ] Error pages are implemented

### ✅ Domain & Hosting Setup
- [ ] Domain is purchased and configured
- [ ] DNS settings point to Hostinger
- [ ] SSL certificate is ready to install
- [ ] Hostinger VPS or hosting plan is active

## Step-by-Step Deployment Process

### Phase 1: Backend Deployment (30-45 minutes)

#### 1.1 Server Preparation
```bash
# Connect to your Hostinger VPS
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install required software
apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib git -y
```

#### 1.2 Database Setup
```bash
# Switch to postgres user and create database
sudo -u postgres psql
CREATE DATABASE newsdb;
CREATE USER newsuser WITH ENCRYPTED PASSWORD 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE newsdb TO newsuser;
\q
```

#### 1.3 Application Deployment
```bash
# Create app user
adduser newsapp
usermod -aG sudo newsapp
su - newsapp

# Clone your repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Set environment variables
nano .env
# Add your production environment variables

# IMPORTANT: Make sure virtual environment is activated
source venv/bin/activate

# Verify Flask is installed
python -c "import flask; print('Flask version:', flask.__version__)"

# Initialize database
export $(cat .env | xargs)
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
python add_comprehensive_dummy_data.py
```

#### 1.4 Service Configuration
```bash
# Test gunicorn
gunicorn --bind 0.0.0.0:8000 wsgi:app

# Create systemd service
sudo nano /etc/systemd/system/newsapp.service
# Copy the service configuration from production-configs.md

# Start service
sudo systemctl daemon-reload
sudo systemctl start newsapp
sudo systemctl enable newsapp
sudo systemctl status newsapp
```

#### 1.5 Nginx Configuration
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/newsapp
# Copy the nginx configuration from production-configs.md

# Enable site
sudo ln -s /etc/nginx/sites-available/newsapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Phase 2: Frontend Deployment (20-30 minutes)

#### Option A: Static Export to Shared Hosting

1. **Local Build Process:**
```bash
# In your local frontend directory
npm install
npm run build

# This creates an 'out' folder with static files
```

2. **Upload to Hostinger:**
   - Login to Hostinger Control Panel
   - Go to File Manager
   - Navigate to public_html
   - Upload all files from the 'out' folder
   - Set proper file permissions

#### Option B: Server-Side Rendering on VPS

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install nodejs -y
npm install -g pm2

# Deploy application
cd /var/www
git clone https://github.com/yourusername/your-repo.git
cd your-repo
npm install
npm run build

# Start with PM2
pm2 start npm --name "nextjs-app" -- start
pm2 startup
pm2 save

# Configure nginx for frontend (update existing config)
sudo nano /etc/nginx/sites-available/newsapp
sudo nginx -t
sudo systemctl restart nginx
```

### Phase 3: SSL and Security (15-20 minutes)

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificates
certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Test auto-renewal
certbot renew --dry-run
```

### Phase 4: Monitoring and Optimization (15 minutes)

```bash
# Setup log rotation
sudo nano /etc/logrotate.d/newsapp
# Copy configuration from production-configs.md

# Create monitoring scripts
mkdir -p /home/newsapp/scripts
nano /home/newsapp/scripts/health-check.sh
chmod +x /home/newsapp/scripts/health-check.sh

# Add to crontab
crontab -e
# Add: */5 * * * * /home/newsapp/scripts/health-check.sh >> /var/log/health-check.log 2>&1

# Setup database backups
nano /home/newsapp/scripts/backup-db.sh
chmod +x /home/newsapp/scripts/backup-db.sh

# Add backup to crontab
# Add: 0 2 * * * /home/newsapp/scripts/backup-db.sh
```

## Post-Deployment Verification

### ✅ Backend Testing
```bash
# Test API endpoints
curl https://api.yourdomain.com/api/health
curl https://api.yourdomain.com/api/articles
curl https://api.yourdomain.com/api/categories
```

### ✅ Frontend Testing
- [ ] Visit https://yourdomain.com
- [ ] Check all pages load correctly
- [ ] Verify API integration works
- [ ] Test responsive design
- [ ] Check SEO metadata

### ✅ Performance Testing
```bash
# Test page load speed
curl -o /dev/null -s -w "Time: %{time_total}s\n" https://yourdomain.com

# Check SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

## Common Issues and Solutions

### Backend Issues

**Issue: ModuleNotFoundError: No module named 'flask'**
```bash
# This means virtual environment is not activated
# Solution:
cd /home/newsapp/times-profit/backend
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python
python -c "import flask; print('Flask is available')"

# If Flask is still not found, reinstall dependencies
pip install -r requirements.txt

# Then retry the database initialization
export $(cat .env | xargs)
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
```

**Issue: Gunicorn won't start**
```bash
# Check logs
journalctl -u newsapp.service -f

# Common fixes:
# 1. Check file permissions
sudo chown -R newsapp:www-data /home/newsapp/backend

# 2. Check environment variables
source /home/newsapp/backend/.env
echo $DATABASE_URL

# 3. Test database connection
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.engine.execute('SELECT 1')"
```

**Issue: Database connection failed**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check user permissions
sudo -u postgres psql -c "\du"

# Reset password if needed
sudo -u postgres psql -c "ALTER USER newsuser PASSWORD 'new-password';"
```

### Frontend Issues

**Issue: API calls failing**
- Check CORS settings in Flask app
- Verify API URL in environment variables
- Check nginx proxy configuration

**Issue: Static files not loading**
- Check file permissions in public_html
- Verify nginx static file configuration
- Clear browser cache

### SSL Issues

**Issue: Certificate not working**
```bash
# Check certificate status
certbot certificates

# Renew if needed
certbot renew

# Check nginx configuration
nginx -t
```

## Maintenance Commands

### Daily Operations
```bash
# Check service status
sudo systemctl status newsapp
pm2 status

# View logs
journalctl -u newsapp.service -f
pm2 logs nextjs-app

# Restart services if needed
sudo systemctl restart newsapp
pm2 restart nextjs-app
sudo systemctl restart nginx
```

### Updates
```bash
# Backend updates
cd /home/newsapp/backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart newsapp

# Frontend updates
cd /var/www/your-repo
git pull
npm install
npm run build
pm2 restart nextjs-app
```

## Performance Optimization

### Database Optimization
```bash
# Run the database optimization script
cd /home/newsapp/backend
python optimize_database.py
```

### Nginx Optimization
- Enable gzip compression
- Set proper cache headers
- Configure rate limiting
- Optimize proxy settings

### Application Optimization
- Use Redis for caching (optional)
- Optimize database queries
- Implement API rate limiting
- Monitor server resources

## Security Checklist

- [ ] SSH key authentication enabled
- [ ] Firewall configured (ufw)
- [ ] Regular security updates
- [ ] Strong passwords for all accounts
- [ ] Database access restricted
- [ ] API rate limiting enabled
- [ ] Security headers configured
- [ ] Regular backups automated

## Success Indicators

Your deployment is successful when:
- ✅ Backend API responds at https://api.yourdomain.com/api/health
- ✅ Frontend loads at https://yourdomain.com
- ✅ SSL certificates are active and valid
- ✅ All API endpoints return expected data
- ✅ Database is populated with sample data
- ✅ Monitoring and logging are working
- ✅ Automatic backups are configured

## Next Steps After Deployment

1. **Content Management**: Add real content to replace dummy data
2. **Analytics**: Setup Google Analytics or similar
3. **SEO**: Submit sitemap to search engines
4. **Performance**: Monitor and optimize based on real usage
5. **Features**: Add user authentication, comments, etc.
6. **Backup Strategy**: Implement regular backups
7. **Scaling**: Plan for increased traffic

## Support Resources

- **Hostinger Documentation**: https://support.hostinger.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Nginx Documentation**: https://nginx.org/en/docs/

**Estimated Total Deployment Time: 2-3 hours**
**Difficulty Level: Intermediate**
**Cost: $10-50/month (depending on hosting plan)**
