import os
from colorama import init, Fore, Style

# Ініціалізація colorama для коректної роботи кольорового виводу в консолі Windows
init(autoreset=True)

# Функція для очищення екрану консолі
def clear_screen():
    """Очищає екран консоли залежно від операційної системи."""
    if os.name == 'nt':  # Якщо Windows
        os.system('cls')
    else:  # Якщо Linux або macOS
        os.system('clear')

# Функція для малювання горизонтальної лінії
def draw_line(length, char='-'):
    """Малює горизонтальну лінію заданої довжини."""
    print(char * length)

# Функція для малювання смуги прогресу
def draw_bar(value, max_value, length=30):
    """Малює горизонтальну смугу прогресу для візуалізації величини."""
    bar_length = int(value / max_value * length)
    bar = '█' * bar_length + '-' * (length - bar_length)
    return bar

# Функція для жадібного алгоритму
def greedy_algorithm(items, budget):
    """
    Реалізація жадібного алгоритму для вибору страви з найбільшою калорійністю за одиницю вартості
    без перевищення бюджету.
    """
    print(Fore.YELLOW + "\n--- Жадібний алгоритм ---" + Style.RESET_ALL)
    
    # Обчислюємо співвідношення калорій до вартості для кожної страви
    ratios = []
    for item, details in items.items():
        ratio = details["calories"] / details["cost"]
        ratios.append((item, ratio, details["cost"], details["calories"]))
    
    # Сортуємо страви за співвідношенням калорій до вартості у порядку спадання
    ratios.sort(key=lambda x: x[1], reverse=True)
    
    print(Fore.GREEN + "\nТаблиця страв з їх співвідношенням калорій до вартості (calories/cost):")
    print(f"{'Страва':<12} {'Співвідношення':<15} {'Вартість (грн)':<15} {'Калорії':<10} {'Прогрес (калорії)'}")
    draw_line(70)
    for item, ratio, cost, calories in ratios:
        bar = draw_bar(calories, 1000)  # 1000 — максимальна кількість калорій
        print(f"{item:<12} {ratio:<15.2f} {cost:<15} {calories:<10} {bar}")
    draw_line(70)

    selected_items = []  # Список вибраних страв
    total_cost = 0  # Загальна вартість
    total_calories = 0  # Загальна калорійність

    print("\nВибір страв, що не перевищує бюджет...")
    for item, ratio, cost, calories in ratios:
        if total_cost + cost <= budget:  # Перевіряємо, чи не перевищуємо бюджет
            selected_items.append(item)
            total_cost += cost
            total_calories += calories
            print(Fore.CYAN + f"Вибрано: {item} | Вартість: {cost} грн | Калорії: {calories}" + Style.RESET_ALL)

    # Виведення смуги прогресу для калорій та вартості
    print("\nСмуга прогресу для загальної вартості:")
    print(draw_bar(total_cost, budget, 40))
    print(Fore.YELLOW + f"Загальна вартість: {total_cost} грн з {budget} грн" + Style.RESET_ALL)
    
    print("\nСмуга прогресу для загальної калорійності:")
    print(draw_bar(total_calories, 1000, 40))  # 1000 — максимальне значення калорій
    print(Fore.YELLOW + f"Загальна калорійність: {total_calories} калорій" + Style.RESET_ALL)
    
    return selected_items, total_calories, total_cost

# Функція для алгоритму динамічного програмування
def dynamic_programming(items, budget):
    """
    Реалізація алгоритму динамічного програмування для вибору страви з найбільшою калорійністю
    при заданому бюджеті.
    """
    print(Fore.YELLOW + "\n--- Динамічне програмування ---" + Style.RESET_ALL)
    
    # Створюємо таблицю для зберігання максимальної калорійності для кожного бюджету
    n = len(items)
    dp = [0] * (budget + 1)
    item_list = list(items.items())
    
    # Заповнюємо таблицю dp, перевіряючи всі страви
    for i in range(n):
        item, details = item_list[i]
        cost = details["cost"]
        calories = details["calories"]
        
        # Заповнюємо таблицю dp ззаду вперед, щоб не перезаписати значення, які ще використовуються
        for b in range(budget, cost - 1, -1):
            dp[b] = max(dp[b], dp[b - cost] + calories)
    
    print(Fore.GREEN + "\nТаблиця для заповнення максимальної калорійності при кожному бюджеті:")
    print(f"{'Бюджет (грн)':<15} {'Калорії':<10} {'Прогрес калорії'}")
    draw_line(40)
    for b in range(budget + 1):
        bar = draw_bar(dp[b], 1000)  # 1000 — максимальна кількість калорій
        print(f"{b:<15} {dp[b]:<10} {bar}")
    draw_line(40)

    # Визначаємо, які страви були вибрані
    selected_items = []
    remaining_budget = budget
    print("\nВибір страв для досягнення максимальних калорій...")
    for i in range(n - 1, -1, -1):
        item, details = item_list[i]
        cost = details["cost"]
        if remaining_budget >= cost and dp[remaining_budget] == dp[remaining_budget - cost] + details["calories"]:
            selected_items.append(item)
            remaining_budget -= cost
            print(Fore.CYAN + f"Вибрано: {item} | Вартість: {cost} грн | Калорії: {details['calories']}" + Style.RESET_ALL)

    # Виведення смуги прогресу для калорій та вартості
    print("\nСмуга прогресу для загальної вартості:")
    print(draw_bar(sum([items[item]["cost"] for item in selected_items]), budget, 40))
    print(Fore.YELLOW + f"Загальна вартість: {sum([items[item]['cost'] for item in selected_items])} грн з {budget} грн" + Style.RESET_ALL)
    
    print("\nСмуга прогресу для загальної калорійності:")
    total_calories = sum([items[item]["calories"] for item in selected_items])
    print(draw_bar(total_calories, 1000, 40))  # 1000 — максимальне значення калорій
    print(Fore.YELLOW + f"Загальна калорійність: {total_calories} калорій" + Style.RESET_ALL)
    
    selected_items.reverse()  # Сортуємо у порядку вибору
    return selected_items, total_calories

# Дані про їжу
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

# Бюджет
budget = 100

# Виведення інформації для користувача
clear_screen()  # Очищаємо екран перед виведенням нової інформації
print(Fore.MAGENTA + "Задача: вибір страв з найбільшою калорійністю, не перевищуючи бюджет." + Style.RESET_ALL)
print(Fore.YELLOW + f"Заданий бюджет: {budget} грн" + Style.RESET_ALL)

# Використовуємо жадібний алгоритм
greedy_items, greedy_calories, greedy_cost = greedy_algorithm(items, budget)
print(Fore.GREEN + "\n--- Результати жадібного алгоритму ---" + Style.RESET_ALL)
print(f"Вибрані страви: {greedy_items}")
print(f"Загальна калорійність: {greedy_calories} калорій")
print(f"Загальна вартість: {greedy_cost} грн")

# Використовуємо динамічне програмування
dp_items, dp_calories = dynamic_programming(items, budget)
print(Fore.GREEN + "\n--- Результати динамічного програмування ---" + Style.RESET_ALL)
print(f"Вибрані страви: {dp_items}")
print(f"Загальна калорійність: {dp_calories} калорій")
