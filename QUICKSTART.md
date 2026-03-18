# Arctic DB Docker - Quick Start Guide

## 📋 Overview

This is a complete Arctic DB setup with:
- ✅ Docker containerization with S3 backend
- ✅ REST API with Flask
- ✅ Python client library
- ✅ Example scripts and full documentation
- ✅ Git repository initialized

## 🚀 5-Minute Setup

### Step 1: Configure AWS Credentials

```bash
cd arcticdb-project
cp .env.example .env
```

Edit `.env` with your AWS credentials:
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-existing-bucket-name
```

### Step 2: Start the Container

```bash
docker-compose up -d
```

### Step 3: Verify It's Running

```bash
# Check container status
docker-compose ps

# Health check
curl http://localhost:8080/health

# Expected response:
# {"status": "healthy", "timestamp": "...", "arctic_db": "connected"}
```

## 📚 Project Structure

```
arcticdb-project/
├── app.py                    # Flask API server
├── arctic_client.py         # Python client library
├── examples.py              # Usage examples
├── Dockerfile               # Container image
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── Makefile                 # Development shortcuts
├── .env.example            # Configuration template
├── README.md               # Full documentation
├── API.md                  # API reference
├── setup.sh                # Setup script
└── .git                    # Git repository
```

## 🔌 API Endpoints

### Write Data
```bash
curl -X POST http://localhost:8080/api/v1/write \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "stocks",
    "data": [
      {"date": "2024-01-01", "price": 100.50},
      {"date": "2024-01-02", "price": 101.20}
    ]
  }'
```

### Read Data
```bash
curl http://localhost:8080/api/v1/read/stocks
```

### Upload to S3
```bash
curl -X POST http://localhost:8080/api/v1/s3/upload \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "data/test.json",
    "content": {"test": "data"}
  }'
```

### Load S3 to DB
```bash
curl -X POST http://localhost:8080/api/v1/s3/load-to-db \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "data/test.json",
    "table_name": "imported_data"
  }'
```

## 🐍 Python Client Usage

```python
from arctic_client import ArcticDBClient
import pandas as pd

# Initialize
client = ArcticDBClient()

# Write data
df = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02'],
    'value': [100, 110]
})
client.write('my_table', df)

# Read data
df = client.read('my_table')
print(df)

# S3 operations
client.upload_to_s3('data/file.json', {'key': 'value'})
content = client.download_from_s3('data/file.json')
client.load_s3_to_db('data/file.json', 'imported_table')
```

## 📊 Useful Make Commands

```bash
make help          # Show all available commands
make start         # Start containers
make stop          # Stop containers
make logs          # View logs
make test          # Run tests
make examples      # Run example scripts
make clean         # Remove containers
make health        # Check health
make info          # Get system info
```

## 🔍 Troubleshooting

### Container won't start
```bash
docker-compose logs arctic-db
docker-compose up -d --build
```

### S3 connection error
- Verify `.env` credentials
- Check S3 bucket exists
- Confirm IAM permissions

### Port 8080 already in use
```bash
# Edit docker-compose.yml
# Change ports: ["8081:8080"]
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f arctic-db
# Or from host
tail -f logs/arctic.log
```

## 📁 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask API application |
| `arctic_client.py` | Python client library for API |
| `examples.py` | Usage examples and demos |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `requirements.txt` | Python package dependencies |
| `Makefile` | Development task automation |
| `.env.example` | Configuration template |
| `README.md` | Complete documentation |
| `API.md` | API endpoint reference |

## 🌐 Exposed Port

- **Port 8080**: Arctic DB API
  - Health: `http://localhost:8080/health`
  - API: `http://localhost:8080/api/v1/*`

## 🔐 Security Notes

1. **Never commit `.env`** - Add to `.gitignore` (already done)
2. **Rotate credentials** - Regularly update AWS keys
3. **Use IAM roles** - Prefer IAM over hardcoded keys
4. **HTTPS in production** - Use reverse proxy (nginx/traefik)
5. **Authentication** - Add auth layer for production

## 📤 Git Repository

Repository is already initialized with initial commit:

```bash
# View commit history
git log

# Add remote
git remote add origin https://github.com/your-username/arcticdb-project.git

# Push to GitHub
git push -u origin master
```

## 🧪 Testing the Setup

1. **Start container**
   ```bash
   docker-compose up -d
   ```

2. **Check health**
   ```bash
   curl http://localhost:8080/health
   ```

3. **Run examples**
   ```bash
   python examples.py
   ```

4. **Write test data**
   ```bash
   curl -X POST http://localhost:8080/api/v1/write \
     -H "Content-Type: application/json" \
     -d '{"table_name": "test", "data": [{"id": 1, "name": "test"}]}'
   ```

5. **Read test data**
   ```bash
   curl http://localhost:8080/api/v1/read/test
   ```

## 📚 Next Steps

1. **Configure AWS S3 bucket**
   - Create bucket with S3_BUCKET_NAME from .env
   - Ensure credentials have proper permissions

2. **Customize API**
   - Edit `app.py` for custom logic
   - Add authentication if needed

3. **Deploy to Production**
   - Use Docker Swarm or Kubernetes
   - Add reverse proxy (nginx/traefik)
   - Enable HTTPS
   - Set resource limits

4. **Scale Horizontally**
   - Use Docker Compose with multiple replicas
   - Add load balancer
   - Use S3 for persistent storage

## 📞 Support

- Check `README.md` for comprehensive documentation
- Review `API.md` for endpoint details
- Run `examples.py` for usage patterns
- Check logs: `docker-compose logs -f`

## 📄 License

MIT License

---

**Happy Arctic DB-ing! 🎉**
