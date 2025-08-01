# Shopify Data Extraction Pipeline

This repository contains a simple pipeline script, `pp_data_extract_shpy`, that
extracts data from Shopify stores and uploads it to Amazon S3. The script is
configured to handle multiple stores and fetches the `orders`, `customers`, and
`checkouts` endpoints for each store.

## Setup

1. Create and activate a Python 3 virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a configuration file based on `config_template.json` and set the
   environment variable `SHOPIFY_STORES_CONFIG` to its path.

## Running

Execute the pipeline:

```bash
python pp_data_extract_shpy.py
```

The script will read store credentials from the configuration file and upload
JSON results for each endpoint to the configured S3 bucket.

## Testing

Run unit tests with:

```bash
pytest
```

