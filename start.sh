#!/bin/bash
# Feedback Intelligence - Complete Startup Script

echo "🚀 Feedback Intelligence - Startup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    exit 1
fi

echo -e "${BLUE}1. Starting Backend...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Backend ready${NC}"
echo "Starting uvicorn server on http://localhost:8000..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Wait a moment for backend to start
sleep 3

echo ""
echo -e "${BLUE}2. Starting Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install -q
fi

echo -e "${GREEN}✓ Frontend ready${NC}"
echo "Starting Next.js dev server on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo -e "${GREEN}✅ Both services are starting!${NC}"
echo ""
echo "📍 Frontend:  http://localhost:3000"
echo "📍 Backend:   http://localhost:8000"
echo "📍 API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
