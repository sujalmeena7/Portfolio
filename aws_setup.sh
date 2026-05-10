#!/bin/bash
set -e

echo "Waiting for apt locks to release..."
while sudo fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do
    sleep 1
done

echo "Updating packages..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing dependencies..."
sudo apt install -y python3-pip python3-venv git curl

echo "Installing Node.js and PM2..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install pm2 -g

echo "Cloning repository..."
cd /home/ubuntu
if [ ! -d "Portfolio" ]; then
    git clone https://github.com/sujalmeena7/Portfolio.git
else
    cd Portfolio
    git pull origin main
    cd ..
fi

echo "Setting up backend environment..."
cd /home/ubuntu/Portfolio/backend

# ── Write .env from environment variables (set these on your server beforehand) ──
# Required env vars: MONGO_URL, JWT_SECRET, GEMINI_API_KEY
# Optional: DB_NAME, CORS_ORIGINS, AI_PROVIDER, AI_MODEL, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
if [ -f .env ]; then
    echo ".env already exists — skipping creation. Edit manually if needed."
else
    cat << EOF > .env
MONGO_URL=${MONGO_URL:?Set MONGO_URL before running this script}
DB_NAME=${DB_NAME:-portfolio_db}
JWT_SECRET=${JWT_SECRET:?Set JWT_SECRET before running this script}
CORS_ORIGINS=${CORS_ORIGINS:-*}
GEMINI_API_KEY=${GEMINI_API_KEY:?Set GEMINI_API_KEY before running this script}
AI_PROVIDER=${AI_PROVIDER:-gemini}
AI_MODEL=${AI_MODEL:-gemini/gemini-2.0-flash}
JWT_ALGORITHM=${JWT_ALGORITHM:-HS256}
JWT_EXPIRE_MINUTES=${JWT_EXPIRE_MINUTES:-720}
UPLOAD_DIR=/home/ubuntu/Portfolio/backend/uploads
PUBLIC_UPLOAD_BASE=/api/uploads
EOF
    echo ".env created successfully."
fi

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Starting backend with PM2..."
pm2 delete portfolio-backend || true
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8000" --name portfolio-backend
pm2 save
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u ubuntu --hp /home/ubuntu

echo "Setup Complete!"
