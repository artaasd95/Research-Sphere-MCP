# Deployment Guide

This guide provides instructions for deploying the MCP RAG System in various environments.

## Prerequisites

- Docker and Docker Compose
- Git
- Python 3.8+ (for local development)
- Node.js 16+ (for local development)
- OpenAI API key

## Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
OPENAI_API_KEY=your-api-key
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
ENVIRONMENT=production

# Frontend
VITE_API_URL=http://localhost:8000
VITE_OPENAI_API_KEY=your-api-key
```

## Deployment Options

### 1. Docker Deployment

#### Using Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/mcp-rag.git
   cd mcp-rag
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Verify deployment:
   ```bash
   docker-compose ps
   ```

#### Using Individual Containers

1. Build the backend image:
   ```bash
   cd backend
   docker build -t mcp-rag-backend .
   ```

2. Build the frontend image:
   ```bash
   cd frontend
   docker build -t mcp-rag-frontend .
   ```

3. Run the containers:
   ```bash
   # Backend
   docker run -d \
     --name mcp-rag-backend \
     -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/logs:/app/logs \
     --env-file .env \
     mcp-rag-backend

   # Frontend
   docker run -d \
     --name mcp-rag-frontend \
     -p 3000:3000 \
     --env-file .env \
     mcp-rag-frontend
   ```

### 2. Standalone Deployment

#### Backend Deployment

1. Set up Python environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

#### Frontend Deployment

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Build the application:
   ```bash
   npm run build
   ```

4. Serve the application:
   ```bash
   npm run preview
   ```

### 3. Production Deployment

#### Using Nginx

1. Install Nginx:
   ```bash
   sudo apt-get update
   sudo apt-get install nginx
   ```

2. Configure Nginx:
   ```nginx
   # /etc/nginx/sites-available/mcp-rag
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/mcp-rag /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

#### Using Systemd

1. Create backend service:
   ```ini
   # /etc/systemd/system/mcp-rag-backend.service
   [Unit]
   Description=MCP RAG Backend
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/mcp-rag/backend
   Environment="PATH=/path/to/mcp-rag/backend/venv/bin"
   ExecStart=/path/to/mcp-rag/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. Create frontend service:
   ```ini
   # /etc/systemd/system/mcp-rag-frontend.service
   [Unit]
   Description=MCP RAG Frontend
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/mcp-rag/frontend
   ExecStart=/usr/bin/npm run preview
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start services:
   ```bash
   sudo systemctl enable mcp-rag-backend
   sudo systemctl enable mcp-rag-frontend
   sudo systemctl start mcp-rag-backend
   sudo systemctl start mcp-rag-frontend
   ```

## Monitoring

### Logs

1. Docker logs:
   ```bash
   docker-compose logs -f
   ```

2. Systemd logs:
   ```bash
   journalctl -u mcp-rag-backend -f
   journalctl -u mcp-rag-frontend -f
   ```

### Health Checks

1. API health check:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. Frontend health check:
   ```bash
   curl http://localhost:3000/health
   ```

## Backup and Recovery

### Data Backup

1. Backup vector store:
   ```bash
   tar -czf vector_store_backup.tar.gz /path/to/data/vector_store
   ```

2. Backup documents:
   ```bash
   tar -czf documents_backup.tar.gz /path/to/data/documents
   ```

### Recovery

1. Restore vector store:
   ```bash
   tar -xzf vector_store_backup.tar.gz -C /path/to/data
   ```

2. Restore documents:
   ```bash
   tar -xzf documents_backup.tar.gz -C /path/to/data
   ```

## Scaling

### Horizontal Scaling

1. Load balancer configuration:
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

2. Docker Swarm deployment:
   ```bash
   docker swarm init
   docker stack deploy -c docker-compose.yml mcp-rag
   ```

### Vertical Scaling

1. Increase container resources:
   ```yaml
   # docker-compose.yml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

## Security

### SSL/TLS Configuration

1. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

2. Configure Nginx:
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
   }
   ```

### Firewall Configuration

1. Configure UFW:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

## Troubleshooting

### Common Issues

1. Container fails to start:
   ```bash
   docker-compose logs backend
   ```

2. API connection issues:
   ```bash
   curl -v http://localhost:8000/api/v1/health
   ```

3. Frontend build fails:
   ```bash
   npm run build --verbose
   ```

### Performance Issues

1. Check resource usage:
   ```bash
   docker stats
   ```

2. Monitor logs:
   ```bash
   tail -f /path/to/logs/app.log
   ```

## Maintenance

### Updates

1. Pull latest changes:
   ```bash
   git pull origin main
   ```

2. Rebuild containers:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

### Cleanup

1. Remove old containers:
   ```bash
   docker system prune
   ```

2. Clean logs:
   ```bash
   find /path/to/logs -type f -name "*.log" -mtime +30 -delete
   ``` 