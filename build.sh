#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "Building QSVM Structure Testing..."
if [ ! -d "python" ]; then
  echo "python/ not found. Run ./setup-python.sh first."
  exit 1
fi
npm run electron:build "$@"
echo ""
echo "Done. Output in dist-electron/"
