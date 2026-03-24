#!/usr/bin/env python3
“””
ArcticDB on EC2 with S3 Backend
Demonstrates reading, writing, and managing tables in ArcticDB with S3 storage
“””

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from arcticdb import Arctic
import boto3

# Configuration

S3_BUCKET = os.getenv(‘ARCTIC_S3_BUCKET’, ‘your-bucket-name’)
S3_REGION = os.getenv(‘AWS_REGION’, ‘us-east-1’)
ARCTIC_PREFIX = ‘arcticdb/’  # S3 prefix for ArcticDB data

class ArcticS3Manager:
“”“Manager for ArcticDB operations with S3 backend”””

```
def __init__(self, s3_bucket: str, region: str = 'us-east-1'):
    """
    Initialize ArcticDB with S3 backend
    
    Args:
        s3_bucket: S3 bucket name
        region: AWS region
    """
    self.s3_bucket = s3_bucket
    self.region = region
    self.s3_client = boto3.client('s3', region_name=region)
    
    # Initialize Arctic with S3 URI
    uri = f"s3://{s3_bucket}/{ARCTIC_PREFIX}"
    print(f"Connecting to ArcticDB: {uri}")
    self.ac = Arctic(uri)
    
def create_sample_dataframe(self, rows: int = 1000) -> pd.DataFrame:
    """Generate sample dataframe for testing"""
    dates = [datetime.now() - timedelta(days=x) for x in range(rows)]
    data = {
        'timestamp': dates,
        'sensor_id': np.random.randint(1, 10, rows),
        'temperature': np.random.normal(20, 5, rows),
        'humidity': np.random.uniform(30, 80, rows),
        'pressure': np.random.normal(1013, 10, rows),
        'status': np.random.choice(['OK', 'WARNING', 'ERROR'], rows)
    }
    return pd.DataFrame(data)

def write_data(self, lib_name: str, table_name: str, df: pd.DataFrame):
    """
    Write DataFrame to ArcticDB
    
    Args:
        lib_name: Library name (similar to database)
        table_name: Table name
        df: pandas DataFrame to write
    """
    try:
        lib = self.ac.get_or_create_library(lib_name)
        lib.write(table_name, df)
        print(f"✓ Written {len(df)} rows to {lib_name}.{table_name}")
        return True
    except Exception as e:
        print(f"✗ Error writing data: {e}")
        return False

def read_data(self, lib_name: str, table_name: str) -> pd.DataFrame:
    """
    Read DataFrame from ArcticDB
    
    Args:
        lib_name: Library name
        table_name: Table name
        
    Returns:
        pandas DataFrame
    """
    try:
        lib = self.ac.get_or_create_library(lib_name)
        df = lib.read(table_name).data
        print(f"✓ Read {len(df)} rows from {lib_name}.{table_name}")
        return df
    except Exception as e:
        print(f"✗ Error reading data: {e}")
        return None

def update_data(self, lib_name: str, table_name: str, df: pd.DataFrame):
    """Update existing table (overwrites)"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        lib.write(table_name, df)
        print(f"✓ Updated {lib_name}.{table_name}")
    except Exception as e:
        print(f"✗ Error updating data: {e}")

def append_data(self, lib_name: str, table_name: str, df: pd.DataFrame):
    """Append data to existing table"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        # ArcticDB doesn't have native append; read, concat, write
        try:
            existing = lib.read(table_name).data
            df_combined = pd.concat([existing, df], ignore_index=True)
            lib.write(table_name, df_combined)
            print(f"✓ Appended {len(df)} rows to {lib_name}.{table_name}")
        except:
            # Table doesn't exist, create new
            lib.write(table_name, df)
            print(f"✓ Created new table and wrote {len(df)} rows")
    except Exception as e:
        print(f"✗ Error appending data: {e}")

def list_libraries(self) -> list:
    """List all libraries in ArcticDB"""
    try:
        libs = self.ac.list_libraries()
        print(f"✓ Found {len(libs)} libraries")
        return libs
    except Exception as e:
        print(f"✗ Error listing libraries: {e}")
        return []

def list_tables(self, lib_name: str) -> list:
    """List all tables in a library"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        tables = lib.list_versions()
        print(f"✓ Found {len(tables)} tables in {lib_name}")
        return tables
    except Exception as e:
        print(f"✗ Error listing tables: {e}")
        return []

def delete_table(self, lib_name: str, table_name: str):
    """Delete a table"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        lib.delete(table_name)
        print(f"✓ Deleted {lib_name}.{table_name}")
    except Exception as e:
        print(f"✗ Error deleting table: {e}")

def get_table_info(self, lib_name: str, table_name: str):
    """Get metadata about a table"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        df = lib.read(table_name).data
        print(f"\n=== Table Info: {lib_name}.{table_name} ===")
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"Size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"Dtypes:\n{df.dtypes}")
        return df.info()
    except Exception as e:
        print(f"✗ Error getting table info: {e}")

def query_by_range(self, lib_name: str, table_name: str, 
                  col: str, start: float, end: float) -> pd.DataFrame:
    """Query data within a range"""
    try:
        lib = self.ac.get_or_create_library(lib_name)
        df = lib.read(table_name).data
        filtered = df[(df[col] >= start) & (df[col] <= end)]
        print(f"✓ Filtered {len(filtered)} rows from {len(df)} total")
        return filtered
    except Exception as e:
        print(f"✗ Error querying data: {e}")
        return None

def verify_s3_access(self) -> bool:
    """Verify S3 bucket access"""
    try:
        self.s3_client.head_bucket(Bucket=self.s3_bucket)
        print(f"✓ S3 bucket access verified: {self.s3_bucket}")
        
        # List objects in ArcticDB prefix
        response = self.s3_client.list_objects_v2(
            Bucket=self.s3_bucket,
            Prefix=ARCTIC_PREFIX,
            MaxKeys=10
        )
        if 'Contents' in response:
            print(f"✓ Found {len(response['Contents'])} objects in {ARCTIC_PREFIX}")
        return True
    except Exception as e:
        print(f"✗ S3 access error: {e}")
        return False
```

