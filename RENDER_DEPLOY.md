# Render.com Deployment Settings

## 🚀 RENDER DEPLOYMENT CONFIGURATION

### Build & Deploy Settings:
```
Build Command: npm run build
Start Command: npm start
Environment: Node
```

### Environment Variables:
```
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

### Auto-Deploy:
- ✅ Enable Auto-Deploy from GitHub
- Branch: main

## 📋 Complete Setup Steps:

1. **Push the cleaned code:**
   ```bash
   git add .
   git commit -m "Simplified for Render deployment"
   git push origin main
   ```

2. **Create Render Service:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name:** times-profit
     - **Environment:** Node
     - **Build Command:** `npm run build`
     - **Start Command:** `npm start`
     - **Node Version:** 18.x or higher

3. **Add Environment Variables:**
   - NODE_ENV = production
   - NEXT_TELEMETRY_DISABLED = 1

4. **Deploy!**

## ✅ What's Fixed:
- Removed problematic API routes (stockdaily, webhooks, og)
- Removed sitemap generation routes
- Removed catch-all routes
- Removed package-lock.json conflicts
- Simplified Next.js config

Your site will be live at: `https://times-profit.onrender.com`
