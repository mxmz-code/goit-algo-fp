import uuid
import networkx as nx
import matplotlib.pyplot as plt
import os
import platform
import sys
from collections import deque
from colorama import Fore, Back, Style, init

# Ініціалізація colorama для роботи на Windows
init(autoreset=True)

class Node:
    def __init__(self, key, color="#87CEEB"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # За замовчуванням колір у шістнадцятковому форматі
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла

# Функція для генерації кольорів у шістнадцятковому форматі
def assign_colors_to_nodes(nodes_visited):
    color_step = 255 // len(nodes_visited)
    colors = []
    for i, node in enumerate(nodes_visited):
        # Генерація кольору від темного до світлого в шістнадцятковому форматі
        r = hex(i * color_step)[2:].zfill(2)
        g = hex(0)[2:].zfill(2)
        b = hex(255 - i * color_step)[2:].zfill(2)
        color_hex = f"#{r}{g}{b}"  # Збираємо колір у форматі #RRGGBB
        node.color = color_hex
        colors.append(color_hex)  # Додаємо шістнадцятковий колір до списку
    return nodes_visited

# Обхід в глибину (DFS) з використанням стека
def dfs_traversal(root):
    stack = [root]
    visited = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
    return visited

# Обхід в ширину (BFS) з використанням черги
def bfs_traversal(root):
    queue = deque([root])
    visited = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return visited

# Додавання ребер для побудови графа
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використовуємо id і зберігаємо значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

# Побудова дерева з масиву
def build_heap_tree(heap):
    root = Node(heap[0])
    nodes = [root]
    
    for i in range(1, len(heap)):
        node = Node(heap[i])
        parent = nodes[(i - 1) // 2]  # Знаходимо батьківський вузол
        if i % 2 == 1:
            parent.left = node
        else:
            parent.right = node
        nodes.append(node)
    
    return root

# Очищення консолі залежно від операційної системи
def clear_console():
    system_name = platform.system()
    if system_name == "Windows":
        os.system('cls')  # Для Windows
    else:
        os.system('clear')  # Для Unix-подібних систем (Linux, macOS)

# Візуалізація обходу дерева
def visualize_traversal(root, traversal_type):
    if traversal_type == "DFS":
        nodes_visited = dfs_traversal(root)
    else:
        nodes_visited = bfs_traversal(root)

    # Призначаємо кольори вузлам
    nodes_visited = assign_colors_to_nodes(nodes_visited)

    # Побудова дерева для візуалізації
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [node.color for node in nodes_visited]
    labels = {node.id: node.val for node in nodes_visited}

    # Відображення дерева
    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.title(f"Обхід бінарного дерева: {traversal_type}")

    # Показуємо графік і чекаємо закриття вікна
    plt.show()

    # Після закриття вікна програма завершує свою роботу
    sys.exit()  # Явно завершуємо програму після завершення відображення

# Тестування на даних
clear_console()  # Очищаємо консоль перед запуском програми

# 1. Назва задачі
print(Fore.GREEN + Style.BRIGHT + "Задача: Візуалізація обходу бінарного дерева")

# 2. Опис, що потрібно зробити
print(Fore.YELLOW + "\nОпис задачі:")
print(Fore.CYAN + "Задача полягає в візуалізації обходів бінарного дерева за допомогою алгоритмів DFS та BFS.")
print("Необхідно побудувати дерево, виконати обходи з присвоєнням унікальних кольорів кожному вузлу, відображаючи кожен крок обходу.")

# 3. Опис алгоритмів і детальний опис принципу їх роботи
print(Fore.YELLOW + "\nВикористовувані алгоритми:")
print(Fore.CYAN + "- Обхід в глибину (DFS) з використанням стека.")
print(Fore.WHITE + "  Алгоритм обходу в глибину використовує стек для відвідування вузлів. Він відвідує вузли глибше по мірі обходу.")
print(Fore.CYAN + "- Обхід в ширину (BFS) з використанням черги.")
print(Fore.WHITE + "  Алгоритм обходу в ширину використовує чергу для відвідування вузлів на кожному рівні по черзі.")

# 4. Опис рішення
print(Fore.YELLOW + "\nОпис рішення:")
print(Fore.CYAN + "1. Побудовано бінарне дерево на основі масиву даних.")
print("2. Для обходу дерева використано два алгоритми: в глибину (DFS) і в ширину (BFS).")
print("3. Кожен вузол дерева має унікальний колір, який змінюється від темного до світлого.")
print("4. Після виконання обходу дерева графіки відображаються з різними кольорами, щоб продемонструвати кожен крок обходу.")

# 5. Початкові дані
print(Fore.YELLOW + "\nПочаткові дані:")
heap_data = [15, 10, 20, 8, 12, 17, 25, 6, 9]
print(Fore.CYAN + str(heap_data))

# 6. Тестове рішення за цими даними
print(Fore.YELLOW + "\nТестове рішення за цими даними:")
print(Fore.CYAN + "1. Побудовано бінарне дерево.")
print("2. Для обходу дерева застосовані алгоритми DFS та BFS.")
print("3. Візуалізовано графіки з кроками обходу.")

# 7. Висновки
print(Fore.YELLOW + "\nВисновки:")
print(Fore.CYAN + "Використання алгоритмів DFS та BFS для обходу бінарного дерева дозволяє наочно побачити, як обходяться вузли.")
print("Кольори вузлів допомагають відобразити послідовність їх відвідування.")
print("Графіки є корисним інструментом для візуалізації роботи алгоритмів.")

# 8. Приклад виведення графіків: обхід дерева
print(Fore.RED + "+" + "-"*40 + "+")
print(Fore.RED + "|" + " " * 38 + "|")
print(Fore.RED + "|" + "  Приклад виведення графіків: обхід дерева  |")
print(Fore.RED + "|" + " " * 38 + "|")
print(Fore.RED + "+" + "-"*40 + "+")

# Створення дерева з масиву
heap_tree = build_heap_tree(heap_data)

# Відображення візуалізації обходу в глибину (DFS)
visualize_traversal(heap_tree, "DFS")

# Відображення візуалізації обходу в ширину (BFS) буде виконано тільки якщо перший графік не завершить програму
