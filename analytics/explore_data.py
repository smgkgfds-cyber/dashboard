
import duckdb

con = duckdb.connect()

query = """
    SELECT
    name,
    industry,
    employees
FROM read_csv_auto('data/raw/companies.csv')
WHERE employees >= 150
ORDER BY employees DESC
LIMIT 3;
"""

result = con.execute(query).fetchdf()

print("Все организации:")
print(result.to_string(index=False))

con.close()
