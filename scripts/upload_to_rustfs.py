
from pathlib import Path

import boto3
from botocore.config import Config


file_path = Path("airflow/output/companies_by_city.csv")

if not file_path.is_file():
    raise FileNotFoundError(
        f"Файл не найден: {file_path}. "
        "Сначала выполните DAG из работы № 9."
    )

client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfssecret123",
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)

bucket_name = "corporate-processed"
object_name = "reports/companies_by_city.csv"

client.upload_file(
    str(file_path),
    bucket_name,
    object_name,
    ExtraArgs={"ContentType": "text/csv"},
)

print(f"Загружено: {bucket_name}/{object_name}")
