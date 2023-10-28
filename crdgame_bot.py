import telebot
import random

SECRET_KEY = "6529602798:AAGJHd-7NvawjVooxMFVlJx8kZve3T7OziM"

# Инициализация бота
bot = telebot.TeleBot(SECRET_KEY)

# Создание словаря для изображений мастей карт
suits_images = {'Spades': '♠', 'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣'}

# Создание колоды карт
ranks = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King',
    'Ace'
]

# Уровень сложности по умолчанию (1 - отгадывание цвета масти)
user_level = {}

# Словарь для хранения текущей карты пользователя
user_card = {}

# Словарь для хранения статистики игры
user_stats = {}

# Функция для начала игры
@bot.message_handler(commands=['start'])
def start(message):
  user_id = message.chat.id

  markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = telebot.types.KeyboardButton("Уровень 1: Угадай цвет масти карты")
  item2 = telebot.types.KeyboardButton("Уровень 2: Угадай масть карты")
  item3 = telebot.types.KeyboardButton("Уровень 3: Угадай саму карту")
  markup.row(item1)
  markup.row(item2)
  markup.row(item3)

  bot.send_message(
      user_id,
      "Добро пожаловать в игру: Отгадай карту! Выбери уровень сложности:",
      reply_markup=markup)
  
  bot.send_message(user_id, f"Для вызова статистики наберите: Statistics")

# Функция для выбора уровня сложности
@bot.message_handler(func=lambda message: message.text in [
    "Уровень 1: Угадай цвет масти карты", "Уровень 2: Угадай масть карты",
    "Уровень 3: Угадай саму карту"
])
def choose_level(message):
  user_id = message.chat.id
  level = message.text

  if level == "Уровень 1: Угадай цвет масти карты":
    user_level[user_id] = 1
  elif level == "Уровень 2: Угадай масть карты":
    user_level[user_id] = 2
  elif level == "Уровень 3: Угадай саму карту":
    user_level[user_id] = 3

  start_game(user_id)


# Функция для начала игры и генерации случайной карты
def start_game(user_id):
  suit = random.choice(list(suits_images.keys()))  # Выбираем масть
  global_suit = suit
  rank = random.choice(ranks)
  global_rank = rank
  user_card[user_id] = {'suit': suit, 'rank': rank}
  user_stats.setdefault(user_id, {
      'correct': 0,
      'incorrect': 0
  })  # Инициализация статистики

  if user_level[user_id] == 1:
    bot.send_message(user_id, f"Угадай цвет масти (Red or Black):")
  elif user_level[user_id] == 2:
    bot.send_message(user_id, f"Угадай масть карты:\nRank: {rank}")
  elif user_level[user_id] == 3:
    bot.send_message(
        user_id, f"Угадай карту:\nRank: {rank}\nSuit: {suits_images[suit]}")


# Функция для проверки угадывания
@bot.message_handler(
    func=lambda message: message.text in
    ["Red", "Black", "Spades", "Hearts", "Diamonds", "Clubs"] + ranks)
def check_guess(message):
  user_id = message.chat.id
  user_guess = message.text

  if user_id not in user_level:
    start(message)  # Если уровень не выбран, вернуться к выбору уровня
    return

  if user_level[user_id] == 1:
    correct_suit_color = 'Red' if user_card[user_id]['suit'] in [
        'Hearts', 'Diamonds'
    ] else 'Black'
    check_result(user_id, user_guess == correct_suit_color)
  elif user_level[user_id] == 2:
    correct_suit = user_card[user_id]['suit']
    check_result(user_id, user_guess == correct_suit)
  elif user_level[user_id] == 3:
    correct_rank = user_card[user_id]['rank']
    correct_suit = user_card[user_id]['suit']
    check_result(user_id, user_guess == f"{correct_rank} of {correct_suit}")


# Функция для проверки результата и обновления статистики
def check_result(user_id, is_correct):
  correct_card = user_card[user_id]
  user_stats[user_id]['correct' if is_correct else 'incorrect'] += 1
  if is_correct:
    bot.send_message(user_id, "Вы угадали!")
    bot.send_message(
        user_id,
        f"Была загадана карта: {correct_card['rank']}{suits_images[correct_card['suit']]}")
  else:
    bot.send_message(user_id, "Вы не угадали!")
    bot.send_message(
        user_id,
        f"Была загадана карта: {correct_card['rank']}{suits_images[correct_card['suit']]}")

  start_game(user_id)


# Функция для вывода статистики
@bot.message_handler(func=lambda message: message.text == "Statistics")
def show_stats(message):
  user_id = message.chat.id

  if user_id in user_stats:
    stats = user_stats[user_id]
    total = stats['correct'] + stats['incorrect']
    accuracy = (stats['correct'] / total) * 100 if total > 0 else 0
    bot.send_message(
        user_id,
        f"Статистика:\nПравильных ответов: {stats['correct']}\nНеправильных ответов: {stats['incorrect']}\nТочность ответов: {accuracy:.2f}%"
    )
  else:
    bot.send_message(user_id, "Статистика не доступна. Сначала начните игру.")


# Запуск бота
if __name__ == "__main__":
  bot.polling()
