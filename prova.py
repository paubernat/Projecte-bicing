dispatcher.add_handler(CommandHandler('nodes',  nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))



def nodes(bot, update):
    nodes = data.number_of_nodes(graph)
    bot.send_message(chat_id=update.message.chat_id, text=nodes)

def edges(bot, update):

    edges = data.number_of_edges(graph)
    bot.send_message(chat_id=update.message.chat_id, text=edges)

def components(bot, update):
    components = data.number_connected_components(graph)
    bot.send_message(chat_id=update.message.chat_id, text=components)

def bounging_box(dist):
    #Bounding Box
    max_lat, max_lon, min_lat, min_lon = 0.0;
    for node in list(G.node(data=True)):
        if node[0][1] < min_lon:
            min_lon = node[0][1]
        if node[0][1] > max_lon:
            max_lon = node[0][1]
        if node[0][2] < min_lat:
            min_lat = node[0][2]
        if node[0][2] > max_lat:
            max_lat = node[0][2]
    coor1 = (max_lon, min_lat)
    coor2 = (max_lon, max_lat)
    coor3 = (min_lon, max_lat)
    coor4 = (min_lon, min_lat)
    #Distance between nodes of the Bounding Box
    w = haversine(coor4, coor1)
    h = haversine(coor3, coor2)
    #Number of boxes inside the grid nxm
    n =(int)w/dist +1
    m =(int)h/dist +1
    return n, m


def grid(n, m):
    Matrix = [[]]
