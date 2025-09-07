# Easy Vercel Deployment Guide

## Quick Deploy Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Visit: https://vercel.com
   - Sign in with GitHub
   - Click "New Project"
   - Import this repository
   - Click "Deploy"

## Build Commands:
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

## Environment Variables:
Add these in Vercel dashboard:
- `NODE_ENV=production`
- `NEXT_TELEMETRY_DISABLED=1`

## That's it! ✅
Your site will be live at: `https://your-project-name.vercel.app`

## Troubleshooting:
If build fails, check:
1. All dependencies are in package.json
2. No TypeScript errors (we disabled strict checking)
3. All imports are correct

## Manual Commands to Run Locally:
```bash
npm install
npm run dev     # Development
npm run build   # Production build
npm start       # Production server
```
