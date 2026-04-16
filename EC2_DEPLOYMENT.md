# AWS Learning Platform - EC2 Deployment Guide

## Quick Start

This guide will help you deploy the AWS Learning Platform on an Amazon EC2 instance.

## Prerequisites

1. **EC2 Instance Requirements:**
   - Instance Type: t2.micro or higher (t2.small recommended)
   - OS: Amazon Linux 2023, Amazon Linux 2, Ubuntu 20.04/22.04, or CentOS 7/8
   - Storage: 8 GB minimum (20 GB recommended)
   - Security Group: Allow inbound traffic on port 80 (HTTP) and 22 (SSH)

2. **Local Requirements:**
   - SSH key pair for EC2 access
   - Git installed (optional)

## Deployment Methods

### Method 1: Direct SSH Deployment (Recommended)

1. **Connect to your EC2 instance:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```

2. **Copy the application files to EC2:**
   ```bash
   # On your local machine
   scp -i your-key.pem -r /path/to/AWS ec2-user@your-ec2-ip:/tmp/
   ```

3. **On the EC2 instance, move files and run deployment:**
   ```bash
   sudo mkdir -p /opt/aws-learning-platform
   sudo cp -r /tmp/AWS/* /opt/aws-learning-platform/
   cd /opt/aws-learning-platform
   sudo bash deploy_to_ec2.sh
   ```

### Method 2: Git Clone Deployment

1. **Connect to your EC2 instance:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```

2. **Clone and deploy:**
   ```bash
   # If your code is in a Git repository
   sudo su
   cd /opt
   export GIT_REPO="https://github.com/yourusername/your-repo.git"

   # Download the deployment script
   curl -O https://raw.githubusercontent.com/yourusername/your-repo/main/deploy_to_ec2.sh
   chmod +x deploy_to_ec2.sh
   ./deploy_to_ec2.sh
   ```

## What the Deployment Script Does

The `deploy_to_ec2.sh` script automatically:

1. ✅ Updates system packages
2. ✅ Installs Python 3, pip, Nginx, and other dependencies
3. ✅ Creates a dedicated application user (`webapp`)
4. ✅ Sets up Python virtual environment
5. ✅ Installs Python packages from requirements.txt
6. ✅ Creates necessary data directories
7. ✅ Configures systemd service for auto-start
8. ✅ Configures Nginx as reverse proxy
9. ✅ Configures firewall rules
10. ✅ Starts all services

## Post-Deployment

### Access Your Application

Your application will be available at:
```
http://your-ec2-public-ip
```

To find your EC2 public IP:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### Useful Management Commands

```bash
# Check application status
sudo systemctl status aws-learning-platform

# View application logs
sudo journalctl -u aws-learning-platform -f
sudo tail -f /opt/aws-learning-platform/logs/app.log

# Restart application
sudo systemctl restart aws-learning-platform

# Check Nginx status
sudo systemctl status nginx

# Restart Nginx
sudo systemctl restart nginx

# View Nginx logs
sudo tail -f /var/log/nginx/aws-learning-platform_access.log
sudo tail -f /var/log/nginx/aws-learning-platform_error.log
```

## Configuration

### Change Application Port

Edit `/opt/aws-learning-platform/config.py`:
```python
PORT = 5001  # Change this value
```

Then restart:
```bash
sudo systemctl restart aws-learning-platform
```

### Environment Variables

Create a `.env` file in `/opt/aws-learning-platform/`:
```bash
SECRET_KEY=your-secure-secret-key
DEBUG=False
PORT=5001
```

### Update Application

```bash
cd /opt/aws-learning-platform
sudo -u webapp git pull  # If using Git
sudo systemctl restart aws-learning-platform
```

## Security Group Configuration

In AWS Console, ensure your EC2 Security Group allows:

| Type | Protocol | Port Range | Source |
|------|----------|------------|--------|
| SSH  | TCP      | 22         | Your IP |
| HTTP | TCP      | 80         | 0.0.0.0/0 |
| HTTPS| TCP      | 443        | 0.0.0.0/0 |

## Optional: SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

1. **Install Certbot:**
   ```bash
   # Amazon Linux 2
   sudo yum install -y certbot python3-certbot-nginx

   # Ubuntu
   sudo apt install -y certbot python3-certbot-nginx
   ```

2. **Get SSL Certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal:**
   ```bash
   sudo certbot renew --dry-run
   ```

## Troubleshooting

### Application won't start

1. Check logs:
   ```bash
   sudo journalctl -u aws-learning-platform -n 50
   ```

2. Check Python errors:
   ```bash
   sudo -u webapp /opt/aws-learning-platform/venv/bin/python /opt/aws-learning-platform/app.py
   ```

### Can't access from browser

1. Check if service is running:
   ```bash
   sudo systemctl status aws-learning-platform
   sudo systemctl status nginx
   ```

2. Test locally:
   ```bash
   curl http://localhost:5001
   curl http://localhost:80
   ```

3. Check Security Group in AWS Console

4. Check firewall:
   ```bash
   sudo firewall-cmd --list-all  # CentOS/RHEL
   sudo ufw status              # Ubuntu
   ```

### Port already in use

```bash
# Find what's using port 5001
sudo lsof -i :5001
sudo netstat -tulpn | grep 5001

# Kill the process if needed
sudo kill -9 <PID>
```

## Monitoring

### Set up monitoring

```bash
# Install htop for system monitoring
sudo yum install -y htop  # Amazon Linux
sudo apt install -y htop  # Ubuntu

# Monitor system resources
htop
```

### CloudWatch Logs (Optional)

Install CloudWatch agent for AWS-native monitoring:
```bash
# Follow AWS documentation for CloudWatch agent installation
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html
```

## Backup

### Backup data directory

```bash
# Create backup
sudo tar -czf /tmp/aws-learning-backup-$(date +%Y%m%d).tar.gz /opt/aws-learning-platform/data

# Download backup
scp -i your-key.pem ec2-user@your-ec2-ip:/tmp/aws-learning-backup-*.tar.gz ./
```

### Restore from backup

```bash
sudo tar -xzf aws-learning-backup-20260416.tar.gz -C /
sudo chown -R webapp:webapp /opt/aws-learning-platform/data
sudo systemctl restart aws-learning-platform
```

## Performance Tuning

### For production use:

1. **Increase EC2 instance size** (t2.small → t2.medium)
2. **Enable auto-scaling** with Application Load Balancer
3. **Use RDS** instead of file-based storage
4. **Enable CloudFront** CDN for static files
5. **Use Gunicorn** with multiple workers:

```bash
# Install Gunicorn
sudo -u webapp /opt/aws-learning-platform/venv/bin/pip install gunicorn

# Update systemd service
sudo nano /etc/systemd/system/aws-learning-platform.service

# Change ExecStart to:
ExecStart=/opt/aws-learning-platform/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app

# Restart
sudo systemctl daemon-reload
sudo systemctl restart aws-learning-platform
```

## Support

For issues or questions:
- Check application logs: `/opt/aws-learning-platform/logs/`
- Check system logs: `sudo journalctl -u aws-learning-platform`
- Review Nginx logs: `/var/log/nginx/`

## Clean Uninstall

```bash
# Stop services
sudo systemctl stop aws-learning-platform
sudo systemctl stop nginx

# Disable services
sudo systemctl disable aws-learning-platform
sudo systemctl disable nginx

# Remove files
sudo rm -rf /opt/aws-learning-platform
sudo rm /etc/systemd/system/aws-learning-platform.service
sudo rm /etc/nginx/conf.d/aws-learning-platform.conf

# Remove user
sudo userdel -r webapp

# Reload systemd
sudo systemctl daemon-reload
```
