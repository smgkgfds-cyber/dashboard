
import os
from getpass import getpass
from pathlib import Path

import boto3
import duckdb
from botocore.config import Config

access_key = os.getenv("RUSTFS_ACCESS_KEY")
secret_key = os.getenv("RUSTFS_SECRET_KEY")

if not access_key:
    access_key = input("RustFS Access Key: ")

if not secret_key:
    secret_key = getpass("RustFS Secret Key: ")

client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name="us-east-1",
    config=Config(
        s3={"addressing_style": "path"}
    ),
)

output = Path("data/processed/companies_by_city.csv")
output.parent.mkdir(parents=True, exist_ok=True)

client.download_file(
    "corporate-processed",
    "reports/companies_by_city.csv",
    str(output)
)

print(f"Файл скачан: {output}")

con = duckdb.connect()

result = con.execute("""
    SELECT *
    FROM read_csv_auto('data/processed/companies_by_city.csv')
""").fetchdf()

print("\nДанные из PROCESSED:")
print(result.to_string(index=False))

con.close()
