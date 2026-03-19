# 🚀 NetworkInsight Deployment Guide

## 1. ENV CONFIGURATION CHANGES: Development vs Production

### 🔴 CRITICAL CHANGES REQUIRED
These values **MUST** be changed for production:

| Variable | Development | Production | Why |
|----------|-------------|------------|-----|
| `FLASK_ENV` | `development` | `production` | Disables debug mode, security hardening |
| `DEBUG` | `True` | `False` | **CRITICAL**: Prevents source code exposure |
| `SECRET_KEY` | Any string | Generate: `openssl rand -hex 32` | Session security, CSRF protection |
| `DATABASE_URL` | `sqlite:///` (local) | PostgreSQL RDS/Managed service | Scalable, persistent, external DB |
| `REDIS_URL` | `localhost:6379` | External Redis (ElastiCache, Azure Cache) | Distributed caching, session management |
| `CORS_ORIGINS` | `http://localhost:3000` | Your actual domain(s) | Prevents cross-site attacks |
| `VITE_API_BASE_URL` | `http://localhost:5000` | `https://api.yourdomain.com` | Points frontend to production API |

### ⚠️ IMPORTANT CHANGES

| Variable | Development | Production | Notes |
|----------|-------------|------------|-------|
| `WORKERS` | 1-2 | 4+ (depends on CPU) | Gunicorn workers: use `2 × CPU_cores + 1` |
| `THREAD_POOL` | 8-16 | 32+ | Thread pool size for concurrent requests |
| `MAX_CONTENT_LENGTH` | 10MB | 100MB+ | Adjust based on max network file size |
| `UPLOAD_FOLDER` | `/tmp/uploads` | Persistent cloud storage (S3, Azure Blob) | Temp storage will be cleared on restart |
| `LOG_LEVEL` | `DEBUG` | `INFO` or `WARNING` | Reduces log noise, improves performance |
| `NODE_ENV` | `development` | `production` | Enables React production optimizations |

### 🔐 SECURITY-RELATED CHANGES

```env
# OPTIONAL (for HTTPS enforcement)
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true
SECURE_HSTS_PRELOAD=true

# OPTIONAL (for error tracking)
SENTRY_DSN=https://your-sentry-key@sentry.io/project-id

# Mail notifications (if needed)
MAIL_SERVER=smtp.gmail.com
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
```

---

## 2. QUICK ENV CONFIGURATION CHECKLIST

### Before Production Deployment

```bash
# 1. Generate secure SECRET_KEY
openssl rand -hex 32
# Output: abc123def456... (copy this)

# 2. Generate secure database password
openssl rand -base64 32
# Output: xyz789... (copy this)

# 3. Create .env.production with:
DATABASE_URL=postgresql://user:PASSWORD@host:5432/networkinsight
REDIS_URL=redis://:PASSWORD@host:6379/0
SECRET_KEY=abc123def456...
CORS_ORIGINS=["https://yourdomain.com"]
DEBUG=False
FLASK_ENV=production
```

---

## 3. DEPLOYMENT OPTIONS & STRATEGIES

### **Option A: Docker + Container Orchestration (RECOMMENDED for scalability)**

#### Platform: AWS ECS / Azure Container Instances / GCP Cloud Run
```bash
# 1. Build and push Docker image
docker build -t networkinsight-backend:v1.0 ./prototype-backend
docker tag networkinsight-backend:v1.0 AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/networkinsight-backend:v1.0
docker push AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/networkinsight-backend:v1.0

# 2. Deploy using docker-compose or orchestration platform
docker-compose -f docker-compose.production.yml up -d
```

**Best for**: Medium to large scale, auto-scaling needs, microservices

---

### **Option B: Platform-as-a-Service (Easiest for beginners)**

#### Heroku / Railway / Render.com
```bash
# 1. Install CLI
npm install -g heroku

# 2. Create app
heroku create networkinsight-app

# 3. Set production env variables
heroku config:set FLASK_ENV=production DEBUG=False SECRET_KEY=your_key

# 4. Deploy
git push heroku main
```

**Best for**: Quick deployment, minimal DevOps, auto-scaling included

---

### **Option C: Traditional VPS/Dedicated Server**

#### AWS EC2 / DigitalOcean / Linode
```bash
# 1. SSH into server
ssh ubuntu@your-server-ip

# 2. Install dependencies
sudo apt update && sudo apt install python3-pip postgresql redis-server nginx

# 3. Clone repo and setup
git clone https://github.com/yourusername/biological-networks.git
cd biological-networks/prototype-backend
pip install -r requirements.txt

# 4. Configure Gunicorn + Nginx (reverse proxy)
# 5. Enable SSL with Let's Encrypt
sudo certbot certonly --nginx -d yourdomain.com

# 6. Start services
systemctl start gunicorn
systemctl start nginx
```

**Best for**: Full control, custom setup, lower costs

---

### **Option D: Kubernetes (Enterprise-grade)**

#### AWS EKS / Azure AKS / Google GKE
```bash
# 1. Build Docker image
docker build -t networkinsight:v1.0 .

# 2. Push to registry
docker push your-registry/networkinsight:v1.0

# 3. Deploy with Helm or kubectl
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# 4. Scale
kubectl scale deployment networkinsight-backend --replicas=3
```

