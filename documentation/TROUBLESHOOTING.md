# 🔧 Troubleshooting Guide - Application Failed to Start

## Quick Fix (Try This First!)

If the application service failed to start, run this command on your EC2 instance:

```bash
sudo bash quick_fix.sh
```

This script will:
- ✅ Create missing directories
- ✅ Fix file permissions
- ✅ Install/reinstall Python packages
- ✅ Clear port conflicts
- ✅ Restart the service
- ✅ Show you what went wrong

## Detailed Diagnostics

If quick_fix.sh doesn't resolve the issue, run the troubleshooter:

```bash
sudo bash troubleshoot.sh
```

This will check:
- Directory structure
- User permissions
- Python environment
- Application files
- Service configuration
- Port availability
- Recent error logs

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError (Flask, markdown2, etc.)

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'markdown2'
```

**Solution:**
```bash
cd /opt/aws-learning-platform
sudo -u webapp /opt/aws-learning-platform/venv/bin/pip install -r requirements.txt
# OR manually:
sudo -u webapp /opt/aws-learning-platform/venv/bin/pip install Flask Flask-CORS markdown2
sudo systemctl restart aws-learning-platform
```

### Issue 2: Port Already in Use

**Symptom:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find what's using port 5001
sudo lsof -i :5001

# Kill the process
sudo lsof -t -i:5001 | xargs sudo kill -9

# Restart service
sudo systemctl restart aws-learning-platform
```

### Issue 3: Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Fix all permissions
sudo chown -R webapp:webapp /opt/aws-learning-platform
sudo chmod -R 755 /opt/aws-learning-platform
sudo chmod +x /opt/aws-learning-platform/app.py

# Restart service
sudo systemctl restart aws-learning-platform
```

### Issue 4: Missing Directories

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/opt/aws-learning-platform/data'
```

**Solution:**
```bash
cd /opt/aws-learning-platform
sudo -u webapp mkdir -p data/lessons/00-cloud-basics
sudo -u webapp mkdir -p data/quizzes
sudo -u webapp mkdir -p data/challenges
sudo -u webapp mkdir -p data/users
sudo -u webapp mkdir -p logs

sudo systemctl restart aws-learning-platform
```

### Issue 5: Python/Virtual Environment Issues

**Symptom:**
```
/opt/aws-learning-platform/venv/bin/python: No such file or directory
```

**Solution:**
```bash
# Recreate virtual environment
cd /opt/aws-learning-platform
sudo rm -rf venv
sudo -u webapp python3 -m venv venv
sudo -u webapp venv/bin/pip install --upgrade pip
sudo -u webapp venv/bin/pip install -r requirements.txt

sudo systemctl restart aws-learning-platform
```

### Issue 6: Systemd Service Not Found

**Symptom:**
```
Failed to restart aws-learning-platform.service: Unit not found
```

**Solution:**
```bash
# Recreate the service file
sudo bash deploy_to_ec2.sh

# OR manually create it:
sudo nano /etc/systemd/system/aws-learning-platform.service
# (paste the service configuration from deploy_to_ec2.sh)

sudo systemctl daemon-reload
sudo systemctl enable aws-learning-platform
sudo systemctl start aws-learning-platform
```

### Issue 7: Import Error - Config Module

**Symptom:**
```
ModuleNotFoundError: No module named 'config'
```

**Solution:**
```bash
# Ensure config.py exists
ls -la /opt/aws-learning-platform/config.py

# Check file permissions
sudo chmod 644 /opt/aws-learning-platform/config.py
sudo chown webapp:webapp /opt/aws-learning-platform/config.py

# Test import
cd /opt/aws-learning-platform
sudo -u webapp venv/bin/python -c "import config; print('Config OK')"

sudo systemctl restart aws-learning-platform
```

## Manual Testing

### Test 1: Check if Python works

```bash
cd /opt/aws-learning-platform
sudo -u webapp venv/bin/python --version
```

Expected: `Python 3.x.x`

### Test 2: Test Flask import

```bash
cd /opt/aws-learning-platform
sudo -u webapp venv/bin/python -c "from flask import Flask; print('Flask OK')"
```

Expected: `Flask OK`

