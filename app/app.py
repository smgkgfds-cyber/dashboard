from http.server import BaseHTTPRequestHandler, HTTPServer


class PlatformHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Corporate Data Platform</title>
        </head>
        <body>
            <h1>Corporate Data Platform</h1>

            <h2>Корпоративная платформа обработки данных</h2>

            <p>Статус платформы: работает</p>
            <p>Версия приложения: 2.0</p>
            <p>Контейнеризация: Docker</p>

            <h3>Компоненты проекта</h3>

            <ul>
                <li>Docker</li>
                <li>Docker Compose</li>
                <li>Kubernetes</li>
                <li>Airflow</li>
                <li>MinIO</li>
                <li>DuckDB</li>
                <li>NetworkX</li>
                <li>Grafana</li>
            </ul>

            <p>Первый сервис платформы успешно запущен в Docker-контейнере.</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
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