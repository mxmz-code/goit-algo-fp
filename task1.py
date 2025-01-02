import random
import logging
from colorama import Fore, Style, init
import os
import time

# Ініціалізація colorama
init(autoreset=True)

# Налаштування логування
logging.basicConfig(filename='task1.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Очищення екрану перед запуском
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Клас для вузла списку
class Node:
    def __init__(self, data):
        self.data = data  # дані вузла
        self.next = None  # посилання на наступний вузол

# Клас для односпрямованого списку
class LinkedList:
    def __init__(self):
        self.head = None  # початок списку

    # Функція для додавання елемента в кінець списку
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Функція для реверсування списку
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next  # зберігаємо наступний елемент
            current.next = prev  # змінюємо посилання на попередній елемент
            prev = current  # рухаємо prev і current вперед
            current = next_node
        self.head = prev  # новий початок списку

    # Алгоритм сортування злиттям
    def merge_sort(self, head):
        if not head or not head.next:
            return head
        middle = self.get_middle(head)
        left_half = self.split_list(head, middle)
        right_half = left_half.next
        left_half.next = None
        left_half = self.merge_sort(left_half)
        right_half = self.merge_sort(right_half)
        return self.merge_sorted(left_half, right_half)

    # Допоміжні функції для злиття
    def get_middle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def split_list(self, head, middle):
        left_half = head
        right_half = middle.next
        return left_half

    def merge_sorted(self, left, right):
        if not left:
            return right
        if not right:
            return left
        if left.data <= right.data:
            left.next = self.merge_sorted(left.next, right)
            return left
        else:
            right.next = self.merge_sorted(left, right.next)
            return right

    # Алгоритм сортування вставками
    def insertion_sort(self):
        if self.head is None:
            return
        
        sorted_list = None
        current = self.head
        while current:
            next_node = current.next
            sorted_list = self.sorted_insert(sorted_list, current)
            current = next_node
        self.head = sorted_list

    # Допоміжна функція для вставки елемента в відсортований список
    def sorted_insert(self, sorted_list, new_node):
        if sorted_list is None or sorted_list.data >= new_node.data:
            new_node.next = sorted_list
            sorted_list = new_node
        else:
            current = sorted_list
            while current.next and current.next.data < new_node.data:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        return sorted_list

    # Функція для видалення елемента за значенням
    def remove(self, value):
        current = self.head
        previous = None
        while current:
            if current.data == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    # Функція для пошуку елемента
    def search(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    # Функція для знаходження середнього значення
    def find_average(self):
        total = 0
        count = 0
        current = self.head
        while current:
            total += current.data
            count += 1
            current = current.next
        return total / count if count > 0 else None

    # Функція для виведення списку
    def print_list(self):
        current = self.head
        if not current:
            print(Fore.RED + "Список порожній.")
            return
        print(Fore.GREEN + "Список:")
        print(Fore.CYAN + "+---------+")
        print(Fore.CYAN + "| Значення |")
        print(Fore.CYAN + "+---------+")
        while current:
            print(Fore.YELLOW + f"| {current.data}       |")
            current = current.next
        print(Fore.CYAN + "+---------+")

    # Функція для генерації випадкового списку з заданою кількістю елементів
    def generate_random_list(self, size, min_value=0, max_value=100):
        for _ in range(size):
            self.append(random.randint(min_value, max_value))

    # Метод для об'єднання двох відсортованих списків
    def merge_sorted_lists(self, head1, head2):
        if not head1:
            return head2
        if not head2:
            return head1

        if head1.data <= head2.data:
            merged_head = head1
            merged_head.next = self.merge_sorted_lists(head1.next, head2)
        else:
            merged_head = head2
            merged_head.next = self.merge_sorted_lists(head1, head2.next)

        return merged_head

# Очищення екрану перед запуском
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Функція для меню
def menu():
    # Очищаємо екран перед запуском меню
    clear_screen()

    # Генерація випадкових даних на початку
    linked_list = LinkedList()
    size = random.randint(5, 10)  # Генерація випадкової кількості елементів від 5 до 10
    linked_list.generate_random_list(size)
    logging.info(f"Сгенеровано {size} випадкових елементів.")
    print(Fore.GREEN + f"Сгенеровано {size} випадкових елементів.")
    time.sleep(1)

    while True:
        print(Fore.CYAN + "\nМеню:")
        print(Fore.MAGENTA + "1. Додати елемент в список")
        print(Fore.MAGENTA + "2. Видалити елемент за значенням")
        print(Fore.MAGENTA + "3. Реверсувати список")
        print(Fore.MAGENTA + "4. Сортувати список (вставками)")
        print(Fore.MAGENTA + "5. Сортувати список (злиттям)")
        print(Fore.MAGENTA + "6. Знайти середнє значення елементів")
        print(Fore.MAGENTA + "7. Об'єднати два списки")
        print(Fore.MAGENTA + "8. Вивести список")
        print(Fore.MAGENTA + "9. Генерація випадкових даних")
        print(Fore.MAGENTA + "0. Вийти")

        choice = input(Fore.YELLOW + "Виберіть дію (0-9): ")

        if choice == '1':
            values = input(Fore.YELLOW + "Введіть значення для додавання через пробіл (наприклад, 1 2 4): ")
            values = values.split()  # Розділяємо введену строку по пробілах
            for value in values:
                try:
                    linked_list.append(int(value))  # Додаємо значення в список
                    logging.info(f"Додано значення {value}.")
                    print(Fore.GREEN + f"Значення {value} додано в список.")
                except ValueError:
                    print(Fore.RED + f"Помилка: '{value}' не є числом.")
                    logging.error(f"Не вдалося додати значення: '{value}' не є числом.")
        elif choice == '2':
            try:
                value = int(input(Fore.YELLOW + "Введіть значення для видалення: "))
                if linked_list.remove(value):
                    logging.info(f"Елемент {value} видалено.")
                    print(Fore.GREEN + f"Елемент {value} видалено.")
                else:
                    print(Fore.RED + "Елемент не знайдено.")
            except ValueError:
                print(Fore.RED + "Будь ласка, введіть правильне число.")
        elif choice == '3':
            # Виводимо початковий список
            print(Fore.CYAN + "Початковий список:")
            linked_list.print_list()
            
            # Реверсуємо список
            linked_list.reverse()
            logging.info("Список реверсовано.")
            
            # Виводимо реверсований список
            print(Fore.GREEN + "Список реверсовано.")
            linked_list.print_list()  # Виводимо оновлений список
        elif choice == '4':
            # Виводимо початковий список
            print(Fore.CYAN + "Початковий список перед сортуванням (вставками):")
            linked_list.print_list()
            
            # Сортуємо список вставками
            linked_list.insertion_sort()
            logging.info("Список відсортовано вставками.")
            
            # Виводимо відсортований список
            print(Fore.GREEN + "Список відсортовано вставками.")
            linked_list.print_list()  # Виводимо результат сортування
        elif choice == '5':
            # Виводимо початковий список
            print(Fore.CYAN + "Початковий список перед сортуванням (злиттям):")
            linked_list.print_list()
            
            # Сортуємо список злиттям
            linked_list.head = linked_list.merge_sort(linked_list.head)
            logging.info("Список відсортовано злиттям.")
            
            # Виводимо відсортований список
            print(Fore.GREEN + "Список відсортовано злиттям.")
            linked_list.print_list()  # Виводимо результат сортування
        elif choice == '6':
            average = linked_list.find_average()
            if average is not None:
                logging.info(f"Середнє значення елементів: {average}")
                print(Fore.GREEN + f"Середнє значення елементів: {average}")
            else:
                print(Fore.RED + "Список порожній, неможливо обчислити середнє.")
        elif choice == '7':
            # Генерація другого списку випадкових даних
            list2 = LinkedList()
            list2_size = random.randint(5, 10)  # Генерація випадкового розміру другого списку
            list2.generate_random_list(list2_size)
            print(Fore.YELLOW + f"Сгенеровано другий список з {list2_size} елементами:")

            # Виводимо другий список
            list2.print_list()

            # Виводимо перший (основний) список
            print(Fore.YELLOW + "Перший (основний) список перед об'єднанням:")
            linked_list.print_list()

            # Об'єднуємо два відсортованих списки
            merged_head = linked_list.merge_sorted_lists(linked_list.head, list2.head)
            
            # Виводимо об'єднаний список
            print(Fore.GREEN + "Об'єднаний відсортований список:")
            merged_list = LinkedList()
            merged_list.head = merged_head
            merged_list.print_list()
        elif choice == '8':
            linked_list.print_list()
        elif choice == '9':
            size = int(input(Fore.YELLOW + "Введіть кількість елементів для генерації: "))
            linked_list.generate_random_list(size)
            logging.info(f"Сгенеровано {size} випадкових елементів.")
            print(Fore.GREEN + f"Сгенеровано {size} випадкових елементів.")
        elif choice == '0':
            logging.info("Користувач вийшов з програми.")
            print(Fore.CYAN + "Дякуємо за використання програми! До побачення!")
            break
        else:
            print(Fore.RED + "Невірний вибір. Спробуйте ще раз.")
        
        # Запит на продовження з умолчанням y
        while True:
            continue_choice = input(Fore.YELLOW + "Хотіте продовжити? (y/n): ").lower()
            if continue_choice == '' or continue_choice == 'y':  # Якщо порожньо або 'y'
                clear_screen()  # Очищаємо екран
                break
            elif continue_choice == 'n':
                print(Fore.CYAN + "Дякуємо за використання програми! До побачення!")
                break
            else:
                print(Fore.RED + "Невірний вибір. Будь ласка, введіть 'y' для продовження або 'n' для виходу.")
                continue
            break

# Запуск меню
menu()
