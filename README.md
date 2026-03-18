# Arctic DB Docker Container with S3 Integration

Complete Docker setup for Arctic DB with S3 storage backend, API endpoints, and Python client library.

## Features

- **Arctic DB**: High-performance time series database
- **S3 Integration**: Store and retrieve files from AWS S3
- **REST API**: Flask-based API for all operations
- **Docker Support**: Full containerization with Docker & Docker Compose
- **Python Client**: Easy-to-use client library for API operations
- **Health Checks**: Built-in health check endpoints
- **Logging**: Comprehensive logging to file and stdout

## Project Structure

```
arcticdb-project/
├── app.py                    # Main Flask application
├── arctic_client.py         # Python client library
├── examples.py              # Usage examples
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── data/                   # Local data storage
├── logs/                   # Application logs
└── config/                 # Configuration files
```

## Prerequisites

- Docker & Docker Compose (or Python 3.11+)
- AWS Account with S3 bucket and credentials
- Git

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd arcticdb-project
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your AWS credentials:

```bash
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

### 4. Verify Container

```bash
# Check logs
docker-compose logs -f arctic-db

# Health check
curl http://localhost:8080/health

# System info
curl http://localhost:8080/api/v1/info
```

## API Endpoints

### Health & Info

#### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "arctic_db": "connected"
}
```

#### System Info
```bash
GET /api/v1/info

Response:
{
  "status": "success",
  "arctic_uri": "s3://arcticdb-data",
  "s3_bucket": "arcticdb-storage",
  "libraries": ["lib1", "lib2"],
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### Arctic DB Operations

#### Write Data
```bash
POST /api/v1/write

Request:
{
  "table_name": "stocks",
  "data": [
    {"date": "2024-01-01", "price": 100.5, "volume": 1000},
    {"date": "2024-01-02", "price": 101.2, "volume": 1200}
  ]
}

Response:
{
  "status": "success",
  "table_name": "stocks",
  "rows_written": 2,
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### Read Data
```bash
GET /api/v1/read/{table_name}

Response:
{
  "status": "success",
  "table_name": "stocks",
  "rows": 2,
  "data": [
    {"date": "2024-01-01", "price": 100.5, "volume": 1000},
    {"date": "2024-01-02", "price": 101.2, "volume": 1200}
  ],
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### S3 Operations

#### Upload to S3
```bash
POST /api/v1/s3/upload

Request:
{
  "file_key": "data/myfile.json",
  "content": {"key": "value"}
}

Response:
{
  "status": "success",
  "bucket": "arcticdb-storage",
  "key": "arctic-data/data/myfile.json",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### Download from S3
```bash
GET /api/v1/s3/download/{file_key}

Response:
{
  "status": "success",
  "bucket": "arcticdb-storage",
  "key": "arctic-data/data/myfile.json",
  "content": {"key": "value"},
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

#### Load S3 to Arctic DB
```bash
POST /api/v1/s3/load-to-db

Request:
{
  "file_key": "data/myfile.json",
  "table_name": "imported_data"
}

Response:
{
  "status": "success",
  "source": {
    "bucket": "arcticdb-storage",
    "key": "arctic-data/data/myfile.json"
  },
  "destination": {"table": "imported_data"},
  "rows_loaded": 100,
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

## Python Client Usage

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from arctic_client import ArcticDBClient
import pandas as pd

# Initialize client
client = ArcticDBClient(base_url="http://localhost:8080")

# Health check
health = client.health_check()
print(health)

# Write data
df = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02'],
    'value': [100, 110]
})
result = client.write('my_table', df)
print(result)

# Read data
df = client.read('my_table')
print(df)

# Upload to S3
client.upload_to_s3('data/file.json', {'test': 'data'})

# Download from S3
content = client.download_from_s3('data/file.json')

# Load S3 to DB
client.load_s3_to_db('data/file.json', 'imported_table')
```

### Run Examples

```bash
python examples.py
```

## Docker Commands

### Build Image

```bash
docker build -t arcticdb:latest .
```

### Run Container Directly

```bash
docker run -d \
  -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e S3_BUCKET_NAME=your-bucket \
  --name arcticdb-server \
  arcticdb:latest
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f arctic-db

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Remove volumes
docker-compose down -v
```

## Logs

View application logs:

```bash
# Inside container
docker-compose exec arctic-db tail -f /app/logs/arctic.log

# From host (after mounting)
tail -f logs/arctic.log
```

## Configuration

Edit `.env` file to customize:

```bash
# Arctic DB
ARCTICDB_URI=s3://arcticdb-data

# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# S3
S3_BUCKET_NAME=your-bucket
S3_PREFIX=arctic-data/

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
```

## Testing

### Health Check

```bash
curl http://localhost:8080/health
```

### Sample Request

```bash
curl -X POST http://localhost:8080/api/v1/write \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "test",
    "data": [
      {"id": 1, "name": "test", "value": 100}
    ]
  }'
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs arctic-db

# Rebuild
docker-compose up -d --build
```

### S3 Connection Issues

- Verify AWS credentials in `.env`
- Check bucket exists and permissions
- Verify S3_BUCKET_NAME is correct

### Port Already in Use

```bash
# Change port in docker-compose.yml
# ports:
#   - "8081:8080"

docker-compose up -d
```

### Permission Denied

```bash
# Fix file permissions
chmod +x app.py
```

## Performance Tuning

### Increase Workers

Edit `Dockerfile`:

```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

### Resource Limits

Edit `docker-compose.yml`:

```yaml
resources:
  limits:
    cpus: '2.0'
    memory: 2G
```

## Security Considerations

1. **Never commit `.env` file** - Always use `.env.example`
2. **Rotate AWS credentials** - Regularly update access keys
3. **Use IAM roles** - Prefer IAM roles over hardcoded credentials
4. **Network policies** - Restrict container network access
5. **HTTPS in Production** - Use reverse proxy (nginx, traefik)

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## License

MIT License

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review examples: `python examples.py`
- Verify configuration: Check `.env` file

## Related Documentation

- [Arctic DB Documentation](https://arcticdb.io/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
