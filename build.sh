#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting Build Process ==="
echo "Current directory: $(pwd)"

# --- Backend Setup ---
echo ">>> Installing backend dependencies..."
pip install -r requirements.txt

# --- Frontend Setup ---
echo ">>> Building frontend..."
cd frontend
echo "Frontend directory: $(pwd)"
npm install
npm run build

echo ">>> Verifying frontend build..."
ls -la dist/
cd ..

echo "=== Build Complete! ==="
