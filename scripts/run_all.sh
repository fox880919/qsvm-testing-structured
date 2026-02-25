#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [ -f "$HOME/.nvm/nvm.sh" ] && [ -f .nvmrc ]; then
  source "$HOME/.nvm/nvm.sh"
  nvm use 2>/dev/null || nvm install
fi

NODE_VER=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)
if [ -z "$NODE_VER" ] || [ "$NODE_VER" -lt 20 ]; then
  echo "Node.js 20+ required (current: $(node -v 2>/dev/null || echo 'not found'))."
  echo "Install: nvm install 20 && nvm use 20   (or: brew install node@20)"
  exit 1
fi

if [ ! -d "venv" ]; then
  echo "Run ./scripts/setup_venv.sh first."
  exit 1
fi

[ ! -d "node_modules" ] && npm install
[ ! -d "frontend/node_modules" ] && (cd frontend && npm install)
echo "Backend: http://localhost:8000 | Frontend: http://localhost:5173"
echo ""
npm start
