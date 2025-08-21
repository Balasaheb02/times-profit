# Hostinger Frontend Deployment Guide (Next.js)

## Option 1: Deploy to Hostinger Static Hosting

### Prerequisites
- Hostinger Web Hosting plan
- Domain configured in Hostinger
- Git repository with your code

### Step 1: Prepare Next.js for Static Export

#### 1.1 Update next.config.mjs
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  env: {
    NEXT_PUBLIC_API_URL: 'https://api.yourdomain.com/api'
  }
};

export default nextConfig;
```

#### 1.2 Update package.json Scripts
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "export": "next build && next export",
    "start": "next start",
    "lint": "next lint"
  }
}
```

#### 1.3 Create Environment File
Create `.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

### Step 2: Build and Export

#### 2.1 Install Dependencies
```bash
npm install
```

#### 2.2 Build for Production
```bash
npm run build
```

This creates an `out` folder with static files.

### Step 3: Upload to Hostinger

#### Option A: File Manager Upload
1. Login to Hostinger Control Panel
2. Go to File Manager
3. Navigate to `public_html` folder
4. Upload all files from the `out` folder
5. Extract and place files directly in `public_html`

#### Option B: FTP Upload
```bash
# Using FileZilla or similar FTP client
# Host: ftp.yourdomain.com
# Username: your-ftp-username
# Password: your-ftp-password
# Upload contents of 'out' folder to public_html
```

### Step 4: Configure Domain
1. In Hostinger Control Panel, go to Domains
2. Point your domain to the hosting account
3. Wait for DNS propagation (up to 24 hours)

---

## Option 2: Deploy to Hostinger VPS (Recommended)

### Step 1: Server Setup

#### 1.1 Connect to VPS
```bash
ssh root@your-vps-ip
```

#### 1.2 Install Node.js and PM2
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install nodejs nginx -y
npm install -g pm2
```

### Step 2: Deploy Application

#### 2.1 Clone Repository
```bash
cd /var/www
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

#### 2.2 Install Dependencies
```bash
npm install
```

#### 2.3 Create Production Environment
```bash
nano .env.production.local
```

Add:
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

#### 2.4 Build Application
```bash
npm run build
```

#### 2.5 Start with PM2
```bash
pm2 start npm --name "nextjs-app" -- start
pm2 startup
pm2 save
```

### Step 3: Configure Nginx

#### 3.1 Create Nginx Configuration
```bash
nano /etc/nginx/sites-available/frontend
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

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
}
```

#### 3.2 Enable Site
```bash
ln -s /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 4: SSL Certificate
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Option 3: Deploy Both on Same VPS

### Complete Nginx Configuration
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring Commands

### Check Application Status
```bash
# Frontend
pm2 status
pm2 logs nextjs-app

# Backend
systemctl status newsapp
journalctl -u newsapp.service -f

# Nginx
systemctl status nginx
tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
# Frontend
pm2 restart nextjs-app

# Backend
systemctl restart newsapp

# Nginx
systemctl restart nginx
```

## Performance Optimization

### 1. Enable Gzip in Nginx
Add to nginx.conf:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

### 2. Add Caching Headers
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Database Connection Pooling
In your Flask app, ensure connection pooling is enabled:
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```
