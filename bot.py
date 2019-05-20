# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import data

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello")

def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="We're Pau Bernat and Andrea Garcia")

def graph(bot, update):
     distance = update.message.text[7:]
     if not distance:
         distance = float(1000)
     else:
         distance = float(distance)
     graph = data.create_graph(float(distance/1000))
     mapa = data.print_all(graph)
     imatge = mapa.render()
     imatge.save('mapa.png')
     bot.send_photo(chat_id=update.message.chat_id, photo=open('mapa.png', 'rb'))
     os.remove('mapa.png')

def nodes(bot, update):

    nodes = data.number_of_nodes(graph)


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph',  graph))
# engega el bot
updater.start_polling()
