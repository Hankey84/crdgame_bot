import telebot
import random
#from PIL import Image, ImageGrab, ImageOp

SECRET_KEY = "6529602798:AAGJHd-7NvawjVooxMFVlJx8kZve3T7OziM"
bot = telebot.TeleBot(SECRET_KEY)


@bot.message_handler(commands=['start'])
def start(message):
  keyboard = telebot.types.ReplyKeyboardMarkup()
  red_button = telebot.types.KeyboardButton("🟥")
  black_button = telebot.types.KeyboardButton("⬛️")
  keyboard.add(red_button)
  keyboard.add(black_button)
  bot.send_message(message.chat.id,
                   "Угадай цвет масти карты: 🟥 или ⬛️",
                   reply_markup=keyboard)
  bot.register_next_step_handler(message, answer_card)


def answer_card(message):
  value, suit = generate_random_card()
  player_answer = message.text
  if player_answer == "🟥" and suit in ["Ч", "Б"]:
    bot.send_message(message.chat.id,
                     f'Угадали! эта карта была: {value} {suit}')
  elif player_answer == "⬛️" and suit in ["П", "К"]:
    bot.send_message(message.chat.id,
                     f'Угадали! эта карта была: {value} {suit}')
  else:
    bot.send_message(message.chat.id,
                     f'Не угадали! эта карта была: {value} {suit}')

  bot.send_message(message.chat.id, 'Давай попробуем еще раз...')
  start(message)


def generate_random_card():
  value = random.choice(
      ["2", "3", "4", "5", "6", "7", "8", "9", "10", "В", "Д", "К", "Т"])
  suit = random.choice(["Ч", "Б", "К", "П"])
  return value, suit


bot.infinity_polling()
