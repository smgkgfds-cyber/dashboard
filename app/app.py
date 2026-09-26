import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg


DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "corporate")
DB_USER = os.getenv("DB_USER", "corporate_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "corporate_password")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_companies():
    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, industry, city, employees
                FROM companies
                ORDER BY id
                """
            )

            return cursor.fetchall()


class PlatformHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            companies = get_companies()

            rows = ""

            for company in companies:
                rows += f"""
                <tr>
                    <td>{company[0]}</td>
                    <td>{company[1]}</td>
                    <td>{company[2]}</td>
                    <td>{company[3]}</td>
                    <td>{company[4]}</td>
                </tr>
                """

            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Corporate Data Platform</title>
            </head>
            <body>
                <h1>Corporate Data Platform</h1>

                <h2>Корпоративная платформа обработки данных</h2>

                <p>Статус приложения: работает</p>

                <p>Версия приложения: 2.0</p>

                <p>Контейнеризация: Docker</p>

                <p>Источник данных: PostgreSQL</p>

                <h3>Организации</h3>

                <table border="1">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Организация</th>
                            <th>Отрасль</th>
                            <th>Город</th>
                            <th>Сотрудников</th>
                        </tr>
                    </thead>

                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header(
                "Content-type",
                "text/html; charset=utf-8",
            )
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

        except Exception as error:
            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Ошибка</title>
            </head>
            <body>
                <h1>Corporate Data Platform</h1>

                <h2>Ошибка подключения к базе данных</h2>

                <p>{error}</p>
            </body>
            </html>
            """

            self.send_response(500)
            self.send_header(
                "Content-type",
                "text/html; charset=utf-8",
            )
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))


server = HTTPServer(("0.0.0.0", 8000), PlatformHandler)

try:
    print(
        "Corporate Data Platform is running on port 8000",
        flush=True,
    )

    server.serve_forever()

except KeyboardInterrupt:
    print("\nServer stopped")
    server.server_close()