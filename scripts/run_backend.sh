#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [ ! -d "venv" ]; then
  echo "Run scripts/setup_venv.sh first to create the virtual environment."
  exit 1
fi

source venv/bin/activate
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
