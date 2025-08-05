#!/bin/bash

echo "🚀 PlatForge.ai Deployment Script"
echo "=================================="

# Backend Railway Deployment
echo "1. Backend Deployment to Railway"
echo "Please run these commands manually:"
echo ""
echo "cd backend"
echo "railway login"
echo "railway init"
echo "railway up"
echo ""
echo "Set these environment variables in Railway dashboard:"
echo "GOOGLE_APPLICATION_CREDENTIALS_JSON=<your-service-account-json>"
echo "PORT=8001"
echo ""

# Frontend Vercel Deployment  
echo "2. Frontend Deployment to Vercel"
echo "Please run these commands manually:"
echo ""
echo "cd frontend"
echo "npx vercel login"
echo "npx vercel --prod"
echo ""
echo "Set this environment variable in Vercel dashboard:"
echo "NEXT_PUBLIC_API_URL=<your-railway-backend-url>"
echo ""

echo "✅ Deployment guide ready!"