def main():
“”“Main demo”””

```
# Verify bucket is set
if S3_BUCKET == 'your-bucket-name':
    print("ERROR: Set ARCTIC_S3_BUCKET environment variable")
    print("Example: export ARCTIC_S3_BUCKET=my-arcticdb-bucket")
    return

# Initialize manager
mgr = ArcticS3Manager(S3_BUCKET, S3_REGION)

# Verify S3 access
print("\n=== Verifying S3 Access ===")
if not mgr.verify_s3_access():
    print("FAILED: Cannot access S3 bucket. Check IAM permissions.")
    return

# Create sample data
print("\n=== Creating Sample Data ===")
df_sensors = mgr.create_sample_dataframe(rows=1000)
print(f"Sample shape: {df_sensors.shape}")
print(f"First rows:\n{df_sensors.head()}")

# Write data
print("\n=== Writing Data ===")
mgr.write_data('sensor_lib', 'temperature_readings', df_sensors)

# Read data back
print("\n=== Reading Data ===")
df_read = mgr.read_data('sensor_lib', 'temperature_readings')
print(f"Read back shape: {df_read.shape}")

# Get table info
print("\n=== Table Info ===")
mgr.get_table_info('sensor_lib', 'temperature_readings')

# Query by range
print("\n=== Query by Range (temp 15-25°C) ===")
df_filtered = mgr.query_by_range('sensor_lib', 'temperature_readings', 
                                  'temperature', 15, 25)
if df_filtered is not None:
    print(f"Temperature stats:\n{df_filtered['temperature'].describe()}")

# Append more data
print("\n=== Appending More Data ===")
df_new = mgr.create_sample_dataframe(rows=500)
mgr.append_data('sensor_lib', 'temperature_readings_v2', df_new)

# List libraries and tables
print("\n=== Libraries ===")
libs = mgr.list_libraries()
for lib in libs:
    print(f"  - {lib}")
    mgr.list_tables(lib)

# Create multiple tables
print("\n=== Creating Multiple Tables ===")
mgr.write_data('sensor_lib', 'humidity_readings', df_sensors)
mgr.write_data('sensor_lib', 'pressure_readings', df_sensors)

# List all tables in library
print("\n=== All Tables in sensor_lib ===")
tables = mgr.list_tables('sensor_lib')
for table in tables:
    print(f"  - {table}")

print("\n✓ Demo Complete!")
```

if **name** == ‘**main**’:
main()