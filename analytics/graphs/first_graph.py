
import networkx as nx


G = nx.Graph()

# Создание вершин
G.add_node("Company A")
G.add_node("Company B")
G.add_node("Tallinn")
G.add_node("Riga")

# Создание связей
G.add_edge("Company A", "Tallinn")
G.add_edge("Company B", "Riga")
G.add_edge("Company A", "Company B")

# Количество вершин и ребер
print("Количество вершин:", G.number_of_nodes())
print("Количество ребер:", G.number_of_edges())

# Вывод вершин
print("\nВершины:")
print(list(G.nodes()))

# Вывод ребер
print("\nРебра:")
print(list(G.edges()))
