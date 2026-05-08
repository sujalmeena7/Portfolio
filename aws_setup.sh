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

cat << 'EOF' > .env
MONGO_URL=mongodb+srv://portfolioUser:EM84vz81%23%23@cluster0.evavgyu.mongodb.net/portfolio_db?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=portfolio_db
JWT_SECRET=x9kP3mR7vL2qQ8sY4wH5nC6bJ1tF9gD0vM3zX8cR
CORS_ORIGINS=*
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=gemini
AI_MODEL=gemini/gemini-1.5-flash
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=720
UPLOAD_DIR=/home/ubuntu/Portfolio/backend/uploads
PUBLIC_UPLOAD_BASE=/api/uploads
EOF

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
