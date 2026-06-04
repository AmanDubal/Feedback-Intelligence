# 🚀 Feedback Intelligence - Complete Setup & Startup Guide

## Quick Start (Recommended)

### Windows
```bash
# Just run this file
start.bat
```

### macOS / Linux
```bash
# Make it executable first
chmod +x start.sh

# Then run it
./start.sh
```

This will automatically:
- ✅ Check environment configuration
- ✅ Install backend dependencies
- ✅ Install frontend dependencies
- ✅ Start the backend server (port 8000)
- ✅ Start the frontend server (port 3000)
- ✅ Open the dashboard

---

## Manual Setup (Step by Step)

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### 1. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual configuration
# Windows:
notepad .env

# macOS/Linux:
nano .env
```

**Important variables to configure:**
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)
- `NEXT_PUBLIC_API_URL` - Should be `http://localhost:8000` for local development
- `DATABASE_URL` - Default is fine for development: `sqlite:///./feedback.db`

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload
```

**Backend will be available at:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### 3. Frontend Setup (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

---

## 🔍 Verification Checklist

After startup, verify everything is working:

### Backend Checks
```bash
# 1. Check health endpoint
curl http://localhost:8000/health

# 2. View API documentation
# Open in browser: http://localhost:8000/docs

# 3. Check root endpoint
curl http://localhost:8000/
```

**Expected responses:**
- Health: `{"status": "healthy"}`
- Root: Shows API info with version

### Frontend Checks
1. Open http://localhost:3000 in your browser
2. You should see the Feedback Intelligence dashboard
3. Check that the integrations page loads
4. Verify navigation works

### Connection Check
1. On the frontend, go to any page that makes an API call
2. Open browser DevTools (F12)
3. Check Network tab - should see requests to `http://localhost:8000/api/v1/...`
4. Responses should show 200 status codes

---

## 📊 Available Endpoints

### Core API Routes

**Feedback Management**
- `GET /api/v1/feedback` - List all feedback
- `POST /api/v1/feedback` - Create new feedback
- `GET /api/v1/feedback/{id}` - Get feedback details

**Analysis**
- `GET /api/v1/analysis/dashboard` - Dashboard metrics
- `GET /api/v1/analysis/clusters` - Feedback clusters
- `GET /api/v1/analysis/trends` - Trend analysis

**Integrations**
- `POST /api/v1/integrations/sources/register` - Register feedback source
- `POST /api/v1/integrations/feedback/ingest` - Ingest feedback batch
- `POST /api/v1/integrations/feedback/upload` - Upload feedback file (CSV/JSON)
- `GET /api/v1/integrations/sync/status` - Sync status
- `POST /api/v1/integrations/sync/manual` - Trigger manual sync

**System**
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

---

## 🆘 Troubleshooting

### Backend won't start

**Error: "Cannot find module python"**
- Ensure Python is in your PATH
- Run `python --version` to verify installation

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Error: "Port 8000 already in use"**
- Find and kill the process:
  ```bash
  # Windows:
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # macOS/Linux:
  lsof -i :8000
  kill -9 <PID>
  ```

### Frontend won't start

**Error: "npm command not found"**
- Install Node.js from https://nodejs.org/

**Error: "npm ERR! 404"**
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

**Error: "Port 3000 already in use"**
- Find and kill the process:
  ```bash
  # Windows:
  netstat -ano | findstr :3000
  taskkill /PID <PID> /F
  
  # macOS/Linux:
  lsof -i :3000
  kill -9 <PID>
  ```

### API connection issues

**Frontend shows "Cannot connect to API"**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env` is correct
- Restart frontend: `npm run dev`

**CORS errors in browser console**
- Check backend config in `backend/app/main.py`
- Ensure `http://localhost:3000` is in CORS origins

### Database errors

**Error: "no such table"**
- The database is created on first startup
- If issues persist, delete `feedback.db` and restart

### Configuration errors

**Error reading .env file**
- Ensure `.env` file exists (not `.env.example`)
- Check file permissions are readable
- Verify syntax: `KEY=value` format

---

## 📁 Project Structure

```
feedback-intelligence/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app setup
│   │   ├── config.py          # Configuration
│   │   ├── api/               # API routes
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utilities
│   ├── requirements.txt        # Python dependencies
│   └── venv/                  # Virtual environment (created on setup)
│
├── frontend/                   # Next.js React frontend
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities
│   │   └── types/             # TypeScript types
│   ├── package.json           # Node dependencies
│   └── node_modules/          # Installed packages (created on setup)
│
├── .env                        # Environment configuration (local, not committed)
├── .env.example               # Configuration template (committed)
├── .gitignore                 # Git ignore rules
├── start.sh                   # Linux/macOS startup script
├── start.bat                  # Windows startup script
├── SETUP.md                   # This file
└── README.md                  # Project documentation
```

---

## 🚀 Production Deployment

### Build for Production

**Backend:**
```bash
# Create production build
cd backend
pip install -r requirements.txt
# Backend is ready to run with any ASGI server
```

**Frontend:**
```bash
# Create optimized production build
cd frontend
npm run build
npm start  # Or deploy to Vercel, Netlify, etc.
```

### Docker Deployment

```bash
docker-compose up -d
```

---

## 💡 Tips & Tricks

### Clear everything and start fresh
```bash
# Remove dependencies
rm -rf backend/venv
rm -rf frontend/node_modules

# Remove generated files
rm -f feedback.db
rm -rf backend/.pytest_cache
rm -rf backend/__pycache__

# Then run setup again
./start.sh  # or start.bat
```

### Run only backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

### Run only frontend
```bash
cd frontend
npm run dev
```

### Access logs in real-time
```bash
# Backend logs appear in terminal where uvicorn is running
# Frontend logs appear in terminal where npm run dev is running
```

---

## 📞 Support

If you encounter issues:
1. Check this troubleshooting section
2. Verify environment configuration (`.env`)
3. Check that ports 3000 and 8000 are available
4. Ensure Python 3.8+ and Node.js 16+ are installed
5. Try clearing cache and reinstalling dependencies

---

**Happy analyzing feedback!** 🎉