### Test 3: Run app.py directly

```bash
cd /opt/aws-learning-platform
sudo -u webapp venv/bin/python app.py
```

Expected: Server should start. Press Ctrl+C to stop. Look for errors.

### Test 4: Check service logs

```bash
# Last 50 lines
sudo journalctl -u aws-learning-platform -n 50

# Follow logs in real-time
sudo journalctl -u aws-learning-platform -f

# Today's logs
sudo journalctl -u aws-learning-platform --since today
```

## Step-by-Step Recovery

If nothing else works, follow these steps:

### Step 1: Stop Everything

```bash
sudo systemctl stop aws-learning-platform
sudo systemctl stop nginx
```

### Step 2: Verify Files

```bash
cd /opt/aws-learning-platform
ls -la

# Should see:
# app.py
# config.py
# requirements.txt
# templates/
# static/
# data/
# venv/
```

If files are missing, copy them again from your local machine.

### Step 3: Recreate Environment

```bash
cd /opt/aws-learning-platform

# Remove old venv
sudo rm -rf venv

# Create new venv
sudo -u webapp python3 -m venv venv

# Install packages
sudo -u webapp venv/bin/pip install --upgrade pip
sudo -u webapp venv/bin/pip install Flask==3.0.2 Flask-CORS==4.0.0 Werkzeug==3.0.1 markdown2==2.5.5
```

### Step 4: Fix Permissions

```bash
sudo chown -R webapp:webapp /opt/aws-learning-platform
sudo chmod -R 755 /opt/aws-learning-platform
```

### Step 5: Test Manually

```bash
cd /opt/aws-learning-platform
sudo -u webapp venv/bin/python app.py
```

If this works (you see Flask starting), press Ctrl+C and continue.

### Step 6: Restart Services

```bash
sudo systemctl daemon-reload
sudo systemctl restart aws-learning-platform
sudo systemctl restart nginx
```

### Step 7: Verify

```bash
sudo systemctl status aws-learning-platform
curl http://localhost:5001
```

## Viewing Logs

### Application Logs

```bash
# Systemd logs
sudo journalctl -u aws-learning-platform -f

# Application log file (if created)
sudo tail -f /opt/aws-learning-platform/logs/app.log
sudo tail -f /opt/aws-learning-platform/logs/error.log
```

### Nginx Logs

```bash
sudo tail -f /var/log/nginx/aws-learning-platform_access.log
sudo tail -f /var/log/nginx/aws-learning-platform_error.log
```

## Security Group Check

Don't forget to check your AWS Security Group:

1. Go to EC2 Dashboard → Security Groups
2. Find your instance's security group
3. Ensure Inbound Rules allow:
   - Port 22 (SSH) from your IP
   - Port 80 (HTTP) from 0.0.0.0/0

## Still Not Working?

### Get Full Diagnostics

```bash
# Run full diagnostic
sudo bash troubleshoot.sh > diagnostic_output.txt 2>&1

# View the file
cat diagnostic_output.txt
```

### Check System Resources

```bash
# Check disk space
df -h

# Check memory
free -h

# Check if system is overloaded
top
```

### Nuclear Option: Complete Reinstall

```bash
# Stop and remove everything
sudo systemctl stop aws-learning-platform
sudo systemctl disable aws-learning-platform
sudo rm -rf /opt/aws-learning-platform
sudo rm /etc/systemd/system/aws-learning-platform.service
sudo systemctl daemon-reload

# Copy files again from local machine
# Then run deployment script again
sudo bash deploy_to_ec2.sh
```

## Contact/Support

If you've tried everything:

1. Collect logs: `sudo journalctl -u aws-learning-platform -n 100 > error_logs.txt`
2. Note your EC2 instance type and OS
3. Document what steps you've tried

## Prevention

To avoid issues in the future:

1. ✅ Always test locally first: `python app.py`
2. ✅ Keep requirements.txt updated
3. ✅ Use the same Python version (3.11+)
4. ✅ Don't modify files while the service is running
5. ✅ Always restart after changes: `sudo systemctl restart aws-learning-platform`

---

**Remember:** The quick_fix.sh and troubleshoot.sh scripts solve 90% of deployment issues!
