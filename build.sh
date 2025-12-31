#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting Build Process ==="
echo "Current directory: $(pwd)"

# --- Backend Setup ---
echo ">>> Installing backend dependencies..."
pip install -r requirements.txt

# --- Install Node.js if not available ---
echo ">>> Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo ">>> Node.js not found. Installing via nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 20
    nvm use 20
fi

echo ">>> Node version: $(node --version)"
echo ">>> NPM version: $(npm --version)"

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
