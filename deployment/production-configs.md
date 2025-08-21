# Production Configuration Files

## Flask Backend Production Files

### 1. config.py
```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-production-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://newsuser:password@localhost/newsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS settings for production
    CORS_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']
    
    # Performance settings
    COMPRESS_MIMETYPES = [
        'text/html', 'text/css', 'text/xml', 'application/json',
        'application/javascript', 'text/javascript', 'application/xml'
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
```

### 2. wsgi.py
```python
import os
from app import create_app

app = create_app('production')

if __name__ == "__main__":
    app.run()
```

### 3. requirements.txt
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.3
Flask-Compress==1.13
marshmallow==3.20.1
marshmallow-sqlalchemy==0.29.0
psycopg2-binary==2.9.7
gunicorn==21.2.0
python-dotenv==1.0.0
```

### 4. .env (Production Environment Variables)
```bash
SECRET_KEY=your-super-secret-production-key-change-this
DATABASE_URL=postgresql://newsuser:your-secure-password@localhost/newsdb
JWT_SECRET_KEY=your-jwt-secret-key-change-this
FLASK_ENV=production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 5. Dockerfile (Optional - for containerized deployment)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:app"]
```

## Next.js Frontend Production Files

### 1. next.config.mjs (Static Export)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  env: {
    NEXT_PUBLIC_API_URL: 'https://api.yourdomain.com/api',
    NEXT_PUBLIC_SITE_URL: 'https://yourdomain.com'
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
};

export default nextConfig;
```

### 2. next.config.mjs (Server-side)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: 'https://api.yourdomain.com/api',
    NEXT_PUBLIC_SITE_URL: 'https://yourdomain.com'
  },
  images: {
    domains: ['yourdomain.com', 'api.yourdomain.com'],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
};

export default nextConfig;
```

### 3. .env.production
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

### 4. package.json (Updated Scripts)
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "export": "next build && next export",
    "lint": "next lint",
    "analyze": "ANALYZE=true next build"
  }
}
```

## System Service Files

### 1. newsapp.service (Backend Service)
```ini
[Unit]
Description=Gunicorn instance to serve newsapp
After=network.target

[Service]
User=newsapp
Group=www-data
WorkingDirectory=/home/newsapp/backend
Environment="PATH=/home/newsapp/backend/venv/bin"
EnvironmentFile=/home/newsapp/backend/.env
ExecStart=/home/newsapp/backend/venv/bin/gunicorn --workers 4 --bind unix:newsapp.sock -m 007 wsgi:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 2. Nginx Configuration (/etc/nginx/sites-available/newsapp)
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=web:10m rate=30r/s;

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req zone=api burst=20 nodelay;
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/newsapp/backend/newsapp.sock;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # API specific optimizations
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/home/newsapp/backend/newsapp.sock;
        
        # Enable compression
        gzip on;
        gzip_types application/json application/javascript text/css text/javascript text/plain text/xml;
        gzip_min_length 1000;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req zone=web burst=50 nodelay;
    
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Static file caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
}
```

## Database Setup

### 1. PostgreSQL Configuration
```sql
-- Create database and user
CREATE DATABASE newsdb;
CREATE USER newsuser WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE newsdb TO newsuser;
ALTER USER newsuser CREATEDB;

-- Connect to newsdb
\c newsdb

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO newsuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO newsuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO newsuser;
```

### 2. Database Backup Script
```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/newsapp/backups"
DB_NAME="newsdb"
DB_USER="newsuser"

mkdir -p $BACKUP_DIR

pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/newsdb_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "newsdb_backup_*.sql" -mtime +7 -delete

echo "Database backup completed: newsdb_backup_$DATE.sql"
```

## Monitoring and Logging

### 1. Log Rotation Configuration
```bash
# /etc/logrotate.d/newsapp
/home/newsapp/backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 newsapp newsapp
    postrotate
        systemctl reload newsapp
    endscript
}
```

### 2. Health Check Script
```bash
#!/bin/bash
# health-check.sh

API_URL="https://api.yourdomain.com/api/health"
WEB_URL="https://yourdomain.com"

# Check API health
if curl -f -s $API_URL > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API is down"
    systemctl restart newsapp
fi

# Check website
if curl -f -s $WEB_URL > /dev/null; then
    echo "✅ Website is healthy"
else
    echo "❌ Website is down"
    pm2 restart nextjs-app
fi
```

Add to crontab:
```bash
# Check every 5 minutes
*/5 * * * * /home/newsapp/scripts/health-check.sh >> /var/log/health-check.log 2>&1
```
