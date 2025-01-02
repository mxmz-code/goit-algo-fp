import os
import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt
from colorama import init, Fore, Back, Style
from time import time_ns
import numpy as np

# Инициализация colorama
init(autoreset=True)

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Кількість вершин
        self.graph = {i: [] for i in range(vertices)}  # Список суміжності

    def add_edge(self, u, v, weight):
        # Додаємо ребра в граф
        if u >= self.V or v >= self.V:
            raise ValueError("Вершини повинні бути в межах кількості вершин")
        if weight < 0:
            raise ValueError("Вага ребра не може бути від'ємною для алгоритму Дейкстри")
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # Для неорієнтованого графа

def dijkstra(graph, start):
    distances = {vertex: float('inf') for vertex in range(graph.V)}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in range(graph.V)}  # Словник для відстеження шляху
    pq = [(0, start)]  # Черга пріоритетів (мінімальна купа)

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph.graph[current_vertex]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_vertices

def reconstruct_path(previous_vertices, start, end):
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path.reverse()
    return path if path[0] == start else []

def generate_random_graph(vertices, edge_probability=0.8, max_weight=10):
    # Генерація випадкового графа з вершинами та ребрами
    graph = Graph(vertices)
    for u in range(vertices):
        for v in range(u + 1, vertices):
            if random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                graph.add_edge(u, v, weight)
    return graph

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def visualize_graph(graph, start, end, previous_vertices):
    G = nx.Graph()
    for u in graph.graph:
        for v, weight in graph.graph[u]:
            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    
    # Створення графічної візуалізації з жовто-синіми полукругами
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Позиції для вершин
    pos = nx.spring_layout(G)
    for i, (x, y) in pos.items():
        # Малюємо верхню синю частину (полукруг)
        theta = np.linspace(0, np.pi, 100)
        x_vals_upper = x + 0.1 * np.cos(theta)
        y_vals_upper = y + 0.1 * np.sin(theta)
        ax.fill(x_vals_upper, y_vals_upper, color='skyblue')

        # Малюємо нижню жовту частину (полукруг)
        theta = np.linspace(np.pi, 2*np.pi, 100)
        x_vals_lower = x + 0.1 * np.cos(theta)
        y_vals_lower = y + 0.1 * np.sin(theta)
        ax.fill(x_vals_lower, y_vals_lower, color='yellow')

    nx.draw_networkx_labels(G, pos, font_size=15, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(G, pos, width=2.0, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

    # Відображення ребер на шляху
    path = reconstruct_path(previous_vertices, start, end)
    edges_to_highlight = set()
    for i in range(len(path) - 1):
        edges_to_highlight.add((path[i], path[i + 1]))
    
    for u, v in G.edges():
        if (u, v) in edges_to_highlight or (v, u) in edges_to_highlight:
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=3.0, edge_color='red', ax=ax)

    plt.axis('off')
    plt.show()

def print_intro():
    print(Fore.YELLOW + Style.BRIGHT + "Програма для знаходження найкоротших шляхів в графі з використанням алгоритму Дейкстри.")
    print(Fore.CYAN + "Цей алгоритм знаходить мінімальні відстані від початкової вершини до всіх інших вершин в графі.")
    print(Fore.CYAN + "Використовується черга з пріоритетами для оптимізації пошуку мінімальних відстаней.")
    print(Fore.GREEN + "Граф створюється випадковим чином, кожна вершина може бути з'єднана з іншими з певною ймовірністю.")
    print(Fore.RED + "У разі від'ємних ваг ребер алгоритм не працюватиме коректно.")
    print(Style.RESET_ALL)

def print_results(distances, previous_vertices, start, end):
    print(Fore.YELLOW + f"\nНайкоротші шляхи від вершини {start}:")
    for vertex, distance in distances.items():
        if distance == float('inf'):
            print(Fore.RED + f"Вершина {vertex}: недоступна")
        else:
            print(Fore.GREEN + f"Вершина {vertex}: {distance}")
    
    path = reconstruct_path(previous_vertices, start, end)
    if path:
        print(Fore.BLUE + f"Шлях від вершини {start} до вершини {end}: {' -> '.join(map(str, path))}")
    else:
        print(Fore.RED + f"Немає шляху від вершини {start} до вершини {end}")

def print_pseudographics():
    print(Fore.MAGENTA + Style.BRIGHT + "+" + "-" * 40 + "+")
    print(Fore.MAGENTA + "| Програма для знаходження найкоротших шляхів в графі |")
    print(Fore.MAGENTA + "+" + "-" * 40 + "+")
    print(Fore.GREEN + "| Стартова вершина: " + "Випадкова " + "|")
    print(Fore.GREEN + "| Кінцева вершина: " + "Випадкова " + "|")
    print(Fore.MAGENTA + "+" + "-" * 40 + "+")

def main():
    clear_screen()
    print_intro()
    
    # Генерація випадкового графа
    vertices = random.randint(5, 10)  # Генеруємо кількість вершин від 5 до 10
    g = generate_random_graph(vertices, edge_probability=0.8)  # Збільшуємо ймовірність рёбер
    
    start_vertex = random.randint(0, vertices - 1)
    end_vertex = random.randint(0, vertices - 1)
    
    # Початок вимірювання часу (наносекунди)
    total_time_ns = 0
    num_runs = 1000  # Виконуємо 1000 прогонів для усереднення
    
    for _ in range(num_runs):
        start_time = time_ns()
        distances, previous_vertices = dijkstra(g, start_vertex)
        end_time = time_ns()
        total_time_ns += (end_time - start_time)
    
    # Усереднюємо час
    average_time_ns = total_time_ns / num_runs
    average_time_ms = average_time_ns / 1_000_000  # Перетворюємо в мілісекунди
    
    print_results(distances, previous_vertices, start_vertex, end_vertex)
    
    # Візуалізація графа з виділенням найкоротших шляхів
    visualize_graph(g, start_vertex, end_vertex, previous_vertices)
    
    # Виведення псевдографіки
    print_pseudographics()
    
    # Виведення часу виконання алгоритму в мілісекундах
    print(Fore.CYAN + f"Середній час виконання алгоритму за {num_runs} запусків: {average_time_ms:.3f} мілісекунд.")

if __name__ == "__main__":
    main()
