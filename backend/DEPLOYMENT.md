# Deployment Guide

## 🚀 Deploy to Railway (Recommended)

Railway.app provides the easiest deployment experience for both backend and frontend.

### Prerequisites
- Railway account (sign up at [railway.app](https://railway.app))
- GitHub account (optional but recommended)
- Your API keys ready

---

## Backend Deployment (FastAPI Microservice)

### Step 1: Create New Project
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo" (recommended) or "Empty Project"

### Step 2: Configure Service

If using GitHub:
1. Connect your GitHub account
2. Select the `test-case-generator-service` repository
3. Railway will auto-detect the Dockerfile

If using Empty Project:
1. Click "New" → "GitHub Repo"
2. Or use Railway CLI: `railway link`

### Step 3: Set Environment Variables

In Railway Dashboard → Variables, add:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
JIRA_URL=https://artemishealth.atlassian.net
JIRA_EMAIL=rsridar@artemishealth.com
JIRA_API_TOKEN=ATATT3xFfGF...
SERVICE_PORT=8000
LOG_LEVEL=INFO
ENABLE_JIRA_MCP=false
```

**Important Notes:**
- Railway automatically provides `$PORT` variable
- The service will be available at: `https://your-service.railway.app`
- Health check endpoint: `/api/v1/health`

### Step 4: Deploy

Railway will automatically build and deploy your service.

**Build Process:**
1. Detects `Dockerfile`
2. Installs Python dependencies
3. Builds container
4. Deploys to Railway infrastructure

**Deployment URL:**
After deployment, you'll get a URL like:
```
https://test-case-generator-production.railway.app
```

### Step 5: Verify Deployment

Test your deployment:
```bash
curl https://your-service.railway.app/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "test-case-generator",
  "version": "1.0.0"
}
```

---

## Frontend Deployment (React App)

### Option 1: Deploy to Railway

1. **Create New Service** in the same Railway project
2. **Connect Frontend Repo**
   ```bash
   cd ../test-case-generator-ui
   git init
   git add .
   git commit -m "Initial commit"
   # Push to GitHub
   ```

3. **Configure Build Settings:**
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`

4. **Set Environment Variable:**
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

5. **Deploy:** Railway will build and serve your React app

### Option 2: Deploy to Vercel (Easier for React)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd test-case-generator-ui
   vercel
   ```

3. **Set Environment Variable:**
   In Vercel dashboard:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

4. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Option 3: Deploy to Netlify

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Build:**
   ```bash
   cd test-case-generator-ui
   npm run build
   ```

3. **Deploy:**
   ```bash
   netlify deploy --prod --dir=dist
   ```

4. **Set Environment:**
   In Netlify dashboard → Site settings → Environment variables:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```

---

## Alternative Deployment Options

### Google Cloud Run

**Backend:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/test-case-generator

# Deploy
gcloud run deploy test-case-generator \
  --image gcr.io/PROJECT_ID/test-case-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=...,JIRA_URL=...,JIRA_EMAIL=...,JIRA_API_TOKEN=...
```

**Frontend:**
Deploy to Firebase Hosting or Cloud Storage + Cloud CDN

### AWS

**Backend:** ECS/Fargate or Elastic Beanstalk
**Frontend:** S3 + CloudFront or Amplify

### Heroku

**Backend:**
```bash
heroku create test-case-generator-api
heroku config:set ANTHROPIC_API_KEY=...
heroku config:set JIRA_URL=...
heroku config:set JIRA_EMAIL=...
heroku config:set JIRA_API_TOKEN=...
git push heroku main
```

---

## Cost Estimates

### Railway.app
- **Free Tier**: $5 credit/month
- **Hobby Plan**: $5/month (500 execution hours)
- **Typical Usage**: Backend ~$3-5/month, Frontend ~$0-2/month

### Vercel/Netlify (Frontend Only)
- **Free Tier**: Generous (perfect for frontend)
- **Bandwidth**: 100GB/month free
- **Builds**: Unlimited

### Google Cloud Run
- **Pricing**: Pay per use
- **Typical Cost**: $0.10-1.00/month for low traffic
- **Free Tier**: 2 million requests/month

---

## Post-Deployment Configuration

### 1. Update Frontend API URL

After backend deployment, update frontend:

**Railway/Vercel/Netlify:**
Set environment variable:
```
VITE_API_URL=https://your-actual-backend-url.railway.app
```

**Local Development:**
Create `.env.local`:
```
VITE_API_URL=http://localhost:8000
```

### 2. Test End-to-End

1. **Health Check:**
   ```bash
   curl https://your-backend.railway.app/api/v1/health
   ```

2. **Generate Test Cases:**
   ```bash
   curl -X POST https://your-backend.railway.app/api/v1/generate-test-cases \
     -H "Content-Type: application/json" \
     -d '{
       "manual_input": {
         "title": "Test Feature",
         "description": "Test",
         "acceptance_criteria": ["Test"]
       },
       "test_types": ["functional"]
     }'
   ```

3. **Open Frontend:**
   Visit `https://your-frontend-url.vercel.app`

### 3. Monitor Logs

**Railway:**
- Dashboard → Service → Logs

**Google Cloud:**
```bash
gcloud logging read "resource.type=cloud_run_revision"
```

---

## Troubleshooting

### Backend Issues

**"ProcessTransport is not ready":**
- This is expected with Railway/cloud deployments
- The async generator workaround is already implemented
- If issues persist, check logs for specific errors

**CORS Errors:**
- Verify CORS is configured in `app/main.py`
- Ensure frontend is using correct backend URL

**Authentication Errors:**
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check JIRA credentials if using JIRA integration

### Frontend Issues

**"Failed to fetch":**
- Check `VITE_API_URL` environment variable
- Verify backend is running and accessible
- Check browser console for CORS errors

**Build Failures:**
- Ensure all dependencies are installed
- Check Node version (should be 18+)
- Clear `node_modules` and reinstall

---

## Security Considerations

### Production Checklist

- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on Railway/Vercel/Netlify)
- [ ] Rotate API keys regularly
- [ ] Monitor API usage and costs
- [ ] Set up rate limiting (optional)
- [ ] Configure proper CORS origins (change from `["*"]` to specific domains)
- [ ] Enable logging and monitoring
- [ ] Set up alerts for errors

### Recommended CORS Update for Production

In `app/main.py`, update CORS after deployment:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "https://your-frontend.railway.app",
        "http://localhost:5173"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Scaling Considerations

### When to Scale

Monitor these metrics:
- Response times > 30 seconds
- Error rates > 5%
- Resource usage > 80%

### Scaling Options

**Railway:**
- Upgrade to Pro plan
- Increase replicas
- Add more memory/CPU

**Horizontal Scaling:**
- Deploy multiple backend instances
- Use load balancer
- Implement request queue

**Optimization:**
- Cache frequent requests
- Optimize Claude Agent SDK configuration
- Use CDN for frontend assets

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway link ${{ secrets.RAILWAY_PROJECT_ID }}
          railway up
```

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Claude Agent SDK**: https://docs.anthropic.com/agent-sdk
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

## Quick Start Commands

```bash
# Backend (Railway)
cd test-case-generator-service
railway login
railway init
railway up

# Frontend (Vercel)
cd test-case-generator-ui
vercel

# Local Development
# Terminal 1 - Backend
cd test-case-generator-service
python3.11 -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd test-case-generator-ui
npm run dev
```

---

**Your microservice is ready for deployment! 🎉**
