# AWS Learning Platform

A comprehensive, interactive platform for learning AWS services with hands-on labs, quizzes, and visual learning tools.

## 📁 Project Structure

```
AWS/
├── aws-platform-new/     # New Flask-based platform (active development)
├── aws-learning-react/   # React-based frontend version
├── documentation/        # All project documentation
├── scripts/             # Deployment and utility scripts
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
├── data/                # Course data and content
├── app.py               # Main Flask application (legacy)
├── config.py            # Application configuration
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### For Local Development
```bash
# Start the development server
bash scripts/start.sh
```

### For EC2 Deployment
```bash
# Deploy to AWS EC2
sudo bash scripts/deploy_to_ec2.sh

# Check deployment status
bash scripts/check_status.sh
```

## 📚 Documentation

All documentation is in the [`documentation/`](documentation/) directory:

- **[README.md](documentation/README.md)** - Project overview and setup
- **[GETTING_STARTED.md](documentation/GETTING_STARTED.md)** - First-time setup guide
- **[QUICKSTART.md](documentation/QUICKSTART.md)** - Quick reference guide
- **[AWS_LEARNING_README.md](documentation/AWS_LEARNING_README.md)** - Learning platform details
- **[EC2_DEPLOYMENT.md](documentation/EC2_DEPLOYMENT.md)** - EC2 deployment guide
- **[DEPLOYMENT_README.md](documentation/DEPLOYMENT_README.md)** - Deployment architecture
- **[SETUP_COMPLETE.md](documentation/SETUP_COMPLETE.md)** - Post-setup checklist
- **[TROUBLESHOOTING.md](documentation/TROUBLESHOOTING.md)** - Common issues and fixes
- **[ANIMATION_GUIDE.md](documentation/ANIMATION_GUIDE.md)** - Animation features guide
- **[TEACHER_MODE_GUIDE.md](documentation/TEACHER_MODE_GUIDE.md)** - Teaching tools guide
- **[NEW_DESIGN_SUMMARY.md](documentation/NEW_DESIGN_SUMMARY.md)** - Design documentation

## 🛠️ Scripts

All utility scripts are in the [`scripts/`](scripts/) directory. See [scripts/README.md](scripts/README.md) for detailed documentation.

**Key scripts:**
- `deploy_to_ec2.sh` - Full EC2 deployment automation
- `start.sh` - Local development server
- `check_status.sh` - Health check and verification
- `troubleshoot.sh` - Diagnostic tool for issues
- `quick_fix.sh` - Automated common fixes
- `INSTALL.sh` - Installation instructions

## 🎯 Features

- **Interactive Learning Modules** - Hands-on AWS service tutorials
- **Visual Diagrams** - Architecture and concept visualizations
- **Quiz System** - Test your knowledge
- **Progress Tracking** - Monitor learning progress
- **Multiple Learning Paths** - EC2, IAM, Security Groups, and more
- **Teacher Mode** - Tools for instructors
- **Animations** - Interactive visual learning aids

## 🏗️ Active Projects

### aws-platform-new/
Current active development version with:
- Simplified architecture
- Modern Flask design
- Focus on core learning features
- See [aws-platform-new/README.md](aws-platform-new/README.md)

### aws-learning-react/
React-based frontend:
- Modern UI with React + Vite
- Redux state management
- Victory charts for visualizations
- See [aws-learning-react/README.md](aws-learning-react/README.md)

## 🔧 Technical Stack

**Backend:**
- Python 3.x
- Flask web framework
- Markdown2 for content rendering

**Frontend:**
- React (in aws-learning-react)
- HTML5/CSS3
- JavaScript
- Bootstrap/Tailwind

**Deployment:**
- Nginx (reverse proxy)
- Systemd (service management)
- AWS EC2 (hosting)

## 📝 Requirements

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- Flask
- Flask-CORS (for API)
- Markdown2 (content rendering)

## 🚀 Running the Application

### Default Port (8080)
```bash
python app.py
```

### Custom Port
```bash
python app.py <port>
```

### Port 80 (requires sudo)
```bash
sudo python app.py 80
```

**Access:** The application runs on `0.0.0.0`, accessible from any network interface.

## 🔍 Monitoring

```bash
# Check application status
bash scripts/check_status.sh

# View logs (EC2)
sudo journalctl -u aws-learning-platform -f

# View application logs
tail -f /opt/aws-learning-platform/logs/app.log
```

## 🐛 Troubleshooting

If you encounter issues:

1. Run the diagnostic tool:
   ```bash
   sudo bash scripts/troubleshoot.sh
   ```

2. Try automatic fixes:
   ```bash
   sudo bash scripts/quick_fix.sh
   ```

3. Check the [TROUBLESHOOTING.md](documentation/TROUBLESHOOTING.md) guide

## 📖 Learning Paths

Current available modules:
- **AWS Fundamentals** - Cloud computing basics
- **EC2 (Elastic Compute Cloud)** - Virtual servers
- **IAM (Identity and Access Management)** - Security and permissions
- **Security Groups** - Firewall configuration
- **How Cloud Works** - Infrastructure overview

## 🤝 Contributing

1. Make changes in appropriate directories
2. Test locally with `bash scripts/start.sh`
3. Deploy to test environment with `scripts/deploy_to_ec2.sh`
4. Update documentation as needed

## 📦 Configuration

- **App Config:** `config.py`
- **Environment Variables:** `.env` (not in repo - see `.env.example`)
- **Port:** Configurable via command line argument
- **Host:** Set to `0.0.0.0` for network access

## 🔐 Security Notes

- Never commit credentials or API keys
- Use environment variables for sensitive data
- See `.env.example` for required variables
- EC2 Security Groups should restrict access appropriately

## 📄 License

[Add your license information here]

## 💡 Support

- Check [documentation/](documentation/) for detailed guides
- Run `scripts/troubleshoot.sh` for diagnostics
- Review logs for error messages
- See [TROUBLESHOOTING.md](documentation/TROUBLESHOOTING.md) for common issues

---

**Last Updated:** June 2026
