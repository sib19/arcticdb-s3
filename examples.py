"""
Example usage of Arctic DB Client
Demonstrates all major operations
"""

import pandas as pd
from datetime import datetime, timedelta
from arctic_client import ArcticDBClient

def example_basic_operations():
    """Example: Basic write and read operations"""
    client = ArcticDBClient()
    
    # Create sample data
    data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=5, freq='D'),
        'price': [100.5, 101.2, 99.8, 102.1, 100.9],
        'volume': [1000, 1200, 900, 1100, 950],
        'symbol': ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL']
    }
    df = pd.DataFrame(data)
    
    # Write to Arctic DB
    print("Writing data to Arctic DB...")
    result = client.write('stocks', df)
    print(f"Write result: {result}")
    
    # Read from Arctic DB
    print("\nReading data from Arctic DB...")
    df_read = client.read('stocks')
    print(f"Data shape: {df_read.shape}")
    print(df_read.head())

def example_s3_operations():
    """Example: S3 upload and download"""
    client = ArcticDBClient()
    
    # Sample data
    data = {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'score': [95, 87, 92]
    }
    
    # Upload to S3
    print("Uploading to S3...")
    s3_result = client.upload_to_s3('data/scores.json', data)
    print(f"S3 upload result: {s3_result}")
    
    # Download from S3
    print("\nDownloading from S3...")
    content = client.download_from_s3('data/scores.json')
    print(f"Downloaded content: {content}")

def example_s3_to_db():
    """Example: Load S3 data into Arctic DB"""
    client = ArcticDBClient()
    
    # First upload data to S3
    print("Setting up test data in S3...")
    test_data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'value': [100, 110, 105],
        'status': ['active', 'active', 'inactive']
    }
    client.upload_to_s3('test/load_me.json', test_data)
    
    # Load from S3 to Arctic DB
    print("Loading from S3 to Arctic DB...")
    result = client.load_s3_to_db('test/load_me.json', 'test_table')
    print(f"Load result: {result}")
    
    # Read back from Arctic DB
    print("\nReading from Arctic DB...")
    df = client.read('test_table')
    print(df)

def example_health_and_info():
    """Example: Health check and system info"""
    client = ArcticDBClient()
    
    # Health check
    print("Health check...")
    health = client.health_check()
    print(f"Health: {health}")
    
    # System info
    print("\nSystem info...")
    info = client.get_info()
    print(f"Info: {info}")

if __name__ == '__main__':
    print("=" * 50)
    print("Arctic DB Examples")
    print("=" * 50)
    
    try:
        print("\n1. Basic Operations")
        print("-" * 50)
        example_basic_operations()
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print("\n2. S3 Operations")
        print("-" * 50)
        example_s3_operations()
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print("\n3. S3 to DB")
        print("-" * 50)
        example_s3_to_db()
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        print("\n4. Health and Info")
        print("-" * 50)
        example_health_and_info()
    except Exception as e:
        print(f"Error: {e}")
