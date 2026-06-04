# Multi-stage Dockerfile for Feedback Intelligence
# This Dockerfile builds both backend and frontend services

# ============================================
# Stage 1: Build Backend
# ============================================
FROM python:3.11-slim as backend-builder

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# ============================================
# Stage 2: Build Frontend
# ============================================
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# ============================================
# Stage 3: Runtime - Start with Python
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Copy Python runtime from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /app/backend ./backend

# Install Node for serving frontend (minimal)
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy frontend build
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package*.json ./frontend/

# Install frontend production deps
WORKDIR /app/frontend
RUN npm ci --only=production

# Expose ports
EXPOSE 3000 8000

# Start both services (requires process manager or separate containers recommended)
WORKDIR /app

# Create startup script
RUN echo '#!/bin/bash\ncd /app/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 &\ncd /app/frontend && npm start' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]
