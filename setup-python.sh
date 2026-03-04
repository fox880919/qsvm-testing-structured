#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "Preparing bundled Python (python-build-standalone)..."
npm run prepare:python
echo ""
echo "Python ready. Run ./build.sh to build the app."
