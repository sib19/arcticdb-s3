"""
Arctic DB Python Client Library
Provides convenient interface for Arctic DB API operations
"""

import requests
import pandas as pd
import json
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

class ArcticDBClient:
    """Client for Arctic DB API"""
    
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30):
        """
        Initialize Arctic DB Client
        
        Args:
            base_url: Base URL of Arctic DB API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.api_version = "v1"
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to API"""
        url = urljoin(f"{self.base_url}/api/{self.api_version}/", endpoint)
        response = requests.request(method, url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response
    
    def health_check(self) -> Dict:
        """Check API health status"""
        response = self._make_request('GET', '/health')
        return response.json()
    
    def write(self, table_name: str, data: Union[List[Dict], pd.DataFrame]) -> Dict:
        """
        Write data to Arctic DB
        
        Args:
            table_name: Name of table to write to
            data: Data as list of dicts or DataFrame
        
        Returns:
            Response dictionary with write status
        """
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        
        payload = {
            'table_name': table_name,
            'data': data
        }
        
        response = self._make_request('POST', 'write', json=payload)
        return response.json()
    
    def read(self, table_name: str) -> pd.DataFrame:
        """
        Read data from Arctic DB
        
        Args:
            table_name: Name of table to read from
        
        Returns:
            DataFrame with table data
        """
        response = self._make_request('GET', f'read/{table_name}')
        result = response.json()
        return pd.DataFrame(result['data'])
    
    def upload_to_s3(self, file_key: str, content: Union[Dict, str]) -> Dict:
        """
        Upload file to S3
        
        Args:
            file_key: S3 file key/path
            content: File content (dict or string)
        
        Returns:
            Response dictionary with upload status
        """
        payload = {
            'file_key': file_key,
            'content': content
        }
        
        response = self._make_request('POST', 's3/upload', json=payload)
        return response.json()
    
    def download_from_s3(self, file_key: str) -> Union[Dict, str]:
        """
        Download file from S3
        
        Args:
            file_key: S3 file key/path
        
        Returns:
            File content
        """
        response = self._make_request('GET', f's3/download/{file_key}')
        result = response.json()
        return result['content']
    
    def load_s3_to_db(self, file_key: str, table_name: str) -> Dict:
        """
        Load data from S3 into Arctic DB
        
        Args:
            file_key: S3 file key/path
            table_name: Target table name
        
        Returns:
            Response dictionary with load status
        """
        payload = {
            'file_key': file_key,
            'table_name': table_name
        }
        
        response = self._make_request('POST', 's3/load-to-db', json=payload)
        return response.json()
    
    def get_info(self) -> Dict:
        """Get system information and library list"""
        response = self._make_request('GET', 'info')
        return response.json()


if __name__ == '__main__':
    # Example usage
    client = ArcticDBClient()
    
    # Health check
    print("Health check:", client.health_check())
    
    # Get info
    print("System info:", client.get_info())
