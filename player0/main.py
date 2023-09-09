import random
from src.game import Game
VARS = {"strategic_troops_number":8 , "mytroops/enemytroops (beta)" : 1.2 , "beta_plus": 1.5, "TroopsTunnel" : 3 , "number_of_attack_attemps" : 3 , "troops_to_put_on_strategics" : 3 , "moving_fraction" : 0.7}
flag = False

ListOfTunnels = []


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
        for i in dict_adj[str(point)]:
            if(mark[i] == 0):
                mark[i] = 1 
                que.append(i)
                dp[i] = dp[point] + 1
                uplist[i] = point
    
    return (uplist)


def TunnelListMaker(list_of_my_strategics,list_of_enemy_strategics,dict_adj):
    result = []
    for my_strategic in list_of_my_strategics:
        my_uplist = Tunnel(my_strategic,dict_adj)
        for enemy_strategic in list_of_enemy_strategics:
            Tunnel_listt = []
            x = enemy_strategic
            while(x != -1):
                Tunnel_listt.append(x)
                x = my_uplist[x]
            
        Tunnel_listt.reverse()
        result.append(Tunnel_listt)
    result.sort(key=lambda x: len(x))
    print('THIS IS ORDERED LIST OF TUNNELS ',result)
    return result[:4]




def initializer(game: Game):
    global ListOfTunnels   
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
            
    

    # Categorizing Strategic nodes by owner 
    my_best_strategic  = []
    enemy_best_strategic = []
    for i in strategic_nodes:
        if (owner[str(i)] == my_id) and (i not in my_best_strategic):
            my_best_strategic.append(i)
        elif (i not in enemy_best_strategic):
            enemy_best_strategic.append(i)
        
    # Make tunnel from my strategtic to enemy strategic :)
    if len(ListOfTunnels) == 0: ListOfTunnels=TunnelListMaker(my_best_strategic,enemy_best_strategic,adj)

    #Filling tunnels with troop
    for tunnel in ListOfTunnels:
        for node in tunnel:
            if(owner[str(node)] == -1):
                game.put_one_troop(node)
                print(f"One Troop Added to Tunnel on node {node}")
                return
    
    #Reinforcement Of our Strategic Nodes
    for i in strategic_nodes:
        if owner[str(i)]==my_id and troops_of[str(i)]<VARS['strategic_troops_number']:
            print(game.put_one_troop(i), "-- putting one troop on neighbor of strategic node", j)
            return
    
    # give 3 troops to all Tunnelnode  :)
    for tunnel in ListOfTunnels:
        for node in tunnel:
            if(troops_of[str(node)] < VARS['TroopsTunnel'] and owner[str(node)] == my_id):
                game.put_one_troop(node)
                print(f"One Troop Added to Tunnel on node {node}")
                return
    

    
    
    return
    
    
 
def turn(game):
    my_id = game.get_player_id()['player_id']



    #PUTTING TROOPS STATE
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
    opurtunity_of_attacks = {}
    beta = VARS["mytroops/enemytroops (beta)"]
    beta_plus = VARS["beta_plus"]
    attack_attemps = VARS["number_of_attack_attemps"]



    #START TASK 1
    for enemy in strategic_nodes:  
        if owner[str(enemy)] != my_id:
            enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)]) #getting the number of enemy troops on the strategic node
            for my in adjacents[str(enemy)]:    
                if owner[str(my)] == my_id:
                    my_troops_layer1node = number_of_troops[str(my)]               
                    attack_score = (my_remaining_troops-attack_attemps + my_troops_layer1node)/enemy_troops_on_node
                    if attack_score > beta: 
                        opurtunity_of_attacks [(my , enemy)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False}

    #start putting troops on suitable nodes
    if len(opurtunity_of_attacks) >= 1:
        #sorting the chance of attacking in the dictionary from a high amount to a low one
        sort_chance_of_attacks = sorted(opurtunity_of_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
        for n in sort_chance_of_attacks:
            n_defenders = n[1]['enemy_troops']
            num_of_needed_troops = (int(-(-(beta*n_defenders)//1))+ attack_attemps-1) - n[1]['my_troops_layer1node']
            #if "num_of_needed_troops" becomes a number which isn't larger than zero I don't need to put any troops of node because I have enough troops
            if my_remaining_troops >= num_of_needed_troops:
                                        #if this condition isn't checked, it may raises and error about that "num_of_needed_troops" is zero or a negetive number
                if num_of_needed_troops > 0:
                    print (game.put_troop(n[0][0] , num_of_needed_troops))#put n troops on the best choice of attacking, which n has been rounded up to ensure that the attack will be successful!
                    my_remaining_troops -= num_of_needed_troops #it is here to update the troops that i have each time
                n[1]['attackon'] = True #it is written to use in the attack state
    #FINISH TASK1


    print(game.next_state()) #going to the next state




    #the second state! attacking!
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    
    if len(sort_chance_of_attacks) >= 1:
        for on in sort_chance_of_attacks: 
            if on[1]['attackon'] == True and game.get_owners()[str(on[0][1])] != my_id and game.get_number_of_troops()[str(on[0][0])] > 1:
                print (game.attack(on[0][0] , on[0][1] , beta , VARS['moving_fraction']))           
    
    random_attacks = {}
    for mine in owner:
        if owner[mine] == my_id:
            for enemies in adjacents[mine]:
                if owner[str(enemies)] != -1 and owner[str(enemies)] != my_id:
                    enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)])
                    my_troops_layer1node = number_of_troops[str(my)]
                    attack_score = (my_troops_layer1node)/ enemy_troops_on_node
                    if attack_score > beta_plus:
                        random_attacks[(int(mine) , enemies)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False}
    random_attacks = sorted(random_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
    for each_attack in random_attacks:
        if game.get_number_of_troops()[str(each_attack[0][0])] > 1:
            print (game.attack(each_attack[0][0] , each_attack[0][1] , beta , 0.5))
    
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
        max_node = 0
        number_of_troops= game.get_number_of_troops()
        troops_in = 0
        for stra in strategic_nodes:
            if owner[str(stra)] == my_id and number_of_troops[str(stra)] > troops_in:
                troops_in = number_of_troops[str(stra)]
                max_node = stra
        print (game.fort(max_node , troops_in-1))
        flag = True
    