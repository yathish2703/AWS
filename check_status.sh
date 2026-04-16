#!/bin/bash

#############################################
# Quick Verification Script
# Run this to check if everything is working
#############################################

APP_NAME="aws-learning-platform"
APP_DIR="/opt/$APP_NAME"

echo "=========================================="
echo "  Application Health Check"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

# Check application service
echo "Checking application service..."
if $SUDO systemctl is-active --quiet $APP_NAME; then
    echo "✓ Application service is running"
    $SUDO systemctl status $APP_NAME --no-pager | grep "Active:"
else
    echo "✗ Application service is NOT running"
    echo "  Try: sudo systemctl start $APP_NAME"
fi
echo ""

# Check Nginx
echo "Checking Nginx..."
if $SUDO systemctl is-active --quiet nginx; then
    echo "✓ Nginx is running"
else
    echo "✗ Nginx is NOT running"
    echo "  Try: sudo systemctl start nginx"
fi
echo ""

# Check if port 5001 is listening
echo "Checking application port..."
if $SUDO lsof -i :5001 > /dev/null 2>&1 || $SUDO netstat -tuln | grep -q ":5001 "; then
    echo "✓ Application is listening on port 5001"
else
    echo "✗ Nothing is listening on port 5001"
fi
echo ""

# Check if port 80 is listening
echo "Checking Nginx port..."
if $SUDO lsof -i :80 > /dev/null 2>&1 || $SUDO netstat -tuln | grep -q ":80 "; then
    echo "✓ Nginx is listening on port 80"
else
    echo "✗ Nothing is listening on port 80"
fi
echo ""

# Test local connection
echo "Testing local connection..."
if curl -s http://localhost:5001 > /dev/null; then
    echo "✓ Application responds on port 5001"
else
    echo "✗ Application not responding on port 5001"
fi

if curl -s http://localhost:80 > /dev/null; then
    echo "✓ Nginx responds on port 80"
else
    echo "✗ Nginx not responding on port 80"
fi
echo ""

# Check disk space
echo "Checking disk space..."
df -h $APP_DIR | tail -1 | awk '{print "  Disk usage: " $5 " used on " $6}'
echo ""

# Check recent logs
echo "Recent application logs (last 5 lines):"
if [ -f "$APP_DIR/logs/app.log" ]; then
    tail -5 $APP_DIR/logs/app.log
else
    $SUDO journalctl -u $APP_NAME -n 5 --no-pager
fi
echo ""

# Get public IP
echo "=========================================="
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
if [ -n "$PUBLIC_IP" ]; then
    echo "Your application URL:"
    echo "  http://$PUBLIC_IP"
else
    echo "Could not determine public IP"
    echo "Run: curl http://169.254.169.254/latest/meta-data/public-ipv4"
fi
echo "=========================================="
