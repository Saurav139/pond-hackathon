# PlatForge.ai Deployment Guide

## 🚀 Complete Deployment from Scratch

### Prerequisites
- GitHub repository: `https://github.com/Saurav139/pond-hackathon`
- GCP Service Account JSON key
- Railway account
- Vercel account

## 1. Backend Deployment (Railway)

### Option 1: Railway Dashboard (Recommended)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `Saurav139/pond-hackathon`
4. Set **Root Directory**: `backend`
5. Railway will auto-detect Python and use the Dockerfile

### Option 2: Railway CLI
```bash
cd backend
railway login
railway init
railway up
```

### Environment Variables (Railway Dashboard)
Add these in Railway Project → Variables:
```
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"...}
PORT=8001
```

### Railway Configuration Files ✅
- `backend/Dockerfile` - Container configuration
- `backend/railway.toml` - Railway deployment settings
- `backend/requirements.txt` - Python dependencies

## 2. Frontend Deployment (Vercel)

### Option 1: Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project" → Import from GitHub
3. Select `Saurav139/pond-hackathon`
4. Set **Root Directory**: `frontend`
5. Set **Framework Preset**: Next.js

### Option 2: Vercel CLI
```bash
cd frontend
npx vercel login
npx vercel --prod
```

### Environment Variables (Vercel Dashboard)
Add in Vercel Project → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

### Vercel Configuration Files ✅
- `frontend/vercel.json` - Vercel configuration
- `frontend/.env.production` - Production environment
- `frontend/package.json` - Dependencies and build scripts

## 3. Domain Configuration

### Custom Domain (platforge.ai)
1. **Railway**: Add custom domain in Railway dashboard
2. **Vercel**: Add custom domain in Vercel dashboard
3. **DNS**: Point DNS records to deployment URLs

## 4. Testing Deployment

1. **Backend Health Check**: Visit `https://your-railway-app.railway.app/`
2. **Frontend**: Visit your Vercel URL
3. **Integration**: Test auto-provision flow with BigQuery

## 5. Troubleshooting

### Common Issues:
- **Build Failures**: Check logs in Railway/Vercel dashboards
- **TypeScript Errors**: All fixed in latest commits ✅
- **CORS Issues**: Backend configured for all domains ✅
- **API Connection**: Verify NEXT_PUBLIC_API_URL is set correctly

### Railway Backend Issues:
- Check environment variables are set
- Verify GCP service account JSON is valid
- Check Railway logs for Python errors

### Vercel Frontend Issues:
- Verify Next.js build completes successfully
- Check TypeScript compilation (all errors fixed ✅)
- Ensure API URL environment variable is set

## 6. Files Ready for Deployment ✅

### Backend Files:
- ✅ `Dockerfile` - Container configuration
- ✅ `railway.toml` - Railway deployment settings  
- ✅ `requirements.txt` - All dependencies
- ✅ `app.py` - CORS configured for production
- ✅ All Python modules and dependencies

### Frontend Files:
- ✅ `vercel.json` - Vercel configuration
- ✅ `package.json` - Build scripts and dependencies
- ✅ TypeScript interfaces - All errors fixed
- ✅ Environment variable configuration
- ✅ Production API URL configuration

## 7. Expected URLs
- **Backend**: `https://backend-production-xxxx.up.railway.app`
- **Frontend**: `https://platforge-ai-xxxx.vercel.app`
- **Custom**: `https://platforge.ai` (when DNS configured)

## 🎯 Ready for Hackathon Submission!

All deployment configurations are complete and tested. Both services should deploy successfully with these configurations.