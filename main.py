from telebot import TeleBot
import os

TOKEN = os.getenv("BOT_TOKEN")

TOKEN = '7030634417:AAFHpZ7NqmMgjf30vYRh8JKMpBKzlaT-404'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привіт!')

@bot.message_handler(content_types=['text'])
def get_txt_message(message):
    bot.send_message(message.from_user.id, message.text)

bot.polling(non_stop=True, interval=0)