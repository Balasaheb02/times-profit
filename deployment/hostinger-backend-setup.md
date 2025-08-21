# Hostinger Backend Deployment Guide

## Prerequisites
- Hostinger VPS or Cloud Hosting plan (shared hosting won't work for Flask)
- SSH access to your server
- Domain name

## Step 1: Prepare Flask App for Production

### 1.1 Create Production Configuration
Create `config.py` in your backend folder:

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-production-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/newsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
```

### 1.2 Create Requirements File
```bash
pip freeze > requirements.txt
```

### 1.3 Create Gunicorn WSGI File
Create `wsgi.py`:

```python
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run()
```

## Step 2: Server Setup on Hostinger

### 2.1 Connect via SSH
```bash
ssh root@your-server-ip
```

### 2.2 Update System
```bash
apt update && apt upgrade -y
```

### 2.3 Install Required Software
```bash
# Install Python and pip
apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Install Node.js for frontend
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install nodejs -y
```

### 2.4 Create Application User
```bash
adduser newsapp
usermod -aG sudo newsapp
su - newsapp
```

### 2.5 Setup PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE newsdb;
CREATE USER newsuser WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE newsdb TO newsuser;
\q
```

## Step 3: Deploy Flask Backend

### 3.1 Upload Code
```bash
# Option 1: Git clone (recommended)
git clone https://github.com/yourusername/your-repo.git
cd your-repo/backend

# Option 2: Upload via SCP/SFTP
# Upload your backend folder to /home/newsapp/backend
```

### 3.2 Setup Virtual Environment
```bash
cd /home/newsapp/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3.3 Set Environment Variables
Create `.env` file:
```bash
export SECRET_KEY="your-super-secret-production-key"
export DATABASE_URL="postgresql://newsuser:your-secure-password@localhost/newsdb"
export JWT_SECRET_KEY="your-jwt-secret-key"
export FLASK_ENV="production"
```

### 3.4 Initialize Database
```bash
source .env
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
python add_comprehensive_dummy_data.py
```

### 3.5 Test Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

## Step 4: Configure Nginx

### 4.1 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/newsapp
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.2 Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/newsapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Step 5: Create Systemd Service

### 5.1 Create Service File
```bash
sudo nano /etc/systemd/system/newsapp.service
```

Add this content:
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
ExecStart=/home/newsapp/backend/venv/bin/gunicorn --workers 3 --bind unix:newsapp.sock -m 007 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 5.2 Start and Enable Service
```bash
sudo systemctl start newsapp
sudo systemctl enable newsapp
sudo systemctl status newsapp
```

## Step 6: SSL Certificate (Optional but Recommended)

### 6.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 6.2 Get SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d api.your-domain.com
```

## Monitoring and Maintenance

### View Logs
```bash
# Application logs
sudo journalctl -u newsapp.service -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Restart Services
```bash
sudo systemctl restart newsapp
sudo systemctl restart nginx
```
