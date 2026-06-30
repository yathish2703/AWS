# Scripts Index

This directory contains utility scripts for deploying, managing, and troubleshooting the AWS Learning Platform.

## Scripts Overview

### 🚀 Deployment Scripts

#### `deploy_to_ec2.sh`
**Purpose:** Complete automated deployment script for EC2 instances

**What it does:**
- Updates system packages
- Installs Python, Nginx, and system dependencies
- Creates application user and directories
- Sets up Python virtual environment
- Installs application dependencies
- Creates systemd service for auto-start
- Configures Nginx as reverse proxy
- Opens firewall ports
- Starts and enables all services

**Usage:**
```bash
sudo bash scripts/deploy_to_ec2.sh
```

**Requirements:**
- Root/sudo access
- Amazon Linux, CentOS, Ubuntu, or Debian OS
- EC2 Security Group allowing ports 22, 80

---

### ▶️ Application Start Scripts

#### `start.sh`
**Purpose:** Local development server startup script

**What it does:**
- Creates Python virtual environment if missing
- Activates virtual environment
- Installs/updates dependencies from requirements.txt
- Stops any existing Flask instances
- Starts Flask development server on port 5001

**Usage:**
```bash
bash scripts/start.sh
```

**Note:** For local development only, not for production deployment

---

### ⚙️ Installation Scripts

#### `INSTALL.sh`
**Purpose:** Quick setup guide and installation summary for EC2

**What it does:**
- Displays step-by-step EC2 setup instructions
- Shows prerequisites checklist
- Provides SCP commands for file transfer
- Lists SSH connection commands
- Shows deployment and verification commands

**Usage:**
```bash
bash scripts/INSTALL.sh
```

**Note:** This is an informational script that displays instructions; it doesn't perform installation itself

---

### 🔍 Monitoring & Verification Scripts

#### `check_status.sh`
**Purpose:** Application health check and verification

**What it does:**
- Checks if application service is running
- Verifies Nginx status
- Tests if port 5001 (app) and port 80 (nginx) are listening
- Tests local HTTP connections
- Shows disk space usage
- Displays recent application logs
- Shows public IP address for access

**Usage:**
```bash
bash scripts/check_status.sh
```

**When to use:** After deployment or when verifying system health

---

### 🛠️ Troubleshooting Scripts

#### `troubleshoot.sh`
**Purpose:** Comprehensive diagnostic tool for failed deployments

**What it does:**
- Checks application directory structure
- Verifies application user exists
- Tests Python virtual environment
- Validates application files (app.py, requirements.txt)
- Checks systemd service status
- Displays last 20 lines of service logs
- Tests Python application directly
- Checks for port conflicts
- Verifies file permissions
- Lists installed Python packages
- Provides common issues and solutions

**Usage:**
```bash
sudo bash scripts/troubleshoot.sh
```

**When to use:** When deployment fails or service won't start

---

#### `quick_fix.sh`
**Purpose:** Automated fix for common deployment issues

**What it does:**
- Creates missing directories
- Fixes file permissions
- Ensures Python virtual environment exists
- Upgrades pip
- Installs/reinstalls Flask and dependencies
- Kills processes blocking port 5001
- Tests Flask imports
- Restarts systemd service
- Verifies service is running
- Tests HTTP connection

**Usage:**
```bash
sudo bash scripts/quick_fix.sh
```

**When to use:**
- After initial deployment fails
- When service stops unexpectedly
- After making code changes
- When troubleshoot.sh identifies fixable issues

---

## Typical Workflow

### First Time Deployment on EC2
```bash
# 1. Copy files to EC2
scp -i key.pem -r /path/to/AWS ec2-user@EC2-IP:/tmp/aws-app

# 2. SSH to EC2
ssh -i key.pem ec2-user@EC2-IP

# 3. Deploy
sudo cp -r /tmp/aws-app /opt/aws-learning-platform
cd /opt/aws-learning-platform
sudo bash scripts/deploy_to_ec2.sh

# 4. Verify
bash scripts/check_status.sh
```

### If Deployment Fails
```bash
# Run quick fix
sudo bash scripts/quick_fix.sh

# If still failing, run full diagnostics
sudo bash scripts/troubleshoot.sh
```

### Local Development
```bash
# Start development server
bash scripts/start.sh
```

### Ongoing Monitoring
```bash
# Check application health
bash scripts/check_status.sh

# View live logs
sudo journalctl -u aws-learning-platform -f

# Restart service
sudo systemctl restart aws-learning-platform
```

---

## Configuration Details

### Default Settings
- **Application Name:** aws-learning-platform
- **Installation Path:** /opt/aws-learning-platform
- **Application User:** webapp
- **Python Version:** 3.11
- **Application Port:** 5001 (internal)
- **Public Port:** 80 (via Nginx)
- **Host:** 0.0.0.0 (all interfaces)

### Required Ports
- **Port 22:** SSH access
- **Port 80:** HTTP access (public)
- **Port 5001:** Flask application (internal only)

---

## Troubleshooting Quick Reference

| Issue | Script to Run |
|-------|---------------|
| Initial deployment | `deploy_to_ec2.sh` |
| Service won't start | `quick_fix.sh` |
| Need diagnostics | `troubleshoot.sh` |
| Check if working | `check_status.sh` |
| Local development | `start.sh` |
| View instructions | `INSTALL.sh` |

---

## Important Notes

⚠️ **Security:**
- Never commit real credentials or API keys
- Keep `.env` files out of version control
- Use EC2 IAM roles instead of hardcoded credentials

⚠️ **Permissions:**
- Deployment scripts require `sudo` access
- Application runs as `webapp` user (not root)
- All scripts maintain proper file ownership

⚠️ **Production:**
- Set `FLASK_ENV=production` in systemd service
- Use proper domain name and HTTPS in production
- Configure proper logging and monitoring

---

## Logs Location

- **Systemd logs:** `sudo journalctl -u aws-learning-platform`
- **Application logs:** `/opt/aws-learning-platform/logs/app.log`
- **Error logs:** `/opt/aws-learning-platform/logs/error.log`
- **Nginx access:** `/var/log/nginx/aws-learning-platform_access.log`
- **Nginx errors:** `/var/log/nginx/aws-learning-platform_error.log`