**Best for**: Large enterprise deployments, high availability, auto-healing

---

## 4. RECOMMENDED DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────┐
│              User's Browser                     │
└────────────────┬────────────────────────────────┘
                 │ HTTPS
                 ▼
┌─────────────────────────────────────────────────┐
│   CDN / CloudFront (Static Assets)              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Load Balancer (AWS ALB / Azure LB)             │
│  - Terminates SSL/TLS                           │
│  - Routes traffic to backend                    │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Backend  │ │ Backend  │ │ Backend  │
│ Instance │ │ Instance │ │ Instance │ (Auto-scaling)
└────┬─────┘ └────┬─────┘ └────┬─────┘
     └────────┬───┴────────┬────┘
              │
     ┌────────┴────────┬──────────────┐
     ▼                 ▼              ▼
  ┌──────┐        ┌──────────┐  ┌─────────┐
  │      │        │          │  │         │
  │  DB  │        │  Redis   │  │   S3    │
  │ (RDS)│        │(ElastiC.)│  │ Storage │
  │      │        │          │  │         │
  └──────┘        └──────────┘  └─────────┘
```

---

## 5. STEP-BY-STEP DEPLOYMENT EXAMPLE: AWS

### Backend Deployment (EC2 + RDS + ElastiCache)

**Prerequisites**: AWS account, EC2 instance, RDS PostgreSQL, ElastiCache Redis

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install dependencies
sudo apt install -y python3.11 python3-pip git nginx supervisor

# 4. Clone repository
git clone https://github.com/yourusername/biological-networks.git
cd biological-networks/prototype-backend

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install Python dependencies
pip install -r requirements.txt

# 7. Create production .env file
cat > .env.production << EOF
FLASK_ENV=production
DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://user:PASSWORD@your-rds-endpoint:5432/networkinsight
REDIS_URL=redis://:PASSWORD@your-elasticache-endpoint:6379/0
WORKERS=4
THREAD_POOL=32
CORS_ORIGINS=["https://yourdomain.com"]
EOF

# 8. Configure Gunicorn + Supervisor
sudo tee /etc/supervisor/conf.d/gunicorn.conf << EOF
[program:gunicorn]
directory=/home/ubuntu/biological-networks/prototype-backend
command=/home/ubuntu/biological-networks/prototype-backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 wsgi:app
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/err.log
stdout_logfile=/var/log/gunicorn/out.log
EOF

# 9. Configure Nginx (reverse proxy)
sudo tee /etc/nginx/sites-available/networkinsight << EOF
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/networkinsight /etc/nginx/sites-enabled/

# 10. Enable SSL (Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# 11. Start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gunicorn
sudo systemctl start nginx
```

### Frontend Deployment (S3 + CloudFront)

```bash
# 1. Build frontend for production
cd prototype-frontend
npm run build  # Creates dist/ folder

# 2. Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# 3. Create CloudFront distribution pointing to S3
```

---

## 6. MONITORING & HEALTH CHECKS POST-DEPLOYMENT

```bash
# Check backend health
curl https://yourdomain.com/api/health

# Check database connection
curl https://yourdomain.com/api/admin/db-status

# View logs
tail -f /var/log/gunicorn/err.log

# Monitor system resources
top
df -h
```

---

## 7. ENV TEMPLATE FOR PRODUCTION

Copy this to your `.env.production` file and fill in values:

```env
# Core Settings
FLASK_ENV=production
DEBUG=False
SECRET_KEY=GENERATE_WITH_OPENSSL_RAND_HEX_32
FLASK_APP=wsgi.py

# Database
DATABASE_URL=postgresql://networkinsight:YOUR_STRONG_PASSWORD@rds-endpoint:5432/networkinsight

# Cache
REDIS_URL=redis://:YOUR_PASSWORD@redis-endpoint:6379/0

# API Configuration
WORKERS=4
THREAD_POOL=32
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# File Upload
UPLOAD_FOLDER=s3://your-bucket/uploads
MAX_CONTENT_LENGTH=104857600

# Frontend
NODE_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/networkinsight/app.log

# Security (HTTPS)
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true
SECURE_HSTS_PRELOAD=true

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn
```

---

## 8. COMMON PITFALLS & SOLUTIONS

| Issue | Cause | Fix |
|-------|-------|-----|
| 500 Error on first request | `DEBUG=False`, errors not visible | Check logs, enable `SENTRY_DSN` |
| Database connection fails | Wrong connection string | Verify RDS endpoint, security groups |
| CORS errors | Frontend domain not in `CORS_ORIGINS` | Add domain to env variable |
| Slow uploads | Small `MAX_CONTENT_LENGTH` | Increase to 100MB+ |
| High memory usage | Too few workers | Reduce `WORKERS` or increase RAM |
| Session not persisting | Redis connection issues | Check `REDIS_URL` connectivity |

---

## Next Steps

1. **Test your .env.production locally** with `docker-compose.production.yml`
2. **Choose deployment platform** (AWS recommended for scalability)
3. **Set up CI/CD** (GitHub Actions, GitLab CI, AWS CodePipeline)
4. **Configure monitoring** (Sentry, DataDog, CloudWatch)
5. **Enable SSL/HTTPS** (Let's Encrypt or AWS Certificate Manager)
