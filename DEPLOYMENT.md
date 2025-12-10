# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# 1. Clone repository
cd "Fake News V2"

# 2. Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run setup
python setup.py

# 5. Add your trained models
# Place these files in models/ directory:
# - random_forest.joblib
# - lightgbm.joblib
# - xgboost.joblib

# 6. Start server
python main.py
```

---

## Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run
```bash
# Build image
docker build -t fake-news-api .

# Run container
docker run -d -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/google-vision-credentials.json:/app/google-vision-credentials.json \
  --name fake-news-api \
  fake-news-api

# Check logs
docker logs -f fake-news-api
```

---

## Production Deployment

### Cloud Platforms

#### AWS (EC2 + ECS)
1. **EC2 Instance**: Launch Ubuntu 20.04 t2.medium
2. **Install Dependencies**: Python 3.11, Docker
3. **Upload Models**: Use S3 for model storage
4. **Configure Security**: Open port 8000 in security group
5. **Use ECS**: For container orchestration

#### Google Cloud (Cloud Run)
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/fake-news-api

# Deploy to Cloud Run
gcloud run deploy fake-news-api \
  --image gcr.io/PROJECT_ID/fake-news-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

#### Azure (App Service)
```bash
# Create App Service
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name fake-news-api \
  --runtime "PYTHON:3.11"

# Deploy
az webapp up --name fake-news-api
```

#### Heroku
```bash
# Create app
heroku create fake-news-api

# Add buildpacks
heroku buildpacks:add heroku/python

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1
```

---

## Nginx Reverse Proxy

### Install Nginx
```bash
sudo apt update
sudo apt install nginx
```

### Configure
```nginx
# /etc/nginx/sites-available/fake-news-api
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable and Start
```bash
sudo ln -s /etc/nginx/sites-available/fake-news-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Process Manager (PM2)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
# ecosystem.config.js
module.exports = {
  apps: [{
    name: 'fake-news-api',
    script: 'uvicorn',
    args: 'main:app --host 0.0.0.0 --port 8000',
    interpreter: 'python3',
    instances: 4,
    exec_mode: 'cluster',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};

# Start
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# Save and auto-start
pm2 save
pm2 startup
```

---

## Environment Variables

### Production .env
```bash
# Server
HOST=0.0.0.0
PORT=8000

# Models
MODEL_DIR=/app/models
RF_MODEL_PATH=/app/models/random_forest.joblib
LGB_MODEL_PATH=/app/models/lightgbm.joblib
XGB_MODEL_PATH=/app/models/xgboost.joblib

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/app/google-vision-credentials.json

# Cache
CACHE_ENABLED=true
CACHE_MAX_SIZE=5000
CACHE_TTL=3600

# Security
ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
```

---

## Performance Optimization

### 1. Gunicorn Workers
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### 2. Redis Caching
```python
# Replace in-memory cache with Redis
import redis
from functools import lru_cache

redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

### 3. Model Loading
- Use model versioning
- Load models lazily
- Share models across workers

### 4. Database
- Store predictions in PostgreSQL
- Track analytics and metrics
- Enable audit logging

---

## Monitoring

### 1. Application Monitoring
```python
# Install prometheus client
pip install prometheus-fastapi-instrumentator

# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 2. Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 3. Health Checks
- `/health` endpoint for load balancers
- Monitor model accuracy drift
- Track prediction distribution
- Alert on errors

---

## Security

### 1. API Keys
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
```

### 2. Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: Request, ...):
    ...
```

### 3. CORS
```python
# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Scaling

### Horizontal Scaling
- Use load balancer (nginx, AWS ELB)
- Multiple API instances
- Shared Redis cache
- Centralized model storage (S3)

### Vertical Scaling
- Increase server resources
- More CPU for faster inference
- More RAM for larger models
- GPU for deep learning models

---

## Backup and Recovery

### 1. Model Backups
```bash
# Backup models to S3
aws s3 sync models/ s3://your-bucket/models/

# Restore
aws s3 sync s3://your-bucket/models/ models/
```

### 2. Database Backups
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

---

## Testing

### Load Testing
```bash
# Install locust
pip install locust

# Run test
locust -f load_test.py --host http://localhost:8000
```

### Integration Testing
```bash
# Run API tests
python test_api.py

# Run with pytest
pytest tests/
```

---

## Cost Optimization

1. **Use Spot Instances**: 70% cheaper on AWS
2. **Auto-scaling**: Scale down during low traffic
3. **Model Compression**: Reduce model size
4. **Caching**: Reduce redundant predictions
5. **CDN**: Cache static responses
