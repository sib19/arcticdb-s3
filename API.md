# Arctic DB API Documentation

## Base URL

```
http://localhost:8080
```

## Authentication

Currently no authentication required. Consider implementing in production.

## Response Format

All responses are JSON with the following structure:

### Success Response (2xx)
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

---

## Endpoints

### Health & System

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "arctic_db": "connected"
}
```

**Example:**
```bash
curl http://localhost:8080/health
```

---

#### GET /api/v1/info
Get system information and library list.

**Response:**
```json
{
  "status": "success",
  "arctic_uri": "s3://arcticdb-data",
  "s3_bucket": "arcticdb-storage",
  "libraries": ["library1", "library2"],
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/info
```

---

### Arctic DB Operations

#### POST /api/v1/write
Write data to Arctic DB.

**Request Body:**
```json
{
  "table_name": "stocks",
  "data": [
    {
      "date": "2024-01-01",
      "symbol": "AAPL",
      "price": 150.50,
      "volume": 1000000
    },
    {
      "date": "2024-01-02",
      "symbol": "AAPL",
      "price": 151.20,
      "volume": 1100000
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "table_name": "stocks",
  "rows_written": 2,
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/api/v1/write \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "stocks",
    "data": [
      {"date": "2024-01-01", "price": 150.50}
    ]
  }'
```

**Status Codes:**
- `200` - Data written successfully
- `400` - Missing table_name or data
- `500` - Server error

---

#### GET /api/v1/read/{table_name}
Read data from Arctic DB table.

**Path Parameters:**
- `table_name` (string, required) - Name of table to read

**Response:**
```json
{
  "status": "success",
  "table_name": "stocks",
  "rows": 2,
  "data": [
    {
      "date": "2024-01-01",
      "symbol": "AAPL",
      "price": 150.50,
      "volume": 1000000
    },
    {
      "date": "2024-01-02",
      "symbol": "AAPL",
      "price": 151.20,
      "volume": 1100000
    }
  ],
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/read/stocks
```

**Status Codes:**
- `200` - Data read successfully
- `404` - Table not found
- `500` - Server error

---

### S3 Operations

#### POST /api/v1/s3/upload
Upload file to S3 bucket.

**Request Body:**
```json
{
  "file_key": "data/myfile.json",
  "content": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "bucket": "arcticdb-storage",
  "key": "arctic-data/data/myfile.json",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/api/v1/s3/upload \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "data/test.json",
    "content": {"test": "data"}
  }'
```

**Status Codes:**
- `200` - File uploaded successfully
- `400` - Missing file_key or content
- `500` - Server error

---

#### GET /api/v1/s3/download/{file_key}
Download file from S3 bucket.

**Path Parameters:**
- `file_key` (string, required) - Path to file in S3

**Response:**
```json
{
  "status": "success",
  "bucket": "arcticdb-storage",
  "key": "arctic-data/data/myfile.json",
  "content": {
    "key1": "value1",
    "key2": "value2"
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/s3/download/data/myfile.json
```

**Status Codes:**
- `200` - File downloaded successfully
- `404` - File not found
- `500` - Server error

---

#### POST /api/v1/s3/load-to-db
Load data from S3 into Arctic DB.

**Request Body:**
```json
{
  "file_key": "data/import.json",
  "table_name": "imported_data"
}
```

**Response:**
```json
{
  "status": "success",
  "source": {
    "bucket": "arcticdb-storage",
    "key": "arctic-data/data/import.json"
  },
  "destination": {
    "table": "imported_data"
  },
  "rows_loaded": 100,
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/api/v1/s3/load-to-db \
  -H "Content-Type: application/json" \
  -d '{
    "file_key": "data/import.json",
    "table_name": "imported_data"
  }'
```

**Status Codes:**
- `200` - Data loaded successfully
- `400` - Missing file_key or table_name
- `404` - File not found
- `500` - Server error

---

## Rate Limiting

Currently no rate limiting implemented. Consider adding for production.

## Error Handling

All errors return appropriate HTTP status codes with error messages:

```json
{
  "error": "Descriptive error message",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

---

## Pagination

Not implemented. Consider for large datasets.

---

## Versioning

API version: `v1`

Future versions would use `/api/v2/`, `/api/v3/`, etc.

---

## Implementation Notes

- All timestamps are in ISO 8601 format
- Data is stored as JSON
- S3 keys are prefixed with configured S3_PREFIX
- Arctic DB creates libraries automatically as needed
- Concurrent writes to same table are supported
