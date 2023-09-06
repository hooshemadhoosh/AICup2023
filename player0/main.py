import random
from src.game import Game
VARS = {"strategic_troops_number":8 , "mytroops/enemytroops (beta)" : 1.2}
flag = False


#the following function gets the adjacents of all nodes and the most important strategic node which we want
#and return the best adjacent to put troops on for attacking
def find_best_adj (dict_of_troops , alladj , most_strategic_node , owner , my_id):
    highest_num_of_troops = 0
    best_adj = 0
    for each_adj in alladj[most_strategic_node]: #searching in the adjacment of strategic node
        if owner[str(each_adj)] == my_id and dict_of_troops[str(each_adj)] > highest_num_of_troops:
            best_adj = each_adj
            highest_num_of_troops = dict_of_troops[str(each_adj)]
        elif owner[str(each_adj)] == -1:
            best_adj = each_adj
    return best_adj

def Tunnel(start, dict_adj):
    dp = [10000] * (len(dict_adj) + 1)
    mark = [0] * (len(dict_adj) + 1)
    uplist = [-1] * (len(dict_adj) + 1)
    mark[start] = 1
    dp[start] = 0
    que = []
    que.append(start) 
    while len(que):
        point = que.pop(0)
        for i in dict_adj[point]:
            if(mark[i] == 0):
                mark[i] = 1 
                que.append(i)
                dp[i] = dp[point] + 1
                uplist[i] = point
    
    return (uplist)


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
    my_id = game.get_player_id()['player_id']



    #the first state! putting troops!
    global flag
    owner = game.get_owners()
    my_remaining_troops = game.get_number_of_troops_to_put()['number_of_troops']
    strategic_nodes = game.get_strategic_nodes() ['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    adjacents = game.get_adj()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    opurtunity_of_attacking_strategic_nodes = {}
    beta = VARS["mytroops/enemytroops (beta)"]

    for s in strategic_nodes:  
        enemy_troops_on_node = int(number_of_troops[str(s)]) + int(number_of_fort_troops[str(s)]) #getting the number of enemy troops on the strategic node
        if owner[str(s)] != my_id and ((my_remaining_troops-2) / enemy_troops_on_node) > beta:
            number_of_free_adjacents_of_strategic_node = 0

            #adding "the chance of successful attack on each neighbor of strategic node" as value to the opurtunity_of_attacking_strategic_nodes dictionary with the key of that node
            for neighborss in adjacents[str(s)]:
                if owner[str(neighborss)] == -1 or owner[str(neighborss)]==my_id:
                    number_of_free_adjacents_of_strategic_node += 1
            if number_of_free_adjacents_of_strategic_node != 0:
                opurtunity_of_attacking_strategic_nodes [str(s)] = score[strategic_nodes.index(s)]*my_remaining_troops*number_of_free_adjacents_of_strategic_node / enemy_troops_on_node


    #start putting troops on suitable nodes that we have chosen above...
    if len(opurtunity_of_attacking_strategic_nodes) >= 1:
        #sorting the chance of attacking in the dictionary from a high amount to a low one
        opurtunity_of_attacking_strategic_nodes_sorted_from_high_to_low = sorted(opurtunity_of_attacking_strategic_nodes.items(), key = lambda item: item[1] , reverse=True)
        pointed_node = opurtunity_of_attacking_strategic_nodes_sorted_from_high_to_low[0][0] #pointing a node with the most chance of successful attack 
        best_adj_to_put_froot = find_best_adj(number_of_troops , adjacents , pointed_node , owner , my_id)
        n_defenders = number_of_fort_troops[str(best_adj_to_put_froot)] + number_of_troops[str(best_adj_to_put_froot)]
        num_of_troops = (int(-(-(beta*n_defenders)//1))+2) - number_of_troops[str(best_adj_to_put_froot)]
        if my_remaining_troops > num_of_troops :
            print (game.put_troop(best_adj_to_put_froot , num_of_troops))#put n troops on the best choice of attacking, which n has been rounded up to ensure that the attack will be successful!

    #if there isn't any suitable node to put troops on we should put our troops on the nodes that we have now or the nodes which no one own them randomly!
    list_of_my_or_free_nodes = [] 
    for x in owner: #i used this instad of     for i in owner.keys()
        if (owner[x] == my_id or owner[x] == -1) and game.get_number_of_troops_to_put()['number_of_troops'] > 1:
            list_of_my_or_free_nodes.append(int(x))
    while game.get_number_of_troops_to_put()['number_of_troops'] > 2:
        print (game.put_troop(random.choice(list_of_my_or_free_nodes), random.choice([2,3])))


#   if game.get_number_of_troops_to_put()['number_of_troops'] > 1:       
#       list_of_my_nodes = []
#       for i in owner: #i used this instad of     for i in owner.keys()
#           if owner[str(i)] == my_id:
#                   list_of_my_nodes.append(i)
#       print(game.put_troop(random.choice(list_of_my_nodes), game.get_number_of_troops_to_put()['number_of_troops']))
#   
#   print(game.get_number_of_troops_to_put())
    print(game.next_state()) #going to the next state




    #the second state! attacking!
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()

    if len(opurtunity_of_attacking_strategic_nodes) >= 1:
        for on in opurtunity_of_attacking_strategic_nodes_sorted_from_high_to_low:
            adj_to_attack = find_best_adj(number_of_troops , adjacents , on , owner , my_id)
            defenders = number_of_troops[str(on)] + number_of_fort_troops[str(on)]
            if (number_of_troops[str(adj_to_attack)]/defenders) > 1.3:
                print (game.attack(adj_to_attack, on, beta, 0.5))
                break
    else:
        # find the node with the most troops that I own
        max_troops = 0
        max_node = -1
        owner = game.get_owners()
        for i in owner: #i used this instad of     for i in owner.keys()
            if owner[str(i)] == my_id:
                if game.get_number_of_troops()[i] > max_troops:
                    max_troops = game.get_number_of_troops()[i]
                    max_node = i
                    
    # find a neighbor of that node that I don't own and attack it! (default code)
        adj = game.get_adj()
        for i in adj[max_node]:
            if owner[str(i)] != my_id and owner[str(i)] != -1:
                print(game.attack(max_node, i, beta, 0.5))
                break
    

    print(game.next_state())
    print(game.get_state())




    #the third state! moving troops state!

    # get the node with the most troops that I own (default code)
    max_troops = 0
    max_node = -1
    owner = game.get_owners()

    for i in owner: #i used this instad of     for i in owner.keys()
        if owner[str(i)] == my_id:
            if game.get_number_of_troops()[i] > max_troops:
                max_troops = game.get_number_of_troops()[i]
                max_node = i

    print(game.get_reachable(max_node))
    destination = random.choice(game.get_reachable(max_node)['reachable'])
    print(game.move_troop(max_node, destination, 1))
    print(game.next_state())




    #the last state! forting!

    # get the node with the most troops that I own (default code)
    if flag == False:
        max_troops = 0
        max_node = -1
        owner = game.get_owners()
        for i in owner: #i used this instad of     for i in owner.keys()
            if owner[str(i)] == my_id:
                if game.get_number_of_troops()[i] > max_troops:
                    max_troops = game.get_number_of_troops()[i]
                    max_node = i

        print(game.get_number_of_troops()[str(max_node)])
        print(game.fort(max_node, 3))
        print(game.get_number_of_fort_troops())
        flag = True 