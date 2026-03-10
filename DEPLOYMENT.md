# Farm App Deployment Guide

This guide covers multiple deployment options for the Farm Fresh Vegetables e-commerce application.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Vercel Deployment](#vercel-deployment)
5. [Traditional VPS Deployment](#traditional-vps-deployment)

## Local Development

### Prerequisites
- Python 3.9+
- pip
- Git

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd farm_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from app import create_tables_and_seed; create_tables_and_seed()"

# Run the application
python app.py
```

The app will be available at `http://localhost:8080`

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Quick Start
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Docker Commands
```bash
# Build image
docker build -t farm-app .

# Run container
docker run -p 5000:5000 farm-app

# With environment variables
docker run -p 5000:5000 \
  -e SECRET_KEY=your_secret_key \
  -e DATABASE_URL=sqlite:///database.db \
  farm-app
```

### Production Docker Setup
1. Update `docker-compose.yml` with your production database credentials
2. Set proper environment variables
3. Configure SSL certificates
4. Set up reverse proxy (nginx is included)

## Heroku Deployment

### Prerequisites
- Heroku CLI
- Git

### Setup
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_secure_secret_key

# Deploy
git push heroku main

# Initialize database
heroku run python -c "from app import create_tables_and_seed; create_tables_and_seed()"
```

### Environment Variables (Heroku)
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_secure_secret_key
# DATABASE_URL is automatically set by Heroku PostgreSQL addon
```

## Vercel Deployment

### Prerequisites
- Vercel CLI
- Vercel account

### Setup
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts to configure deployment
```

### vercel.json Configuration
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

## Traditional VPS Deployment

### Prerequisites
- Ubuntu/CentOS server
- Python 3.9+
- Nginx
- PostgreSQL (optional)

### Setup Steps

1. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Create application user
sudo useradd -m -s /bin/bash farmapp
sudo usermod -aG sudo farmapp
```

2. **Application Deployment**
```bash
# Switch to app user
sudo su - farmapp

# Clone repository
git clone <repository-url> ~/farm_app
cd ~/farm_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with production values
```

3. **Database Setup (PostgreSQL)**
```bash
# Switch to postgres user
sudo su - postgres

# Create database and user
createuser farmapp_user
createdb farm_app_db -O farmapp_user
psql -c "ALTER USER farmapp_user PASSWORD 'your_password';"

# Exit back to farmapp user
exit
exit
sudo su - farmapp
cd ~/farm_app
source venv/bin/activate

# Update .env with PostgreSQL URL
# DATABASE_URL=postgresql://farmapp_user:your_password@localhost/farm_app_db
```

4. **Initialize Database**
```bash
python -c "from app import create_tables_and_seed; create_tables_and_seed()"
```

5. **Systemd Service**
```bash
# Create service file
sudo nano /etc/systemd/system/farmapp.service
```

```ini
[Unit]
Description=Farm App
After=network.target

[Service]
User=farmapp
Group=farmapp
WorkingDirectory=/home/farmapp/farm_app
Environment="PATH=/home/farmapp/farm_app/venv/bin"
ExecStart=/home/farmapp/farm_app/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable farmapp
sudo systemctl start farmapp
sudo systemctl status farmapp
```

6. **Nginx Configuration**
```bash
sudo nano /etc/nginx/sites-available/farmapp
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/farmapp/farm_app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/farmapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **SSL Certificate (Let's Encrypt)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Environment Variables

### Required Variables
- `SECRET_KEY`: Flask secret key (generate a strong random string)
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Set to `production` for production

### Optional Variables
- `UPLOAD_FOLDER`: File upload directory (default: static/uploads)
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

## Security Considerations

1. **Database Security**
   - Use strong database passwords
   - Restrict database access to localhost
   - Use SSL for database connections in production

2. **Application Security**
   - Generate a strong `SECRET_KEY`
   - Use HTTPS in production
   - Set up proper CORS policies
   - Validate all user inputs

3. **Server Security**
   - Keep system updated
   - Use firewall (ufw)
   - Disable unused services
   - Regular security audits

## Monitoring and Logging

### Application Logs
```bash
# Docker logs
docker-compose logs -f web

# Systemd logs
sudo journalctl -u farmapp -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks
The application includes a health check endpoint. Monitor:
- Application responsiveness
- Database connectivity
- Disk space usage
- Memory usage

## Backup Strategy

### Database Backup
```bash
# PostgreSQL
pg_dump -h localhost -U farmapp_user farm_app_db > backup.sql

# SQLite
cp database.db backup/database_$(date +%Y%m%d_%H%M%S).db
```

### File Backup
```bash
# Backup static files and uploads
tar -czf backup/static_files_$(date +%Y%m%d_%H%M%S).tar.gz static/
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check network connectivity

2. **Permission Errors**
   - Ensure proper file permissions
   - Check user/group ownership
   - Verify upload directory exists

3. **Static Files Not Loading**
   - Check Nginx configuration
   - Verify file paths
   - Clear browser cache

4. **Application Not Starting**
   - Check logs for errors
   - Verify dependencies are installed
   - Check environment variables

### Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Use connection pooling
   - Optimize queries

2. **Caching**
   - Implement Redis caching
   - Cache static assets
   - Use browser caching

3. **Load Balancing**
   - Multiple application instances
   - Load balancer configuration
   - Health checks

## Scaling Considerations

1. **Horizontal Scaling**
   - Multiple app servers
   - Load balancer
   - Shared database

2. **Database Scaling**
   - Read replicas
   - Database sharding
   - Connection pooling

3. **CDN Integration**
   - Static asset CDN
   - Image optimization
   - Geographic distribution

## Support

For deployment issues:
1. Check application logs
2. Verify environment configuration
3. Test database connectivity
4. Review security settings

## Admin Access

Default admin credentials:
- Username: `admin`
- Password: `admin123`

**Important**: Change these credentials in production by modifying the admin authentication in `app.py`.
