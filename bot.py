# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from data2 import *
import string

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
     graph = data2.create_graph(float(distance/1000))
     user_data[update.message.username] = graph
     mapa = data2.print_all(graph)
     imatge = mapa.render()
     imatge.save('mapa.png')
     bot.send_photo(chat_id=update.message.chat_id, photo=open('mapa.png', 'rb'))
     os.remove('mapa.png')

def nodes(bot, update):
    g = user_data[update.message.username]
    nodes = data2.number_of_nodes(g)
    bot.send_message(chat_id=update.message.chat_id, text = nodes)

def edges(bot, update):
    g = user_data[update.message.username]
    edges = data2.number_of_edges(g)
    bot.send_message(chat_id=update.message.chat_id, text = edges)

def components(bot, update):
    g = user_data[update.message.username]
    components = data2.number_of_non_connex_components(g)
    bot.send_message(chat_id=update.message.chat_id, text = components)


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph',  graph))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))

# engega el bot
updater.start_polling()
