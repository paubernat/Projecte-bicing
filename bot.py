import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import data2


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unrecognized command. You will find the valid commands in the /help option")

def errorhandler(type, bot, update):
    #posar error per start y comanda no trobada
    if type == 1:
            bot.send_message(chat_id=update.message.chat_id, text="Please start the bot with the command /start")
    if type == 2:
        bot.send_message(chat_id=update.message.chat_id, text="There's no graph, please use the command /graph to create one")
    if type == 3:
        bot.send_message(chat_id=update.message.chat_id, text="There's no path, maybe the adresses aren't correct")
    if type == 4:
        bot.send_message(chat_id=update.message.chat_id, text="Please introduce a valid distance")

def start(bot, update, user_data):
    user_data['inline'] = 1
    user_data['graph'] = 0
    start = True
    bot.send_message(chat_id=update.message.chat_id, text="Hello")

def author(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="We're Pau Bernat and Andrea Garcia")

def help(bot, update):
    message = ' '
    bot.send_message(chat_id=update.message.chat.id, text=message)

def graph(bot, update, user_data):
     distance = update.message.text[7:]
     if not distance:
         distance = 1000
     else:
         if not distance.isdigit() or float(distance) <= 0 :
             errorhandler(4, bot, update)
             return
     graph = data2.create_graph((float(distance))/1000)
     user_data['graph'] = graph
     bot.send_message(chat_id=update.message.chat_id, text="Graph created")

def plotgraph(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        map = data2.print_all(g)
        imatge = map.render()
        imatge.save('mapa.png')
        print('mapa')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('mapa.png', 'rd'))
        os.remove('mapa.png')

def nodes(bot, update, user_data):
    g = user_data['graph']
    if g == 0:s
        errorhandler(2, bot, update)
    else:
        nodes = data2.number_of_nodes(g)
        bot.send_message(chat_id=update.message.chat_id, text = nodes)

def edges(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        edges = data2.number_of_edges(g)
        bot.send_message(chat_id=update.message.chat_id, text = edges)

def components(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        components = data2.number_of_non_connex_components(g)
        bot.send_message(chat_id=update.message.chat_id, text = components)

def path(bot, update, user_data):
    adresses = update.message.text[7:]
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        path = data2.shortest_path(g, adresses)
        print(path)
        if path == None:
            errorhandler(3, bot, update)
        map1 = data2.print_path_solo(path)
        imatge = map1.render()
        imatge.save('path_solo.png')
        print('foto')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('path_solo.png', 'rb'))
        print('enviat')
        os.remove('path_solo.png')
        map2 = data2.print_path_in_graph(path)
        imatge2 = map2.render()
        imatge2.save('path_in_graph.png')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('path_in_graph.png', 'rb'))
        os.remove('path_in_graph.png')

TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('author', author, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('graph',  graph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', path, pass_user_data=True))
dispatcher.add_handler(MessageHandler([Filters.command], unknown))
# engega el bot
updater.start_polling()
