# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import data

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Heo")

def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="We're Pau Bernat and Andrea Garcia")

def graph(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="Hello")
     distance = update.message.float
     graph = data.create_graph(distance/1000)
     mapa = data.print_all(graph)
     bot.send_photo(chat_id=update.message.chat_id, photo=open("mapa.png", 'rb'))




TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph',  graph))
# engega el bot
updater.start_polling()
