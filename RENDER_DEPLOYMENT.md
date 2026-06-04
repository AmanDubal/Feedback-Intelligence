# Deploy on Render Cloud Platform

Complete guide to deploy **Feedback Intelligence** on [Render](https://render.com) - a modern cloud platform.

---

## 📋 Prerequisites

1. **Render Account**: Create free account at [render.com](https://render.com)
2. **GitHub Repository**: Push your project to GitHub
3. **OpenAI API Key**: Get from [platform.openai.com](https://platform.openai.com)
4. Credit card (for paid resources - free tier available for testing)

---

## 🚀 Quick Deploy (5 minutes)

### **Option 1: One-Click Deploy with render.yaml** (Recommended)

This is the easiest approach - Render reads `render.yaml` and sets up everything automatically.

#### Step 1: Connect GitHub to Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Select your `feedback-intelligence` repository

#### Step 2: Configure Environment Variables
Render will automatically create services from `render.yaml`. Before deploying, you'll set environment variables:

1. In the Render dashboard, go to **Environment Variables**
2. Add these variables:

```env
# Frontend
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com

# Backend
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
OPENAI_API_KEY=sk-...your-key...
SECRET_KEY=generate-a-random-secret-key-here
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend.onrender.com
```

**How to get DATABASE_URL:**
- Render creates a PostgreSQL database automatically
- Copy the "External Database URL" from your PostgreSQL service settings

#### Step 3: Deploy
1. Click **"Deploy"**
2. Render builds and deploys both frontend and backend automatically
3. Wait for green checkmarks (5-10 minutes)
4. Access your app via the provided URLs

---

### **Option 2: Manual Setup**

If you prefer manual control over each service:

#### Step 1: Deploy PostgreSQL Database

1. **New Service** → **PostgreSQL**
2. Configure:
   - **Name**: `feedback-intelligence-db`
   - **Region**: Choose closest to users
   - **PostgreSQL Version**: 15
3. Click **Create Database**
4. Copy the connection URL (you'll need this)

#### Step 2: Deploy Backend (FastAPI)

1. **New Service** → **Web Service**
2. Connect GitHub repository
3. Configure:
   - **Name**: `feedback-intelligence-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Same as database

4. **Environment Variables** (add these):
   ```env
   DATABASE_URL=postgresql://username:password@hostname:5432/dbname
   OPENAI_API_KEY=sk-...your-key...
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

5. Click **Create Web Service**
6. Wait for deployment (3-5 minutes)

#### Step 3: Deploy Frontend (Next.js)

1. **New Service** → **Web Service**
2. Connect GitHub repository
3. Configure:
   - **Name**: `feedback-intelligence-web`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build --prefix frontend`
   - **Start Command**: `npm run start --prefix frontend`
   - **Region**: Same as backend

4. **Environment Variables**:
   ```env
   NEXT_PUBLIC_API_URL=https://feedback-intelligence-api.onrender.com
   ```

5. Click **Create Web Service**
6. Wait for deployment

---

## 🗄️ Database Migration

**Important**: SQLite won't work on Render (ephemeral filesystem). You must use PostgreSQL.

### Automatic Migration

The backend will automatically:
1. Create tables on first run
2. Migrate data if you're moving from existing SQLite database

### Manual Migration (if needed)

```bash
# Export data from local SQLite
sqlite3 feedback.db ".dump" > backup.sql

# Connect to PostgreSQL and import
psql -U username -d dbname -f backup.sql
```

---

## 🔧 Configuration for Production

### Update `.env` for production:

```env
# Frontend
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com

# Backend
DATABASE_URL=postgresql://user:password@your-db.onrender.com:5432/feedback_db
OPENAI_API_KEY=sk-...your-openai-key...
SECRET_KEY=generate-strong-random-key
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend.onrender.com
```

### Generate SECRET_KEY:
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 📊 Access Your Application

After deployment succeeds:

- **Frontend**: `https://your-app-name.onrender.com`
- **Backend API**: `https://your-api-name.onrender.com`
- **API Docs**: `https://your-api-name.onrender.com/docs`
- **Database**: Access via connection string in Render dashboard

---

## 💰 Cost Estimation

| Service | Free Tier | Paid | Notes |
|---------|-----------|------|-------|
| Web Service (Backend) | $0 (pauses after 15 min inactivity) | $7/month | Always-on recommended |
| Web Service (Frontend) | $0 (pauses) | $7/month | Always-on recommended |
| PostgreSQL | $7/month | $15+/month | Includes 1GB storage |
| **Total** | ~$7/month | ~$29/month | Minimum production setup |

---

## 🚨 Troubleshooting

### **Backend won't start**
- Check logs: Click service → **Logs** tab
- Verify DATABASE_URL is correct
- Verify OPENAI_API_KEY is set
- Try: `python -m pip install -r backend/requirements.txt`

### **Frontend can't reach backend**
- Verify `NEXT_PUBLIC_API_URL` matches backend URL
- Check backend is running: Visit `/docs` endpoint
- Check CORS settings in backend config

### **Database connection failed**
- Verify connection string format
- Use "External Database URL" not "Internal"
- Wait 2-3 minutes after database creation
- Restart services

### **Build fails**
- Check build logs for errors
- Verify paths (backend/, frontend/)
- Ensure Node/Python versions supported

### **App keeps restarting**
- Check logs for crash errors
- Increase memory: Render console → Service settings
- Scale to at least $7/month plan

---

## 📈 Scaling Tips

1. **Enable Auto-Scaling**: Service settings → Scale plan
2. **Use CDN**: Add Cloudflare for static content caching
3. **Add Redis Cache**: For session management
4. **Upgrade Database**: PostgreSQL paid tier for better performance
5. **Monitor Performance**: Render console → Metrics

---

## 🔒 Security Best Practices

- ✅ Use strong SECRET_KEY (generate with `secrets` module)
- ✅ Never commit `.env` to GitHub
- ✅ Use environment variables for all secrets
- ✅ Enable CORS only for your domain
- ✅ Use HTTPS (automatic on Render)
- ✅ Keep OpenAI API key private
- ✅ Regular database backups

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **GitHub Issues**: Add issue to your repository
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs

---

## ✅ Post-Deployment Checklist

- [ ] Both services show "Live" status (green)
- [ ] Frontend loads without errors
- [ ] Can access API docs at `/docs`
- [ ] Can upload feedback via UI
- [ ] Analysis results display correctly
- [ ] No 503 errors in logs
- [ ] Database contains sample data
- [ ] Email alerts configured (if applicable)

---

**You're live on Render! 🎉**
