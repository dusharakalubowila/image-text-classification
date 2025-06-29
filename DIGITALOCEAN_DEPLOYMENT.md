# DigitalOcean Deployment Guide

## Method 1: DigitalOcean App Platform (Recommended)

### Step 1: Prepare Your Repository
Your repository is already configured with:
- ✅ `.do/app.yaml` - App Platform configuration
- ✅ `gunicorn_config.py` - Optimized Gunicorn settings
- ✅ `Dockerfile` - Container configuration
- ✅ `requirements.txt` - Python dependencies

### Step 2: Deploy to App Platform

1. **Go to DigitalOcean Console**
   - Visit: https://cloud.digitalocean.com/apps
   - Click "Create App"

2. **Connect GitHub Repository**
   - Choose "GitHub" as source
   - Select repository: `dusharakalubowila/image-text-classification`
   - Branch: `main`
   - Auto-deploy: ✅ Enabled

3. **Configure App Settings**
   - **App Name**: `image-text-classification`
   - **Region**: Choose closest to your users
   - **Plan**: Basic ($5/month) or Pro ($12/month) for better performance

4. **Review Configuration**
   - App Platform will auto-detect the Python app
   - It will use the `.do/app.yaml` configuration
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --config gunicorn_config.py app:app`

5. **Deploy**
   - Click "Create Resources"
   - Wait 5-10 minutes for deployment
   - Your app will be available at: `https://your-app-name.ondigitalocean.app`

### Step 3: Configure Environment (if needed)

In the App Platform console, you can set environment variables:
- `PORT=8080` (usually auto-configured)
- `PYTHONPATH=/app`

### Expected Costs:
- **Basic Plan**: $5/month (512MB RAM, 1 vCPU)
- **Professional Plan**: $12/month (1GB RAM, 1 vCPU) - Recommended for ML apps

---

## Method 2: DigitalOcean Droplet (Manual Setup)

### Step 1: Create Droplet

1. **Create Droplet**
   - Image: Ubuntu 22.04 LTS
   - Size: $12/month (2GB RAM, 1 vCPU) minimum
   - Region: Choose closest to users
   - SSH Keys: Add your SSH key

### Step 2: Server Setup

1. **Connect to Droplet**
```bash
ssh root@your_droplet_ip
```

2. **Update System**
```bash
apt update && apt upgrade -y
```

3. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

4. **Clone Repository**
```bash
git clone https://github.com/dusharakalubowila/image-text-classification.git
cd image-text-classification
```

5. **Build and Run**
```bash
docker build -t image-classifier .
docker run -d -p 80:8080 --name ml-app image-classifier
```

### Step 3: Configure Domain (Optional)

1. **Point Domain to Droplet IP**
2. **Install Nginx (for SSL)**
```bash
apt install nginx certbot python3-certbot-nginx -y
```

3. **Configure Nginx**
```bash
# Create nginx config
cat > /etc/nginx/sites-available/ml-app << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/ml-app /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

4. **Get SSL Certificate**
```bash
certbot --nginx -d your-domain.com
```

---

## Deployment Commands Summary

### For App Platform:
```bash
# Already done - just use the web interface
# Your repo is ready with .do/app.yaml configuration
```

### For Droplet with Docker:
```bash
# On your droplet
git clone https://github.com/dusharakalubowila/image-text-classification.git
cd image-text-classification
docker build -t image-classifier .
docker run -d -p 80:8080 --restart unless-stopped --name ml-app image-classifier
```

## Monitoring and Logs

### App Platform:
- View logs in DigitalOcean console
- Runtime metrics available in dashboard
- Auto-scaling and health checks included

### Droplet:
```bash
# View Docker logs
docker logs ml-app

# Check container status
docker ps

# Restart if needed
docker restart ml-app
```

## Troubleshooting

### Common Issues:

1. **Memory Issues**
   - Upgrade to higher plan (Professional $12/month)
   - Add swap file on Droplet

2. **Build Timeout**
   - Use pre-built Docker image
   - Optimize requirements.txt

3. **Tesseract Not Found**
   - Already handled in Dockerfile
   - System dependencies included

### Debug Commands:
```bash
# Test locally
docker run -it --rm image-classifier bash

# Check health endpoint
curl https://your-app.ondigitalocean.app/health
```

---

## Recommended: App Platform

**Advantages:**
- ✅ Automatic deployments from GitHub
- ✅ Built-in load balancing
- ✅ SSL certificates included
- ✅ Monitoring and logging
- ✅ Easy scaling
- ✅ No server management

**Perfect for your ML app!** 🚀
