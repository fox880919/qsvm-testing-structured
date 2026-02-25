#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

echo "Using Python: $(python3 --version)"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r api/requirements.txt
echo ""
echo "Virtual environment ready. Activate with:"
echo "  source venv/bin/activate"
