#!/bin/bash

#############################################
# AWS Learning Platform - EC2 Deployment Script
# This script prepares an EC2 instance for deployment
#############################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="aws-learning-platform"
APP_DIR="/opt/$APP_NAME"
APP_USER="webapp"
PYTHON_VERSION="3.11"
PORT="5001"

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_message "$BLUE" "=========================================="
print_message "$BLUE" "  AWS Learning Platform Deployment"
print_message "$BLUE" "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_message "$RED" "Please run as root (use sudo)"
    exit 1
fi

print_message "$GREEN" "Step 1: Updating system packages..."
yum update -y || apt-get update -y

print_message "$GREEN" "Step 2: Installing system dependencies..."
# Detect OS type
if command -v yum &> /dev/null; then
    # Amazon Linux / CentOS / RHEL
    yum install -y \
        python3 \
        python3-pip \
        python3-devel \
        git \
        wget \
        curl \
        gcc \
        make \
        nginx \
        supervisor \
        || print_message "$YELLOW" "Some packages may already be installed"
elif command -v apt-get &> /dev/null; then
    # Ubuntu / Debian
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        git \
        wget \
        curl \
        gcc \
        make \
        nginx \
        supervisor \
        || print_message "$YELLOW" "Some packages may already be installed"
else
    print_message "$RED" "Unsupported OS. Please use Amazon Linux, CentOS, Ubuntu, or Debian."
    exit 1
fi

print_message "$GREEN" "Step 3: Creating application user..."
if ! id -u $APP_USER > /dev/null 2>&1; then
    useradd -m -s /bin/bash $APP_USER
    print_message "$GREEN" "User $APP_USER created"
else
    print_message "$YELLOW" "User $APP_USER already exists"
fi

print_message "$GREEN" "Step 4: Creating application directory..."
mkdir -p $APP_DIR
chown -R $APP_USER:$APP_USER $APP_DIR

print_message "$GREEN" "Step 5: Installing the application..."
# Copy application files
cd $APP_DIR

# If running from a git repo, clone it
# Otherwise, files should be manually copied to the server
if [ -n "$GIT_REPO" ]; then
    print_message "$BLUE" "Cloning from Git repository: $GIT_REPO"
    sudo -u $APP_USER git clone $GIT_REPO .
else
    print_message "$YELLOW" "No GIT_REPO specified. Please copy your application files to $APP_DIR"
    print_message "$YELLOW" "Then run this script again or continue manually"
fi

print_message "$GREEN" "Step 6: Setting up Python virtual environment..."
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
print_message "$GREEN" "Virtual environment created"

print_message "$GREEN" "Step 7: Installing Python dependencies..."
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
if [ -f "$APP_DIR/requirements.txt" ]; then
    sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt
    print_message "$GREEN" "Python dependencies installed"
else
    print_message "$YELLOW" "No requirements.txt found. Skipping pip install."
fi

print_message "$GREEN" "Step 8: Creating necessary directories..."
sudo -u $APP_USER mkdir -p $APP_DIR/data/lessons
sudo -u $APP_USER mkdir -p $APP_DIR/data/lessons/00-cloud-basics
sudo -u $APP_USER mkdir -p $APP_DIR/data/quizzes
sudo -u $APP_USER mkdir -p $APP_DIR/data/challenges
sudo -u $APP_USER mkdir -p $APP_DIR/data/users
sudo -u $APP_USER mkdir -p $APP_DIR/logs

print_message "$GREEN" "Step 9: Creating systemd service..."
cat > /etc/systemd/system/$APP_NAME.service <<EOF
[Unit]
Description=AWS Learning Platform Flask Application
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/app.py
Restart=always
RestartSec=10
StandardOutput=append:$APP_DIR/logs/app.log
StandardError=append:$APP_DIR/logs/error.log

[Install]
WantedBy=multi-user.target
EOF

print_message "$GREEN" "Systemd service created"

print_message "$GREEN" "Step 10: Configuring Nginx..."
cat > /etc/nginx/conf.d/$APP_NAME.conf <<EOF
server {
    listen 80;
    server_name _;

    access_log /var/log/nginx/${APP_NAME}_access.log;
    error_log /var/log/nginx/${APP_NAME}_error.log;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_buffering off;
    }

    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /favicon.ico {
        alias $APP_DIR/static/favicon.ico;
        access_log off;
        log_not_found off;
    }

    client_max_body_size 10M;
}
EOF

# Test Nginx configuration
nginx -t

print_message "$GREEN" "Step 11: Configuring firewall..."
# Open HTTP port
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --reload
    print_message "$GREEN" "Firewall configured (firewalld)"
elif command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    print_message "$GREEN" "Firewall configured (ufw)"
else
    print_message "$YELLOW" "No firewall detected. Please configure manually."
fi

print_message "$GREEN" "Step 12: Starting services..."
# Reload systemd
systemctl daemon-reload

# Enable and start the application
systemctl enable $APP_NAME.service
systemctl restart $APP_NAME.service

# Enable and start Nginx
systemctl enable nginx
systemctl restart nginx

# Wait a bit for the service to start
sleep 3

print_message "$GREEN" "Step 13: Checking service status..."
if systemctl is-active --quiet $APP_NAME.service; then
    print_message "$GREEN" "✓ Application service is running"
else
    print_message "$RED" "✗ Application service failed to start"
    systemctl status $APP_NAME.service --no-pager
fi

if systemctl is-active --quiet nginx; then
    print_message "$GREEN" "✓ Nginx is running"
else
    print_message "$RED" "✗ Nginx failed to start"
    systemctl status nginx --no-pager
fi

print_message "$GREEN" "=========================================="
print_message "$GREEN" "  Deployment Complete!"
print_message "$GREEN" "=========================================="
print_message "$BLUE" ""
print_message "$BLUE" "Application Details:"
print_message "$BLUE" "  - Service Name: $APP_NAME"
print_message "$BLUE" "  - App Directory: $APP_DIR"
print_message "$BLUE" "  - App User: $APP_USER"
print_message "$BLUE" "  - Internal Port: $PORT"
print_message "$BLUE" "  - Public Port: 80 (HTTP)"
print_message "$BLUE" ""
print_message "$BLUE" "Useful Commands:"
print_message "$BLUE" "  - Check status: sudo systemctl status $APP_NAME"
print_message "$BLUE" "  - View logs: sudo journalctl -u $APP_NAME -f"
print_message "$BLUE" "  - Restart app: sudo systemctl restart $APP_NAME"
print_message "$BLUE" "  - Restart nginx: sudo systemctl restart nginx"
print_message "$BLUE" "  - View app logs: sudo tail -f $APP_DIR/logs/app.log"
print_message "$BLUE" ""
print_message "$GREEN" "Your application should now be accessible at:"
print_message "$GREEN" "  http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'YOUR-EC2-IP')"
print_message "$BLUE" ""
print_message "$YELLOW" "NOTE: Make sure your EC2 Security Group allows inbound traffic on port 80"
print_message "$BLUE" "=========================================="
