# Vercel Deployment Guide

## Problem: 404 NOT_FOUND Error

When deploying a React SPA (Single Page Application) to Vercel, you get a 404 error because:

1. **SPA Routing Issue**: React apps use client-side routing. When you navigate to a route like `/events`, Vercel tries to find a file at that path, but it doesn't exist. The server needs to serve `index.html` for all routes.

2. **Missing Configuration**: Vercel needs a `vercel.json` file to tell it how to handle SPA routing.

## Solution

### 1. Root Cause

**What was happening:**
- Vercel receives a request for `/` → serves `index.html` ✅
- Vercel receives a request for `/events` → looks for `/events/index.html` → 404 ❌
- React Router expects the server to serve `index.html` for ALL routes

**What it needed to do:**
- Vercel should serve `index.html` for ALL routes, letting React handle routing client-side

### 2. The Fix

Created `frontend/vercel.json` with rewrite rules:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This tells Vercel: "For any route, serve `/index.html`" - allowing React to handle routing.

### 3. Deployment Steps

#### Option A: Deploy Frontend Only (Recommended for now)

1. **Deploy Frontend to Vercel:**
   ```bash
   cd frontend
   vercel
   ```

2. **Set Environment Variable:**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `VITE_API_URL` = `http://your-backend-url:8000` (or your deployed backend URL)

3. **Redeploy** after adding environment variables

#### Option B: Deploy Both Frontend and Backend

**Backend (FastAPI):**
- Deploy to Railway, Render, or another Python hosting service
- Or use Vercel Serverless Functions (more complex)

**Frontend:**
- Deploy to Vercel as above
- Set `VITE_API_URL` to your backend URL

### 4. Important Configuration

**Build Settings in Vercel:**
- **Framework Preset**: Vite
- **Root Directory**: `frontend` (if deploying from root)
- **Build Command**: `npm run build` (runs in frontend directory)
- **Output Directory**: `dist`

**Environment Variables:**
- `VITE_API_URL`: Your backend API URL (e.g., `https://your-backend.railway.app`)

### 5. Understanding the Concept

**Why does this error exist?**
- Traditional web servers serve files from the filesystem
- SPAs use JavaScript to render different "pages" client-side
- The server needs to know: "Serve the same HTML file for all routes"

**Mental Model:**
- **Server-side routing**: `/about` → server looks for `/about/index.html`
- **Client-side routing**: `/about` → server serves `/index.html`, React shows About component

**Vercel's Rewrite Rules:**
- `rewrites` = URL rewriting (keeps the URL, changes what's served)
- `redirects` = URL redirection (changes the URL)
- For SPAs, we use `rewrites` to serve `index.html` for all routes

### 6. Warning Signs

**Look out for:**
- ✅ 404 errors on routes other than `/`
- ✅ App works locally but not on Vercel
- ✅ Direct URL access fails, but navigation works
- ✅ Missing `vercel.json` or routing configuration

**Similar mistakes:**
- Forgetting to configure routing in other hosting services (Netlify, AWS S3, etc.)
- Not setting up API proxy correctly
- Hardcoding `localhost` URLs in production code

### 7. Alternative Approaches

**Option 1: Vercel Rewrites (Current Solution)**
- ✅ Simple, works for all SPAs
- ✅ No code changes needed
- ❌ Requires `vercel.json` file

**Option 2: Vercel Redirects**
- Similar but uses redirects instead of rewrites
- Less ideal for SPAs (changes URL)

**Option 3: Server-Side Rendering (SSR)**
- Use Next.js instead of React
- More complex but better for SEO
- Overkill for this project

**Option 4: Hash Routing**
- Use `/#/events` instead of `/events`
- Works without server configuration
- ❌ Ugly URLs, not recommended

### 8. Testing After Deployment

1. **Check Homepage**: `https://your-app.vercel.app/` should work
2. **Check Direct Routes**: `https://your-app.vercel.app/events` should work (not 404)
3. **Check API Calls**: Open browser console, verify API calls go to correct backend
4. **Check Environment Variables**: Verify `VITE_API_URL` is set correctly

### 9. Common Issues

**Issue**: Still getting 404 after adding `vercel.json`
- **Fix**: Make sure `vercel.json` is in the `frontend` directory (or root if deploying from root)
- **Fix**: Redeploy after adding the file

**Issue**: API calls failing
- **Fix**: Set `VITE_API_URL` environment variable in Vercel
- **Fix**: Make sure backend CORS allows your Vercel domain

**Issue**: Build fails
- **Fix**: Check build logs in Vercel dashboard
- **Fix**: Make sure all dependencies are in `package.json`

## Quick Fix Summary

1. ✅ Created `frontend/vercel.json` with rewrite rules
2. ✅ Updated API configuration to use environment variables
3. ⚠️ **You need to**: Set `VITE_API_URL` in Vercel environment variables
4. ⚠️ **You need to**: Deploy your backend separately (Railway, Render, etc.)

After deploying, your app should work correctly!

