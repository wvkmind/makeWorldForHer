#!/bin/bash
# Deploy World Server to VPS
# Usage: bash server/deploy.sh

VPS="root@47.95.178.225"
REMOTE_DIR="/opt/world-server"

echo "=== Deploying World Server ==="

# 1. Create remote directory
ssh $VPS "mkdir -p $REMOTE_DIR"

# 2. Upload server files
scp server/main.py server/models.py server/state.py server/requirements.txt $VPS:$REMOTE_DIR/

# 3. Install dependencies and setup systemd service
ssh $VPS << 'EOF'
cd /opt/world-server

# Install Python if needed
apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv > /dev/null 2>&1

# Create venv
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/world-server.service << 'SERVICE'
[Unit]
Description=World Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/world-server
ExecStart=/opt/world-server/venv/bin/python main.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE

# Start service
systemctl daemon-reload
systemctl enable world-server
systemctl restart world-server
systemctl status world-server --no-pager

echo ""
echo "=== Deployed! ==="
echo "HTTP: http://47.95.178.225:8080/api/state"
echo "WS App: ws://47.95.178.225:8080/ws/app"
echo "WS OpenClaw: ws://47.95.178.225:8080/ws/openclaw"
EOF
