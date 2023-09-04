import random
from src.game import Game
VARS = {"strategic_troops_number":8}
flag = False

def initializer(game: Game):   
    strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    owner = game.get_owners()
    my_id = game.get_player_id()['player_id']
    adj = game.get_adj()
    troops_of = game.get_number_of_troops()
    print("Turn Number: ",game.get_turn_number())
    #print(f"STRATEGIC NODES: {strategic_nodes}\n SCORE: {score}")

    #Filling Strategic Nodes...
    for i in strategic_nodes:
        if owner[str(i)] == -1:
            print(game.put_one_troop(i), "-- putting one troop on", i)
            return 
        
    #Filling Adjacents of Strategic nodes orderd by most degree
    for i in strategic_nodes:
        ordered_adj = [k for k in adj[str(i)]]
        ordered_adj.sort(key= lambda adjacent: len(adj[str(adjacent)]) , reverse=True)
        for j in ordered_adj:
            if owner[str(j)] == -1:
                print(game.put_one_troop(j), "-- putting one troop on neighbor of strategic node", j)
                return
            
    #Reinforcement Of our Strategic Nodes
    for i in strategic_nodes:
        if owner[str(i)]==my_id and troops_of[str(i)]<VARS['strategic_troops_number']:
            print(game.put_one_troop(i), "-- putting one troop on neighbor of strategic node", j)
            return
    return

def turn(game):
    global flag
    print(game.get_number_of_troops_to_put())
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == -1 and game.get_number_of_troops_to_put()['number_of_troops'] > 1:
            print(game.put_troop(i, 1))
            
    list_of_my_nodes = []
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            list_of_my_nodes.append(i)
    print(game.put_troop(random.choice(list_of_my_nodes), game.get_number_of_troops_to_put()['number_of_troops']))
    print(game.get_number_of_troops_to_put())

    print(game.next_state())

    # find the node with the most troops that I own
    max_troops = 0
    max_node = -1
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            if game.get_number_of_troops()[i] > max_troops:
                max_troops = game.get_number_of_troops()[i]
                max_node = i
    # find a neighbor of that node that I don't own
    adj = game.get_adj()
    for i in adj[max_node]:
        if owner[str(i)] != game.get_player_id()['player_id'] and owner[str(i)] != -1:
            print(game.attack(max_node, i, 1, 0.5))
            break
    print(game.next_state())
    print(game.get_state())
    # get the node with the most troops that I own
    max_troops = 0
    max_node = -1
    owner = game.get_owners()
    for i in owner.keys():
        if owner[str(i)] == game.get_player_id()['player_id']:
            if game.get_number_of_troops()[i] > max_troops:
                max_troops = game.get_number_of_troops()[i]
                max_node = i
    print(game.get_reachable(max_node))
    destination = random.choice(game.get_reachable(max_node)['reachable'])
    print(game.move_troop(max_node, destination, 1))
    print(game.next_state())

    if flag == False:
        max_troops = 0
        max_node = -1
        owner = game.get_owners()
        for i in owner.keys():
            if owner[str(i)] == game.get_player_id()['player_id']:
                if game.get_number_of_troops()[i] > max_troops:
                    max_troops = game.get_number_of_troops()[i]
                    max_node = i

        print(game.get_number_of_troops()[str(max_node)])
        print(game.fort(max_node, 3))
        print(game.get_number_of_fort_troops())
        flag = True
