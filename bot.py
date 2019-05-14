# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello")

def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="We are Pau Bernat and Andrea Garcia, nice to meet you!")

TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
# engega el bot
updater.start_polling()
