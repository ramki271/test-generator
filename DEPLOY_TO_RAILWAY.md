# 🚀 Deploy to Railway

## Quick Deploy Guide

### Prerequisites
- Railway account ([signup here](https://railway.app))
- Your API keys ready (from backend/.env file)

---

## Backend Deployment

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

### 2. Deploy Backend
```bash
cd backend
railway init
railway up
```

### 3. Configure Environment Variables

In Railway Dashboard → Variables, add these variables:

| Variable | Where to Get It |
|----------|-----------------|
| `ANTHROPIC_API_KEY` | From [console.anthropic.com](https://console.anthropic.com) → API Keys |
| `JIRA_URL` | Your JIRA instance URL (e.g., https://yourcompany.atlassian.net) |
| `JIRA_EMAIL` | Your JIRA account email |
| `JIRA_API_TOKEN` | From [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `SERVICE_PORT` | 8000 |
| `LOG_LEVEL` | INFO |
| `ENABLE_JIRA_MCP` | false |

**💡 Tip**: Copy these values from your local `backend/.env` file

### 4. Get Your Backend URL

Railway provides a URL like: `https://your-service.railway.app`

### 5. Test Deployment

```bash
curl https://your-service.railway.app/api/v1/health
```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

```bash
cd frontend
npm i -g vercel
vercel
```

Set environment variable in Vercel:
- `VITE_API_URL` = `https://your-backend.railway.app`

Then redeploy:
```bash
vercel --prod
```

### Option 2: Railway

```bash
cd frontend
railway init
railway up
```

Set in Railway dashboard:
- `VITE_API_URL` = `https://your-backend.railway.app`

**Build Command**: `npm install && npm run build`
**Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

---

## 🎉 Done!

Your application is now live!

- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-backend.railway.app
- **API Docs**: https://your-backend.railway.app/docs

---

## 💰 Costs

- **Railway**: $5/month (Hobby plan) or $5 free credits
- **Vercel**: Free for frontend
- **Claude API**: ~$0.10-0.30 per test case generation

---

## 🔧 Troubleshooting

### Backend won't start
- Check all environment variables are set
- View logs in Railway dashboard
- Ensure Python 3.10+ is available

### Frontend can't connect
- Verify `VITE_API_URL` is correct
- Check CORS is enabled (already configured)
- Test backend health endpoint directly

---

For detailed deployment options, see [backend/DEPLOYMENT.md](backend/DEPLOYMENT.md)
