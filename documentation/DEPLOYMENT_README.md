# AWS Learning Platform - Modern Design + EC2 Ready

A gamified, interactive AWS learning platform with a clean, modern design.

## 🎨 New Modern Design

The application has been redesigned with a contemporary, professional look featuring:

- **Clean, Minimalist Interface** - Modern card-based layout
- **Smooth Animations** - Fade-in effects and hover interactions
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Modern Color Scheme** - Blue primary colors with accent colors
- **Professional Typography** - Inter font family with proper hierarchy
- **Card-Based Layouts** - Clean, organized content presentation
- **Glassmorphism Effects** - Modern translucent UI elements in the header stats

### Design Features

- 🎯 **Hero Section** - Eye-catching gradient header with progress tracking
- 📚 **Lesson Cards** - Interactive cards with hover effects and badges
- 📊 **Stats Dashboard** - Beautiful stat boxes with icons and animations
- 🔄 **Smooth Transitions** - All interactions are smooth and polished
- 📱 **Mobile-First** - Fully responsive grid system

## 🚀 Quick Start (Local Development)

```bash
# Clone or navigate to the project
cd /path/to/AWS

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at: http://localhost:5001
```

## ☁️ Deploy to AWS EC2

### Quick Deployment (3 Steps)

1. **Launch an EC2 instance** (Amazon Linux 2023 or Ubuntu recommended)
   - Instance Type: t2.micro or higher
   - Security Group: Allow ports 22 (SSH) and 80 (HTTP)

2. **Copy files to EC2:**
   ```bash
   scp -i your-key.pem -r . ec2-user@your-ec2-ip:/tmp/aws-app
   ```

3. **SSH to EC2 and run deployment:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   sudo cp -r /tmp/aws-app /opt/aws-learning-platform
   cd /opt/aws-learning-platform
   sudo bash deploy_to_ec2.sh
   ```

### What Gets Deployed

The deployment script automatically:
- ✅ Installs all system dependencies (Python, Nginx, etc.)
- ✅ Sets up Python virtual environment
- ✅ Installs application dependencies
- ✅ Creates systemd service for auto-start
- ✅ Configures Nginx as reverse proxy
- ✅ Sets up proper permissions and directories
- ✅ Starts all services

### Post-Deployment

Access your application at: `http://your-ec2-public-ip`

Check status:
```bash
./check_status.sh
```

View logs:
```bash
sudo journalctl -u aws-learning-platform -f
```

## 📁 Project Structure

```
AWS/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── deploy_to_ec2.sh           # EC2 deployment script ⭐
├── check_status.sh            # Health check script
├── EC2_DEPLOYMENT.md          # Detailed deployment guide
├── templates/
│   ├── base.html              # Modern base template ⭐
│   ├── index.html             # Modern dashboard ⭐
│   ├── lesson.html
│   ├── quiz.html
│   ├── profile.html
│   ├── leaderboard.html
│   └── teacher_*.html
├── static/
│   ├── css/
│   │   ├── modern.css         # New modern design CSS ⭐
│   │   ├── retro.css          # Optional retro style
│   │   ├── main.css           # Original styles
│   │   └── ...
│   └── js/
│       ├── app.js
│       ├── gamification.js
│       └── ...
└── data/
    ├── lessons/
    ├── quizzes/
    └── users/
```

## 🎨 Design System

### Color Palette

```css
Primary:   #2563eb (Blue)
Secondary: #10b981 (Green)
Accent:    #f59e0b (Amber)
Danger:    #ef4444 (Red)
```

### Typography

- **Font Family**: Inter (Professional, modern sans-serif)
- **Headings**: Bold (700), 1.2 line-height
- **Body**: Regular (400), 1.6 line-height

### Components

- Cards with hover effects
- Gradient hero sections
- Progress bars with animations
- Stat boxes with icons
- Modern buttons with transitions
- Badges and tags
- Alert boxes

## 🛠️ Management Commands

### Application Management

```bash
# Start application
sudo systemctl start aws-learning-platform

# Stop application
sudo systemctl stop aws-learning-platform

# Restart application
sudo systemctl restart aws-learning-platform

# Check status
sudo systemctl status aws-learning-platform

# View logs
sudo journalctl -u aws-learning-platform -f
sudo tail -f /opt/aws-learning-platform/logs/app.log
```

### Nginx Management

```bash
# Restart Nginx
sudo systemctl restart nginx

# Check Nginx status
sudo systemctl status nginx

# Test Nginx config
sudo nginx -t

# View Nginx logs
sudo tail -f /var/log/nginx/aws-learning-platform_access.log
```

## 🔧 Configuration

### Change Port

Edit `config.py`:
```python
PORT = 5001  # Change to your desired port
```

### Production Settings

Edit `config.py`:
```python
DEBUG = False
SECRET_KEY = 'your-secure-random-key-here'
```

## 📚 Documentation

- **[EC2_DEPLOYMENT.md](EC2_DEPLOYMENT.md)** - Complete EC2 deployment guide
- Includes troubleshooting, SSL setup, monitoring, and more

## 🔒 Security Considerations

### For Production:

1. **Change SECRET_KEY** in `config.py`
2. **Set DEBUG = False** in production
3. **Configure HTTPS/SSL** using Let's Encrypt
4. **Restrict Security Group** to specific IPs when possible
5. **Regular Updates** - Keep system packages updated
6. **Backup Data** regularly

## 📊 Features

- ✅ Gamified learning with points, levels, badges
- ✅ Interactive lessons and quizzes
- ✅ Progress tracking
- ✅ User profiles
- ✅ Leaderboard
- ✅ Teacher mode for creating content
- ✅ Modern, responsive design
- ✅ Cloud-ready with easy EC2 deployment

## 🆘 Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u aws-learning-platform -n 50

# Test Python directly
sudo -u webapp /opt/aws-learning-platform/venv/bin/python /opt/aws-learning-platform/app.py
```

### Can't access from browser

1. Check Security Group allows port 80
2. Check firewall: `sudo firewall-cmd --list-all` or `sudo ufw status`
3. Test locally: `curl http://localhost`
4. Check Nginx: `sudo nginx -t`

### Run health check

```bash
./check_status.sh
```

## 📝 License

Educational project - Free to use and modify

## 🤝 Contributing

Feel free to improve the design, add features, or fix bugs!

## 📞 Support

For issues:
1. Check application logs: `/opt/aws-learning-platform/logs/`
2. Check system logs: `sudo journalctl -u aws-learning-platform`
3. Review the EC2_DEPLOYMENT.md guide

---

**Built with:** Python Flask, Modern CSS, Vanilla JavaScript

**Deployed on:** AWS EC2 with Nginx
