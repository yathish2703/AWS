# AWS Learning Platform

A Flask-based web application for AWS learning and training.

## Requirements

- Python 3.x
- Flask

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Default Port (8080)
```bash
python app.py
```
Access at: `http://localhost:8080`

### Custom Port
```bash
python app.py <port_number>
```
Example: `python app.py 3000`

### Port 80 (Standard HTTP)
```bash
sudo python app.py 80
```
Access at: `http://localhost`

**Note:** Port 80 requires administrator privileges (sudo).

## Network Access

The application runs on `0.0.0.0`, making it accessible from:
- Local machine: `http://localhost:<port>`
- Network devices: `http://<your-ip-address>:<port>`

## Features

- Interactive AWS learning modules
- Course management dashboard
- Learning paths for EC2, IAM, and Security Groups
- Progress tracking
- Quiz functionality

## Development

The application runs in debug mode by default, enabling:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger
