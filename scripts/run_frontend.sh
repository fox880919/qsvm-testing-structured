#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../frontend"

if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

npm run dev
