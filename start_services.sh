#!/usr/bin/env bash
# Start backend (uvicorn) and frontend static server reliably
set -euo pipefail
cd "$(dirname "$0")"

# Load env for backend if exists
if [ -f backend/.env ]; then
  set -o allexport
  # shellcheck disable=SC1091
  source backend/.env
  set +o allexport
fi

# Activate venv if present
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Kill existing processes on ports
lsof -ti :8000 | xargs -r kill -9 || true
lsof -ti :8001 | xargs -r kill -9 || true

# Start backend
echo "Starting FastAPI backend on port 8000..."
nohup bash -lc "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload" > backend/fastapi.log 2>&1 &
BACKEND_PID=$!
sleep 0.8

# Start frontend static server
echo "Starting frontend static server on port 8001..."
nohup python3 -m http.server 8001 --directory . > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

echo "Started backend PID=${BACKEND_PID} frontend PID=${FRONTEND_PID}"
echo "Tail backend logs: backend/fastapi.log"

# Print status
ss -lntp | grep -E ":8000|:8001" || true

exit 0
