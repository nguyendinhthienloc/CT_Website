#!/usr/bin/env bash
set -euo pipefail

# Create virtualenv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Edit .env to add your OPENWEATHERMAP_KEY."
  else
    echo "No .env.example found; create backend/.env with OPENWEATHERMAP_KEY."
  fi
fi

echo "Virtualenv created in .venv and dependencies installed. Run: source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
