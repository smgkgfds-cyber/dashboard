
from pathlib import Path

import duckdb
import networkx as nx


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "companies.csv"


def get_graph():
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Не найден файл: {DATA_FILE}")

    con = duckdb.connect()

    try:
        companies = con.execute(
            """
            SELECT id, name, industry, city, employees
            FROM read_csv_auto(?)
            """,
            [str(DATA_FILE)],
        ).fetchall()
    finally:
        con.close()

    G = nx.Graph()

    for company_id, name, industry, city, employees in companies:
        company_node = f"company:{company_id}"
        city_node = f"city:{city}"
        industry_node = f"industry:{industry}"

        G.add_node(
            company_node,
            node_type="company",
            label=name,
            employees=employees,
        )

        G.add_node(
            city_node,
            node_type="city",
            label=city,
        )

        G.add_node(
            industry_node,
            node_type="industry",
            label=industry,
        )

        G.add_edge(
            company_node,
            city_node,
            relation="located_in",
        )

        G.add_edge(
            company_node,
            industry_node,
            relation="operates_in",
        )

    return G


if __name__ == "__main__":
    G = get_graph()

    # Общая информация
    company_count = sum(
        1
        for _, data in G.nodes(data=True)
        if data["node_type"] == "company"
    )

    print("Количество организаций в CSV:", company_count)
    print("Количество вершин графа:", G.number_of_nodes())
    print("Количество ребер графа:", G.number_of_edges())

    # Вывод организаций
    print("\nОрганизации:")

    for _, data in G.nodes(data=True):
        if data["node_type"] == "company":
            print(
                data["label"],
                "-",
                data["employees"],
                "сотрудников",
            )

    # Вывод городов
    print("\nГорода:")

    for _, data in G.nodes(data=True):
        if data["node_type"] == "city":
            print(data["label"])

    # Вывод отраслей
    print("\nОтрасли:")

    for _, data in G.nodes(data=True):
        if data["node_type"] == "industry":
            print(data["label"])

    # Получение списка организаций
    company_nodes = [
        node
        for node, data in G.nodes(data=True)
        if data["node_type"] == "company"
    ]

    # Связи конкретной организации
    if company_nodes:
        selected_company = company_nodes[0]

        print("\nСвязи организации:")
        print(G.nodes[selected_company]["label"])

        for neighbor in G.neighbors(selected_company):
            print(
                "-",
                G.nodes[neighbor]["label"],
                "(",
                G.nodes[neighbor]["node_type"],
                ")",
            )

    # Организации по городам
    print("\nОрганизации по городам:")

    for node, data in G.nodes(data=True):
        if data["node_type"] == "city":
            companies_in_city = [
                G.nodes[neighbor]["label"]
                for neighbor in G.neighbors(node)
                if G.nodes[neighbor]["node_type"] == "company"
            ]

            print(data["label"], ":", ", ".join(companies_in_city))

    # Организации по отраслям
    print("\nОрганизации по отраслям:")

    for node, data in G.nodes(data=True):
        if data["node_type"] == "industry":
            organizations = [
                G.nodes[neighbor]["label"]
                for neighbor in G.neighbors(node)
                if G.nodes[neighbor]["node_type"] == "company"
            ]

            print(data["label"], ":", ", ".join(organizations))

    # Общие города и отрасли
    print("\nОбщие города и отрасли:")

    for i in range(len(company_nodes)):
        for j in range(i + 1, len(company_nodes)):
            first = company_nodes[i]
            second = company_nodes[j]

            common = set(G.neighbors(first)) & set(G.neighbors(second))

            if common:
                print(
                    G.nodes[first]["label"],
                    "<->",
                    G.nodes[second]["label"],
                )

                for node in common:
                    print(
                        "Общий объект:",
                        G.nodes[node]["label"],
                        "(",
                        G.nodes[node]["node_type"],
                        ")",
                    )

    # Степени вершин
    print("\nСтепени вершин:")

    for node, degree in G.degree():
        print(G.nodes[node]["label"], "-", degree)

    # Рейтинг наиболее связанных вершин
    ranking = sorted(
        G.degree(),
        key=lambda item: item[1],
        reverse=True,
    )

    print("\nНаиболее связанные вершины:")

    for node, degree in ranking[:5]:
        print(G.nodes[node]["label"], "-", degree)

    # Центральность по степени
    degree_centrality = nx.degree_centrality(G)

    print("\nЦентральность по степени:")

    for node, value in sorted(
        degree_centrality.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:5]:
        print(G.nodes[node]["label"], "-", round(value, 3))

    # Посредническая центральность
    betweenness = nx.betweenness_centrality(G)

    print("\nПосредническая центральность:")

    for node, value in sorted(
        betweenness.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:5]:
        print(G.nodes[node]["label"], "-", round(value, 3))

    # Компоненты связности
    components = list(nx.connected_components(G))

    print("\nКоличество компонент связности:")
    print(len(components))

    for index, component in enumerate(components, start=1):
        print(
            f"Компонента {index}:",
            len(component),
            "вершин",
        )

    # Кратчайший путь между организациями
    print("\nКратчайший путь:")

    path_found = False

    for i in range(len(company_nodes)):
        for j in range(i + 1, len(company_nodes)):
            source = company_nodes[i]
            target = company_nodes[j]

            if nx.has_path(G, source, target):
                path = nx.shortest_path(
                    G,
                    source=source,
                    target=target,
                )

                print(
                    G.nodes[source]["label"],
                    "->",
                    G.nodes[target]["label"],
                )

                for node in path:
                    print(G.nodes[node]["label"])

                path_found = True
                break

        if path_found:
            break

    if not path_found:
        print("Между выбранными организациями нет пути")

    # Самостоятельная аналитическая задача
    print("\nСамостоятельная аналитическая задача:")

    # Города по количеству организаций
    city_ranking = []

    for node, data in G.nodes(data=True):
        if data["node_type"] == "city":
            city_ranking.append((data["label"], G.degree(node)))

    city_ranking.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print("Города по количеству организаций:")

    for city, count in city_ranking:
        print(city, "-", count)

    # Отрасли по количеству организаций
    industry_ranking = []

    for node, data in G.nodes(data=True):
        if data["node_type"] == "industry":
            industry_ranking.append((data["label"], G.degree(node)))

    industry_ranking.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print("\nОтрасли по количеству организаций:")

    for industry, count in industry_ranking:
        print(industry, "-", count)

    # Максимальная посредническая центральность
    if betweenness:
        max_betweenness = max(betweenness.values())

        print("\nМаксимальная посредническая центральность:")

        for node, value in betweenness.items():
            if value == max_betweenness:
                print(
                    G.nodes[node]["label"],
                    "-",
                    round(value, 3),
                )