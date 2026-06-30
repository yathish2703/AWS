#!/bin/bash

#############################################
# Troubleshooting Script for Failed Start
# Run this to diagnose deployment issues
#############################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_NAME="aws-learning-platform"
APP_DIR="/opt/$APP_NAME"
APP_USER="webapp"

echo -e "${BLUE}=========================================="
echo "  AWS Learning Platform Troubleshooter"
echo "==========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}Gathering diagnostic information...${NC}"
echo ""

# 1. Check if directory exists
echo -e "${BLUE}[1] Checking application directory...${NC}"
if [ -d "$APP_DIR" ]; then
    echo -e "${GREEN}✓ Directory exists: $APP_DIR${NC}"
    ls -la $APP_DIR | head -10
else
    echo -e "${RED}✗ Directory not found: $APP_DIR${NC}"
    exit 1
fi
echo ""

# 2. Check if user exists
echo -e "${BLUE}[2] Checking application user...${NC}"
if id -u $APP_USER > /dev/null 2>&1; then
    echo -e "${GREEN}✓ User exists: $APP_USER${NC}"
else
    echo -e "${RED}✗ User not found: $APP_USER${NC}"
fi
echo ""

# 3. Check Python and venv
echo -e "${BLUE}[3] Checking Python environment...${NC}"
if [ -f "$APP_DIR/venv/bin/python" ]; then
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
    $APP_DIR/venv/bin/python --version
else
    echo -e "${RED}✗ Virtual environment not found${NC}"
fi
echo ""

# 4. Check if app.py exists
echo -e "${BLUE}[4] Checking application files...${NC}"
if [ -f "$APP_DIR/app.py" ]; then
    echo -e "${GREEN}✓ app.py found${NC}"
else
    echo -e "${RED}✗ app.py not found${NC}"
fi

if [ -f "$APP_DIR/requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt found${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt not found${NC}"
fi
echo ""

# 5. Check systemd service
echo -e "${BLUE}[5] Checking systemd service...${NC}"
if systemctl list-unit-files | grep -q $APP_NAME; then
    echo -e "${GREEN}✓ Service file exists${NC}"
    systemctl status $APP_NAME --no-pager | head -15
else
    echo -e "${RED}✗ Service not found${NC}"
fi
echo ""

# 6. Check last 20 lines of service logs
echo -e "${BLUE}[6] Recent service logs (last 20 lines):${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"
journalctl -u $APP_NAME -n 20 --no-pager
echo -e "${YELLOW}----------------------------------------${NC}"
echo ""

# 7. Try to run Python directly to see errors
echo -e "${BLUE}[7] Testing Python application directly...${NC}"
echo -e "${YELLOW}Attempting to run app.py (will timeout after 5 seconds)...${NC}"
cd $APP_DIR
timeout 5 sudo -u $APP_USER $APP_DIR/venv/bin/python $APP_DIR/app.py 2>&1 || true
echo ""

# 8. Check for port conflicts
echo -e "${BLUE}[8] Checking port 5001...${NC}"
if lsof -i :5001 > /dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":5001 "; then
    echo -e "${YELLOW}⚠ Something is already using port 5001:${NC}"
    lsof -i :5001 2>/dev/null || netstat -tulpn 2>/dev/null | grep ":5001"
else
    echo -e "${GREEN}✓ Port 5001 is available${NC}"
fi
echo ""

# 9. Check permissions
echo -e "${BLUE}[9] Checking file permissions...${NC}"
echo "App directory owner:"
ls -ld $APP_DIR
echo "App.py permissions:"
ls -l $APP_DIR/app.py 2>/dev/null || echo "app.py not found"
echo ""

# 10. Check installed Python packages
echo -e "${BLUE}[10] Checking installed Python packages...${NC}"
$APP_DIR/venv/bin/pip list 2>/dev/null | grep -E "(Flask|markdown2)" || echo -e "${RED}Flask packages not found${NC}"
echo ""

# 11. Common issues and solutions
echo -e "${BLUE}=========================================="
echo "  Common Issues & Solutions"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}Issue 1: ModuleNotFoundError${NC}"
echo "Solution: Install dependencies"
echo "  cd $APP_DIR"
echo "  sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt"
echo ""

echo -e "${YELLOW}Issue 2: Port already in use${NC}"
echo "Solution: Kill process on port 5001"
echo "  sudo lsof -t -i:5001 | xargs sudo kill -9"
echo ""

echo -e "${YELLOW}Issue 3: Permission denied${NC}"
echo "Solution: Fix permissions"
echo "  sudo chown -R $APP_USER:$APP_USER $APP_DIR"
echo "  sudo chmod +x $APP_DIR/app.py"
echo ""

echo -e "${YELLOW}Issue 4: Missing dependencies${NC}"
echo "Solution: Reinstall everything"
echo "  cd $APP_DIR"
echo "  sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip"
echo "  sudo -u $APP_USER $APP_DIR/venv/bin/pip install Flask Flask-CORS markdown2"
echo ""

echo -e "${BLUE}=========================================="
echo "  Quick Fix Commands"
echo "==========================================${NC}"
echo ""
echo "Try these commands in order:"
echo ""
echo "1. Install dependencies:"
echo "   cd $APP_DIR && sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt"
echo ""
echo "2. Fix permissions:"
echo "   sudo chown -R $APP_USER:$APP_USER $APP_DIR"
echo ""
echo "3. Restart service:"
echo "   sudo systemctl restart $APP_NAME"
echo ""
echo "4. Check status:"
echo "   sudo systemctl status $APP_NAME"
echo ""

echo -e "${GREEN}=========================================="
echo "  Next Steps"
echo "==========================================${NC}"
echo ""
echo "1. Review the logs above for specific errors"
echo "2. Apply the relevant solution"
echo "3. Restart the service: sudo systemctl restart $APP_NAME"
echo "4. Check status: sudo systemctl status $APP_NAME"
echo ""
