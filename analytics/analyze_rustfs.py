
import duckdb
import os
from getpass import getpass

access_key = os.getenv("RUSTFS_ACCESS_KEY")
secret_key = os.getenv("RUSTFS_SECRET_KEY")

if not access_key:
    access_key = input("RustFS Access Key: ")

if not secret_key:
    secret_key = getpass("RustFS Secret Key: ")

con = duckdb.connect()

con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

def sql_string(value):
    return "'" + value.replace("'", "''") + "'"

con.execute(f"""
    CREATE OR REPLACE SECRET rustfs_secret (
        TYPE s3,
        KEY_ID {sql_string(access_key)},
        SECRET {sql_string(secret_key)},
        REGION 'us-east-1',
        ENDPOINT 'localhost:9000',
        URL_STYLE 'path',
        USE_SSL false
    )
""")

print("Подключение к RustFS настроено")

query = """
    SELECT *
    FROM read_csv_auto(
        's3://corporate-raw/companies.csv'
    )
"""

result = con.execute(query).fetchdf()

print("\nДанные из RAW:")
print(result.to_string(index=False))

query = """
    SELECT
        city,
        COUNT(*) AS company_count,
        SUM(employees) AS total_employees
    FROM read_csv_auto(
        's3://corporate-raw/companies.csv'
    )
    GROUP BY city
    ORDER BY total_employees DESC
"""

result = con.execute(query).fetchdf()

print("\nАнализ RAW по городам:")
print(result.to_string(index=False))


query = """
    SELECT *
    FROM read_csv_auto(
        's3://corporate-processed/reports/companies_by_city.csv'
    )
"""

result = con.execute(query).fetchdf()

print("\nДанные из PROCESSED:")
print(result.to_string(index=False))


raw_structure = con.execute("""
    DESCRIBE SELECT *
    FROM read_csv_auto(
        's3://corporate-raw/companies.csv'
    )
""").fetchdf()

print("\nСтруктура RAW:")
print(raw_structure.to_string(index=False))


processed_structure = con.execute("""
    DESCRIBE SELECT *
    FROM read_csv_auto(
        's3://corporate-processed/reports/companies_by_city.csv'
    )
""").fetchdf()

print("\nСтруктура PROCESSED:")
print(processed_structure.to_string(index=False))


con.close()
