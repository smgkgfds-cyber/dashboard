
# Аналитический модуль Corporate Data Platform

## Назначение

Аналитическая обработка корпоративных данных с использованием DuckDB.

## Источники данных

- PostgreSQL: операционные данные организаций.
- RustFS: S3-совместимое объектное хранилище.
- RAW: corporate-raw/companies.csv
- PROCESSED: corporate-processed/reports/companies_by_city.csv

## Аналитический инструмент

DuckDB.

## Основные операции

- Чтение CSV-файлов.
- Выполнение SQL-запросов.
- Фильтрация и сортировка данных.
- Группировка организаций.
- Расчет агрегированных показателей.
- Формирование аналитических отчетов.

## Результаты

- analytics/reports/city_analytics.csv
- analytics/reports/conclusions.md

## Архитектура

PostgreSQL → Apache Airflow → RustFS Data Lake → DuckDB → Аналитический отчет
