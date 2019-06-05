import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import data

# Invalid Command
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unrecognized command. You will find the valid commands in the /help option")


# Handling errors
def errorhandler(type, bot, update):
    if type == 1: #The user doesn't start the bot
        bot.send_message(chat_id=update.message.chat_id, text="Please start the bot with the command /start")
    if type == 2: #There's no graph created
        bot.send_message(chat_id=update.message.chat_id, text="There's no graph, please use the command /graph to create one")
    if type == 3: #The path doesn't exist
        bot.send_message(chat_id=update.message.chat_id, text="There's no path, maybe the adresses aren't correct")
    if type == 4: #The user introduces a invalid distance
        bot.send_message(chat_id=update.message.chat_id, text="Please introduce a valid distance")
    if type == 5: #The user introduces a invalid number of required bikes and docks
        bot.send_message(chat_id=update.message.chat_id, text="Please introduce a valid number of required bikes and docks")
    if type == 6: #There's no solution in the distribute command
        bot.send_message(chat_id=update.message.chat_id, text="Not solution could be found")
    if type == 7: #The distribute graph is incorrect
        bot.send_message(chat_id=update.message.chat_id, text="Something goes wrong, incorrect graph model")


# Starts the bot
def start(bot, update, user_data):
    user_data['graph'] = 0
    bot.send_message(chat_id=update.message.chat_id, text="Hello")


# Gives the author names
def author(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="We're Pau Bernat and Andrea Garcia")


# Help command, explains how the bot works
def help(bot, update):
    message = 'The commands available in this Bot are: /graph <distance> , /plotgraph , /nodes , /edges , /components , /route <adresses> , /distribute <demand> , /author'
    bot.send_message(chat_id=update.message.chat.id, text=message)


# Creates the graph with the distance introduced by the user
def graph(bot, update, user_data):
     distance = update.message.text[7:]
     if not distance:
         distance = 1000
     else:
         if not distance.isdigit() or float(distance) <= 0 :
             errorhandler(4, bot, update)
             return
     graph = data.create_graph((float(distance))/1000)
     user_data['graph'] = graph
     bot.send_message(chat_id=update.message.chat_id, text="Graph created")

# Plots the graph create with the /graph command
def plotgraph(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        file = "%d.png" % random.randint(10000000, 9999999)
        print(file)
        data.print_all(g, file)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(file, 'rb'))
        os.remove(file)

#Gives the number of nodes of the graph created by the user
def nodes(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        nodes = data.number_of_nodes(g)
        bot.send_message(chat_id=update.message.chat_id, text = nodes)

#Gives the number of edges of the graph created by the user
def edges(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        edges = data.number_of_edges(g)
        bot.send_message(chat_id=update.message.chat_id, text = edges)

# Gives the number of connex components of the graph created by the user
def components(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        components = data.number_of_non_connex_components(g)
        bot.send_message(chat_id=update.message.chat_id, text = components)

# Plots the shortest path between two adresses given by the user
def path(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        adresses = update.message.text[7:]
        path = data.shortest_path(g, adresses)
        if path == None:
            errorhandler(3, bot, update)
        map1 = data.print_path_solo(path)
        imatge = map1.render()
        imatge.save('path_solo.png')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('path_solo.png', 'rb'))
        os.remove('path_solo.png')
        map2 = data.print_path_in_graph(path)
        imatge2 = map2.render()
        imatge2.save('path_in_graph.png')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('path_in_graph.png', 'rb'))
        os.remove('path_in_graph.png')

# Returns the total cost of d
def distribute(bot, update, user_data):
    g = user_data['graph']
    if g == 0:
        errorhandler(2, bot, update)
    else:
        nums = update.message.text[12:]
        bikes, docks = nums.split(' ')
        if not bikes.isdigit() or int(bikes) < 0 :
            errorhandler(5, bot, update)
            return
        if not docks.isdigit() or int(docks) < 0 :
            errorhandler(5, bot, update)
            return
        flow, max = data.distribute(int(bikes), int(docks), g)
        if flow == -1:
            errorhandler(6, bot, update)
            return
        if flow == -2:
            errorhandler(7, bot, update)
            return
        bot.send_message(chat_id=update.message.chat_id, text = "The total cost of tranfering bikes is " + str(flow) + " km")
        if flow == 0.0:
            bot.send_message(chat_id=update.message.chat_id, text = "All the edges has cost 0.0")
        else:
            bot.send_message(chat_id=update.message.chat_id, text = "The maximum edge cost is from " +  str(max[1]) + " to " + str(max[2]) + " with " + str(max[0]))


TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Commands available
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('author', author, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('graph',  graph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', path, pass_user_data=True))
dispatcher.add_handler(CommandHandler('distribute', distribute, pass_user_data=True))
dispatcher.add_handler(MessageHandler([Filters.command], unknown)) # Invalid command

updater.start_polling()
