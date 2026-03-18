import os
import json
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import boto3
import pandas as pd
from arcticdb import Arctic
import traceback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/arctic.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Arctic DB Configuration
class ArcticDBConfig:
    def __init__(self):
        self.uri = os.getenv('ARCTICDB_URI', 's3://arcticdb-data')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_bucket = os.getenv('S3_BUCKET_NAME', 'arcticdb-storage')
        self.s3_prefix = os.getenv('S3_PREFIX', 'arctic-data/')

# Initialize clients
config = ArcticDBConfig()
s3_client = boto3.client(
    's3',
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_secret_key,
    region_name=config.aws_region
)

# Arctic DB instance
try:
    ac = Arctic(config.uri)
    logger.info(f"Connected to Arctic DB at {config.uri}")
except Exception as e:
    logger.error(f"Failed to connect to Arctic DB: {str(e)}")
    ac = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'arctic_db': 'connected' if ac else 'disconnected'
    }), 200

@app.route('/api/v1/write', methods=['POST'])
def write_data():
    """Write data to Arctic DB"""
    try:
        data = request.get_json()
        table_name = data.get('table_name')
        df_data = data.get('data')
        
        if not table_name or not df_data:
            return jsonify({'error': 'Missing table_name or data'}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(df_data)
        
        # Get or create library
        lib = ac.get_library(table_name, create_if_missing=True)
        
        # Write to Arctic DB
        lib.write(table_name, df)
        
        logger.info(f"Successfully wrote {len(df)} rows to {table_name}")
        
        return jsonify({
            'status': 'success',
            'table_name': table_name,
            'rows_written': len(df),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error writing data: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/read/<table_name>', methods=['GET'])
def read_data(table_name):
    """Read data from Arctic DB"""
    try:
        lib = ac.get_library(table_name, create_if_missing=False)
        df = lib.read(table_name).data
        
        logger.info(f"Successfully read {len(df)} rows from {table_name}")
        
        return jsonify({
            'status': 'success',
            'table_name': table_name,
            'rows': len(df),
            'data': df.to_dict('records'),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error reading data: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/s3/upload', methods=['POST'])
def upload_to_s3():
    """Upload data file to S3"""
    try:
        data = request.get_json()
        file_key = data.get('file_key')
        content = data.get('content')
        
        if not file_key or not content:
            return jsonify({'error': 'Missing file_key or content'}), 400
        
        # Upload to S3
        s3_key = f"{config.s3_prefix}{file_key}"
        s3_client.put_object(
            Bucket=config.s3_bucket,
            Key=s3_key,
            Body=json.dumps(content) if isinstance(content, dict) else content,
            ContentType='application/json'
        )
        
        logger.info(f"Successfully uploaded {s3_key} to S3")
        
        return jsonify({
            'status': 'success',
            'bucket': config.s3_bucket,
            'key': s3_key,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading to S3: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/s3/download/<path:file_key>', methods=['GET'])
def download_from_s3(file_key):
    """Download data file from S3"""
    try:
        s3_key = f"{config.s3_prefix}{file_key}"
        
        response = s3_client.get_object(Bucket=config.s3_bucket, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
        
        logger.info(f"Successfully downloaded {s3_key} from S3")
        
        return jsonify({
            'status': 'success',
            'bucket': config.s3_bucket,
            'key': s3_key,
            'content': json.loads(content) if content.startswith('{') else content,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except s3_client.exceptions.NoSuchKey:
        return jsonify({'error': f'File not found: {file_key}'}), 404
    except Exception as e:
        logger.error(f"Error downloading from S3: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/s3/load-to-db', methods=['POST'])
def load_s3_to_db():
    """Load data from S3 into Arctic DB"""
    try:
        data = request.get_json()
        file_key = data.get('file_key')
        table_name = data.get('table_name')
        
        if not file_key or not table_name:
            return jsonify({'error': 'Missing file_key or table_name'}), 400
        
        # Download from S3
        s3_key = f"{config.s3_prefix}{file_key}"
        response = s3_client.get_object(Bucket=config.s3_bucket, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
        
        # Parse and write to Arctic DB
        df_data = json.loads(content)
        df = pd.DataFrame(df_data)
        
        lib = ac.get_library(table_name, create_if_missing=True)
        lib.write(table_name, df)
        
        logger.info(f"Successfully loaded {s3_key} into {table_name}")
        
        return jsonify({
            'status': 'success',
            'source': {'bucket': config.s3_bucket, 'key': s3_key},
            'destination': {'table': table_name},
            'rows_loaded': len(df),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error loading S3 to DB: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/info', methods=['GET'])
def info():
    """Get system information"""
    try:
        libraries = [lib for lib in ac.list_libraries()]
        return jsonify({
            'status': 'success',
            'arctic_uri': config.uri,
            's3_bucket': config.s3_bucket,
            'libraries': libraries,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Arctic DB API Server")
    app.run(host='0.0.0.0', port=8080, debug=False)
