import os
import sys
from unittest.mock import MagicMock, patch

# Ensure repository root is on path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Stub external dependencies before importing the pipeline
sys.modules['boto3'] = MagicMock()
sys.modules['requests'] = MagicMock()

import pp_data_extract_shpy as pipeline


def mock_requests_get(url, auth):
    response = MagicMock()
    response.json.return_value = {"url": url}
    response.raise_for_status.return_value = None
    return response


def test_run_store_uploads_all_endpoints():
    store = {
        "name": "test",
        "domain": "test.myshopify.com",
        "api_key": "key",
        "password": "pwd",
        "s3_bucket": "bucket",
    }
    fake_s3 = MagicMock()
    with patch("pp_data_extract_shpy.requests.get", side_effect=mock_requests_get) as mock_get:
        pipeline.run_store(store, s3_client=fake_s3)
    assert mock_get.call_count == len(pipeline.ENDPOINTS)
    assert fake_s3.put_object.call_count == len(pipeline.ENDPOINTS)


def test_run_pipeline_multiple_stores():
    config = {
        "stores": [
            {
                "name": "s1",
                "domain": "s1.myshopify.com",
                "api_key": "a",
                "password": "p",
                "s3_bucket": "b",
            },
            {
                "name": "s2",
                "domain": "s2.myshopify.com",
                "api_key": "a2",
                "password": "p2",
                "s3_bucket": "b",
            },
        ]
    }
    with patch("pp_data_extract_shpy.run_store") as mock_run_store:
        pipeline.run_pipeline(config)
    assert mock_run_store.call_count == len(config["stores"])
