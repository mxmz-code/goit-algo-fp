import turtle
import time
import os
from colorama import Fore, Back, Style, init

# Ініціалізація colorama
init(autoreset=True)

# Функція для очищення консолі
def clear_console():
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux та macOS
        os.system('clear')

# Функція для малювання дерева Піфагора з кольорами та анімацією
def draw_tree(length, angle, level, color, max_level):
    if level == 0:
        return
    else:
        # Зміна кольору на основі рівня, використовуючи кольори українського флагу
        if level % 2 == 0:
            turtle.pencolor("#ffd700")  # Жовтий для нижніх гілок (ліві гілки)
        else:
            turtle.pencolor("#005bbb")  # Синій для верхніх гілок (праві гілки)
        
        # Малюємо основну гілку
        turtle.forward(length)
        
        # Малюємо праву гілку
        turtle.left(angle)
        draw_tree(length * 0.7, angle, level - 1, "brown", max_level)
        
        # Повертаємось назад і малюємо ліву гілку
        turtle.right(2 * angle)
        draw_tree(length * 0.7, angle, level - 1, "green", max_level)
        
        # Повертаємось до початкової позиції
        turtle.left(angle)
        turtle.backward(length)

# Функція для отримання валідного вводу
def get_valid_input(prompt, valid_options, default='y'):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == '':
            user_input = default  # Якщо Enter без вводу, вибирається 'y'
        if user_input in valid_options:
            return user_input
        print(f"{Fore.RED}Невірний ввід. Будь ласка, введіть {', '.join(valid_options)}.")

# Функція для очищення екрану перед кожним новим запуском
def reset_turtle():
    try:
        turtle.clearscreen()  # Очистка екрану, щоб не викликати turtle.Terminator
    except turtle.Terminator:
        pass  # Якщо вікно вже закрите, просто ігноруємо помилку

# Функція для безпечного завершення роботи програми без помилки
def safe_exit():
    try:
        turtle.bye()  # Закриття вікна turtle
    except turtle.Terminator:
        pass  # Ігноруємо помилку, якщо вікно вже закрите

# Основна частина програми
def main():
    clear_console()  # Очищення консолі при запуску програми

    # Привітання користувача та пояснення програми
    print(Fore.CYAN + Style.BRIGHT + """
    ***********************************************
    Привіт! Це програма для створення фрактала 'дерево Піфагора'.
    Використовує рекурсію для малювання дерева з гілками,
    що змінюються за розміром та кутом.
    Ви можете вказати рівень рекурсії, і програма побудує дерево відповідно до вашого вводу.
    ***********************************************
    """)

    # Вхідні дані від користувача
    while True:
        try:
            level = int(input(Fore.YELLOW + "Введіть рівень рекурсії (максимум 12, мінімум 1): "))
            if 1 <= level <= 12:
                break
            else:
                print(Fore.RED + "Рівень рекурсії має бути від 1 до 12.")
        except ValueError:
            print(Fore.RED + "Будь ласка, введіть число.")
    
    turtle.setup(800, 600)  # Тепер відкриваємо вікно лише після введення рівня
    turtle.clearscreen()  # Очистка екрану після введення рівня

    turtle.speed(0)  # Встановлюємо максимальну швидкість
    turtle.hideturtle()  # Сховати черепаху

    # Задаємо вертикальну орієнтацію (90 градусів)
    turtle.setheading(90)  # 90 градусів - вертикальне малювання

    # Початкові параметри
    length = 100  # Початкова довжина гілки
    angle = 30  # Кут між гілками

    # Малюємо дерево Піфагора з анімацією
    max_level = level
    draw_tree(length, angle, level, "brown", max_level)

    # Додавання анімації (переривання та поступове малювання)
    for _ in range(30):
        try:
            turtle.update()  # Оновлюємо екран
        except turtle.Terminator:
            print(Fore.RED + "Вікно анімації було закрите.")
            user_choice = get_valid_input(Fore.GREEN + "Бажаєте продовжити? (y/n): ", ['y', 'n'])
            if user_choice == 'y':
                reset_turtle()  # Перезапускаємо екран без закриття вікна
                main()  # Запускаємо програму знову
                return  # Завершуємо поточну версію функції
            else:
                print(Fore.MAGENTA + "Дякуємо за використання програми! До побачення!")
                safe_exit()  # Закриваємо вікно turtle без помилки
                return  # Завершуємо програму
        time.sleep(0.05)  # Затримка для анімації

    # Диалог після створення дерева
    while True:
        user_choice = get_valid_input(Fore.GREEN + "Чи хочете продовжити? (y/n): ", ['y', 'n'])
        if user_choice == 'y':
            reset_turtle()  # Перезапускаємо екран без закриття вікна
            main()  # Запускаємо програму знову
            break
        elif user_choice == 'n':
            print(Fore.MAGENTA + "Дякуємо за використання програми! До побачення!")
            safe_exit()  # Закриваємо вікно turtle без помилки
            break

# Виклик головної функції для початку роботи програми
if __name__ == "__main__":
    main()
