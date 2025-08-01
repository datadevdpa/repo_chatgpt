import json
import os
from datetime import datetime
from typing import Dict, Any, List

import boto3
import requests


ENDPOINTS = ["orders", "customers", "checkouts"]

def fetch_endpoint(store: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
    """Fetch a single endpoint from Shopify for the given store."""
    api_version = store.get("api_version", "2023-07")
    url = f"https://{store['domain']}/admin/api/{api_version}/{endpoint}.json"
    auth = (store["api_key"], store["password"])
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def upload_json_to_s3(data: Dict[str, Any], bucket: str, key: str, s3_client=None) -> None:
    """Upload a JSON-serialisable object to S3."""
    if s3_client is None:
        s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(data))

def run_store(store: Dict[str, Any], s3_client=None) -> Dict[str, Dict[str, Any]]:
    """Fetch all endpoints for a store and upload them to S3."""
    if s3_client is None:
        s3_client = boto3.client("s3")
    results: Dict[str, Dict[str, Any]] = {}
    for endpoint in ENDPOINTS:
        data = fetch_endpoint(store, endpoint)
        results[endpoint] = data
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        key = f"{store['name']}/{endpoint}_{timestamp}.json"
        upload_json_to_s3(data, store["s3_bucket"], key, s3_client=s3_client)
    return results

def run_pipeline(config: Dict[str, Any]) -> None:
    """Run extraction for all stores defined in config."""
    s3_client = boto3.client("s3")
    for store in config.get("stores", []):
        run_store(store, s3_client=s3_client)

def load_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    config_path = os.environ.get("SHOPIFY_STORES_CONFIG", "config.json")
    configuration = load_config(config_path)
    run_pipeline(configuration)
