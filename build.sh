#!/usr/bin/env bash
# exit on error
set -o errexit

# --- Backend Setup ---
echo "Installing backend dependencies..."
pip install -r requirements.txt

# --- Frontend Setup ---
echo "Building frontend..."
pushd frontend
npm install
npm run build
popd

echo "Build complete!"
