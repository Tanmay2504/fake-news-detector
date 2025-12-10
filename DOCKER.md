# Docker Quick Start

## Build and Run

### Using Docker
```bash
# Build image
docker build -t fake-news-api .

# Run container
docker run -d -p 8000:8000 \
  -v ${PWD}/models:/app/models \
  -v ${PWD}/google-vision-credentials.json:/app/google-vision-credentials.json \
  --name fake-news-api \
  fake-news-api

# Check logs
docker logs -f fake-news-api

# Stop container
docker stop fake-news-api

# Remove container
docker rm fake-news-api
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Access API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Important Notes

1. **Models**: Place your trained models in `models/` directory BEFORE building
2. **Credentials**: Place `google-vision-credentials.json` in project root
3. **Port**: Default port is 8000, change in docker-compose.yml if needed
4. **Volumes**: Models are mounted as volumes for easy updates
