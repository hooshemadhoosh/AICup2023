import random
from src.game import Game
VARS = {"strategic_troops_number":8 , "mytroops/enemytroops (beta)" : 1.2 , 'beta_plus': 1.5, "Troops" : 3}
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
        for i in dict_adj[str(point)]:
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

    # MAke Tunnel 
    my_best_strategic  = []
    enemy_best_strategic = []
    my_uplist = []
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            my_best_strategic.append(i)
        else:
            enemy_best_strategic.append(i)
        
    
    my_uplist1 = Tunnel(my_best_strategic[0], adj)
    
    dict_of_Tunnel_list = {}
    # Make tunnel from my strategtic to enemy strategic :)

    for i in enemy_best_strategic:

        Tunnel_listt = []
        x = i
        while(x != -1):
            Tunnel_listt.append(x)
            x = my_uplist1[x]
            
        Tunnel_listt.reverse()
        Tunnel_listt = Tunnel_listt[1:]
        dict_of_Tunnel_list[len(dict_of_Tunnel_list)] = Tunnel_listt
    #first Tunnel
    # first putting troop in Tunnelnode 

    for i in dict_of_Tunnel_list[0]:
        if(owner[str(i)] == -1):
            game.put_one_troop(i)
            return 

    # give 3 troops to all Tunnelnode  :)
    for i in dict_of_Tunnel_list[0]:
        if(troops_of[str(i)] < VARS['Troops'] and owner[str(i)] == my_id):
            game.put_one_troop(i)
            return
    #Second Tunnel
    # first putting troop in Tunnelnode 

    for i in dict_of_Tunnel_list[1]:
        if(owner[str(i)] == -1):
            game.put_one_troop(i)
            return 

    # give 3 troops to all Tunnelnode  :)
    for i in dict_of_Tunnel_list[1]:
        if(troops_of[str(i)] < VARS['Troops'] and owner[str(i)] == my_id):
            game.put_one_troop(i)
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
    opurtunity_of_attacks = {}
    beta = VARS["mytroops/enemytroops (beta)"]
    beta_plus = VARS["beta_plus"]

    for enemy in strategic_nodes:  
        enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)]) #getting the number of enemy troops on the strategic node
        if owner[str(enemy)] != my_id:
            for my in adjacents[str(enemy)]:
                if owner[str(my)] == my_id:
                    my_troops_layer1node = number_of_troops[str(my)]
                    attack_score = (my_remaining_troops-3 + my_troops_layer1node)/ enemy_troops_on_node
                    if attack_score > beta:
                        opurtunity_of_attacks [(my , enemy)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False}
                        #s is enemy node and node is my node  #the chance of attacking #the number of enemy troops on strategic node #the troops i have on layer1 before 


    #start putting troops on suitable nodes #جهت احتیاط این شرط رو گذاشتم که یه چند تا سربازی هم داشته باشیم تا جاهای دیگه به عنوان مدافع کار بذاریم!
    if len(opurtunity_of_attacks) >= 1 and my_remaining_troops > 2:
        #sorting the chance of attacking in the dictionary from a high amount to a low one
        sort_chance_of_attacks = sorted(opurtunity_of_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
        for n in sort_chance_of_attacks:
            n_defenders = n[1]['enemy_troops']
            num_of_needed_troops = (int(-(-(beta*n_defenders)//1))+2) - n[1]['my_troops_layer1node']
            if my_remaining_troops > num_of_needed_troops > 0 :
                print (game.put_troop(n[0][0] , num_of_needed_troops))#put n troops on the best choice of attacking, which n has been rounded up to ensure that the attack will be successful!
                n[1]['attackon'] = True
                my_remaining_troops -= num_of_needed_troops
            else:
                n[1]['attackon'] = True
    #if there isn't any suitable node to put troops on we should put our troops on the nodes that we have now or the nodes which no one own them randomly!
    list_of_my_strategics = [] 
    for x in strategic_nodes:
        if owner[str(x)] == my_id and game.get_number_of_troops_to_put()['number_of_troops'] > 2:
            list_of_my_strategics.append(int(x))
    while game.get_number_of_troops_to_put()['number_of_troops'] > 2:
        print (game.put_troop(random.choice(list_of_my_strategics), random.choice([2,3])))

    print(game.next_state()) #going to the next state




    #the second state! attacking!
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    
    if len(sort_chance_of_attacks) >= 1:
        for on in sort_chance_of_attacks:
            if on[1]['attackon'] == True and game.get_owners()[str(on[0][1])] != my_id and game.get_number_of_troops()[str(on[0][0])] > 1:
                print (game.attack(on[0][0] , on[0][1] , beta , 0.7))
    
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
    owner = game.get_owners()
    # get the node with the most troops that I own (default code)
    
            
    if flag == False:
        max_node = 0
        number_of_troops= game.get_number_of_troops()
        troops_in = 0
        for stra in strategic_nodes:
            if owner[str(stra)] == my_id and number_of_troops[str(stra)] > troops_in:
                troops_in = number_of_troops[str(stra)]
                max_node = stra
        print (game.fort(stra , troops_in-1))
        flag = True
    