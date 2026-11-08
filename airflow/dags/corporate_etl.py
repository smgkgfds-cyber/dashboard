
import csv
import os

import boto3
import psycopg

from datetime import datetime
from airflow.sdk import dag, task
from botocore.config import Config


@dag(
    dag_id="corporate_etl",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["corporate-data", "etl"],
)
def corporate_etl():

    # EXTRACT
    @task
    def extract_companies():
        connection = psycopg.connect(
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "corporate"),
            user=os.getenv("DB_USER", "corporate_user"),
            password=os.getenv("DB_PASSWORD", "corporate_password"),
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, name, industry, city, employees
                    FROM companies
                    ORDER BY id
                """)

                rows = cursor.fetchall()

                companies = []

                for row in rows:
                    companies.append({
                        "id": row[0],
                        "name": row[1],
                        "industry": row[2],
                        "city": row[3],
                        "employees": row[4],
                    })

                print(f"Extracted companies: {len(companies)}")

                return companies

        finally:
            connection.close()

    # TRANSFORM
    @task
    def transform_companies(companies):
        cities = {}

        for company in companies:
            city = company["city"]
            employees = company["employees"]

            if city not in cities:
                cities[city] = {
                    "city": city,
                    "company_count": 0,
                    "total_employees": 0,
                }

            cities[city]["company_count"] += 1
            cities[city]["total_employees"] += employees

        result = []

        for city_data in cities.values():
            average = (
                city_data["total_employees"]
                / city_data["company_count"]
            )

            result.append({
                "city": city_data["city"],
                "company_count": city_data["company_count"],
                "total_employees": city_data["total_employees"],
                "average_employees": round(average, 2),
            })

        result.sort(key=lambda item: item["city"])

        print(f"Transformed cities: {len(result)}")

        return result

    # LOAD
    @task
    def load_report(data):
        output_file = "/opt/airflow/output/companies_by_city.csv"

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "city",
                    "company_count",
                    "total_employees",
                    "average_employees",
                ],
            )

            writer.writeheader()
            writer.writerows(data)

        print(f"Report saved to {output_file}")
        print(f"Rows written: {len(data)}")

        return output_file

    # UPLOAD TO RUSTFS
    @task
    def upload_to_rustfs(file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Не найден файл отчета: {file_path}"
            )

        client = boto3.client(
            "s3",
            endpoint_url=os.getenv(
                "RUSTFS_ENDPOINT",
                "http://rustfs:9000",
            ),
            aws_access_key_id=os.getenv(
                "RUSTFS_ACCESS_KEY",
                "rustfsadmin",
            ),
            aws_secret_access_key=os.getenv(
                "RUSTFS_SECRET_KEY",
                "rustfssecret123",
            ),
            region_name="us-east-1",
            config=Config(
                s3={"addressing_style": "path"},
            ),
        )

        bucket = os.getenv(
            "RUSTFS_PROCESSED_BUCKET",
            "corporate-processed",
        )

        key = "reports/companies_by_city.csv"

        client.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs={"ContentType": "text/csv"},
        )

        print(f"Загружено: {bucket}/{key}")

    # TASK DEPENDENCIES
    extracted_data = extract_companies()
    transformed_data = transform_companies(extracted_data)
    report_file = load_report(transformed_data)
    upload_to_rustfs(report_file)


corporate_etl()
