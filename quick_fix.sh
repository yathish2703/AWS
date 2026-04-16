#!/bin/bash

#############################################
# Quick Fix Script - Resolves Common Issues
# Run this if deployment failed
#############################################

set +e  # Don't exit on errors

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_NAME="aws-learning-platform"
APP_DIR="/opt/$APP_NAME"
APP_USER="webapp"

echo -e "${BLUE}=========================================="
echo "  Quick Fix Script"
echo "==========================================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Ensuring all directories exist...${NC}"
sudo -u $APP_USER mkdir -p $APP_DIR/data/lessons/00-cloud-basics
sudo -u $APP_USER mkdir -p $APP_DIR/data/quizzes
sudo -u $APP_USER mkdir -p $APP_DIR/data/challenges
sudo -u $APP_USER mkdir -p $APP_DIR/data/users
sudo -u $APP_USER mkdir -p $APP_DIR/logs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

echo -e "${GREEN}Step 2: Fixing permissions...${NC}"
chown -R $APP_USER:$APP_USER $APP_DIR
chmod +x $APP_DIR/app.py 2>/dev/null || true
echo -e "${GREEN}✓ Permissions fixed${NC}"
echo ""

echo -e "${GREEN}Step 3: Ensuring Python packages are installed...${NC}"
cd $APP_DIR

# Check if venv exists
if [ ! -d "$APP_DIR/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    sudo -u $APP_USER python3 -m venv $APP_DIR/venv
fi

echo -e "${YELLOW}Upgrading pip...${NC}"
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip

echo -e "${YELLOW}Installing/upgrading Flask and dependencies...${NC}"
if [ -f "$APP_DIR/requirements.txt" ]; then
    sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt
else
    # Install core dependencies manually
    sudo -u $APP_USER $APP_DIR/venv/bin/pip install Flask==3.0.2 Flask-CORS==4.0.0 Werkzeug==3.0.1 markdown2==2.5.5
fi
echo -e "${GREEN}✓ Packages installed${NC}"
echo ""

echo -e "${GREEN}Step 4: Killing any processes on port 5001...${NC}"
if lsof -t -i:5001 > /dev/null 2>&1; then
    lsof -t -i:5001 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓ Port 5001 cleared${NC}"
else
    echo -e "${GREEN}✓ Port 5001 already free${NC}"
fi
echo ""

echo -e "${GREEN}Step 5: Testing Python application...${NC}"
cd $APP_DIR
timeout 3 sudo -u $APP_USER $APP_DIR/venv/bin/python -c "from flask import Flask; print('Flask import: OK')" && echo -e "${GREEN}✓ Flask works${NC}" || echo -e "${RED}✗ Flask import failed${NC}"
timeout 3 sudo -u $APP_USER $APP_DIR/venv/bin/python -c "import config; print('Config import: OK')" && echo -e "${GREEN}✓ Config works${NC}" || echo -e "${RED}✗ Config import failed${NC}"
echo ""

echo -e "${GREEN}Step 6: Restarting systemd service...${NC}"
systemctl daemon-reload
systemctl stop $APP_NAME 2>/dev/null || true
sleep 2
systemctl start $APP_NAME

# Wait for service to start
sleep 3

echo -e "${GREEN}Step 7: Checking service status...${NC}"
if systemctl is-active --quiet $APP_NAME; then
    echo -e "${GREEN}✓ Service is running!${NC}"
    systemctl status $APP_NAME --no-pager | head -10
else
    echo -e "${RED}✗ Service failed to start${NC}"
    echo ""
    echo -e "${YELLOW}Last 15 lines of logs:${NC}"
    journalctl -u $APP_NAME -n 15 --no-pager
    echo ""
    echo -e "${YELLOW}Try running the troubleshoot script:${NC}"
    echo "  sudo bash troubleshoot.sh"
fi
echo ""

echo -e "${GREEN}Step 8: Testing local connection...${NC}"
sleep 2
if curl -s http://localhost:5001 > /dev/null; then
    echo -e "${GREEN}✓ Application responds on port 5001${NC}"
else
    echo -e "${YELLOW}⚠ Application not responding yet (may need more time)${NC}"
fi
echo ""

echo -e "${BLUE}=========================================="
echo "  Summary"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Check status: sudo systemctl status $APP_NAME"
echo "2. View logs: sudo journalctl -u $APP_NAME -f"
echo "3. If still failing, run: sudo bash troubleshoot.sh"
echo ""
echo "Your app should be at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'YOUR-EC2-IP')"
echo ""
