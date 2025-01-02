import uuid
import networkx as nx
import matplotlib.pyplot as plt
from colorama import Fore, init
import random
import os
import platform

# Ініціалізація Colorama для підтримки кольорів в консолі
init(autoreset=True)

# Очищення екрану консольного вікна
def clear_screen():
    system_name = platform.system()
    if system_name == "Windows":
        os.system('cls')  # Для Windows
    else:
        os.system('clear')  # Для Unix-подібних систем (Linux, macOS)

# Викликаємо очищення екрану при запуску скрипта
clear_screen()

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використання id та збереження значення вузла
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


def draw_heap(heap_root):
    tree = nx.DiGraph()
    pos = {heap_root.id: (0, 0)}
    tree = add_edges(tree, heap_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}  # Використовуйте значення вузла для міток

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


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


def print_heap_graphically(heap):
    """Псевдографічне відображення дерева купи на консолі"""
    print(Fore.GREEN + "Це програма для побудови та візуалізації бінарної купи.")
    print(Fore.YELLOW + "Використовуються алгоритми для побудови бінарної купи та виведення дерева.")
    print(Fore.CYAN + "Програма побудує дерево із масиву, який представляє бінарну купу.")
    print(Fore.MAGENTA + "Використовується максимальна бінарна купа, де кожен батьківський елемент більший за дітей.\n")

    print(Fore.WHITE + "Псевдографічне відображення дерева купи:")
    print(Fore.BLUE + f"Дерево на основі масиву: {heap}")
    
    # Псевдографіка для виведення дерева
    def print_tree(node, prefix="", is_left=True):
        if node is not None:
            print(prefix, "`- " if is_left else "+- ", node.val, sep="")
            print_tree(node.left, prefix + ("|   " if is_left else "    "), True)
            print_tree(node.right, prefix + ("|   " if is_left else "    "), False)
    
    print_tree(build_heap_tree(heap))


# Діалог з користувачем
print(Fore.GREEN + "Ласкаво просимо до програми побудови бінарної купи!")
print(Fore.CYAN + "Ця програма дозволяє побудувати дерево на основі бінарної купи та візуалізувати його.")

# Функція для перевірки введення користувача
def get_valid_input():
    while True:
        heap_input = input(Fore.YELLOW + "Введіть елементи для побудови бінарної купи (через пробіл) або нажміть Enter для генерації випадкових даних: ")

        if heap_input.strip() == "":
            # Генерація випадкових даних, якщо користувач не ввів значення
            heap = [random.randint(1, 100) for _ in range(7)]  # Генерація 7 випадкових чисел
            print(Fore.CYAN + f"Генеровано випадкові дані для купи: {heap}")
            return heap

        # Перевірка введення, чи є це коректними цілими числами
        try:
            heap = list(map(int, heap_input.split()))
            
            # Перевірка на від'ємні значення
            if any(x < 0 for x in heap):
                print(Fore.RED + "Помилка! Введені значення не можуть бути від'ємними.")
                continue
            
            # Перевірка на недостатньо елементів для побудови дерева
            if len(heap) < 2:
                print(Fore.RED + "Помилка! Для побудови дерева необхідно ввести більше одного елемента.")
                continue
            
            return heap

        except ValueError:
            print(Fore.RED + "Помилка! Введіть лише числа, розділені пробілами.")
        except Exception as e:
            print(Fore.RED + f"Сталася непередбачувана помилка: {e}")
            continue

# Отримання правильного вводу
heap = get_valid_input()

# Створення дерева з масиву купи
heap_tree = build_heap_tree(heap)

# Виведення дерева з псевдографікою та візуалізацією
print_heap_graphically(heap)

# Візуалізація дерева за допомогою matplotlib
draw_heap(heap_tree)
