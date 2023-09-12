import random
from src.game import Game
VARS = {"strategic_troops_number":8 , "mytroops/enemytroops (beta)" : 1.05 , "beta_plus": 1.5, "TroopsTunnel" : 1 , "number_of_attack_attemps" : 3 , "troops_to_put_on_strategics" : 3 , "moving_fraction" : 0.9 , "number_of_defender_troops" : 2,"ValueOfTunnelNode":10 , "ReainForce_strategics_everyround" : 2}
flag = False
ListOfTunnels = []
good_list = [4, 5, 6]

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

def is_tunnel_activated(TunnelList,owner,my_id):
    result = True
    for i in TunnelList[:-1]:
        if owner[str(i)]!=my_id:
            result=False
            break
    return result

def number_of_tunnel(node,owner,my_id):
    global ListOfTunnels
    result= -1
    for i in range(len(ListOfTunnels)):
        if is_tunnel_activated(ListOfTunnels[i],owner,my_id) and ListOfTunnels[i][-2]==node and owner[str(node)]==my_id:
            result = i
            break
    return result

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
        elif (owner[str(i)]!=-1) and (i not in enemy_best_strategic):
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
    # for tunnel in ListOfTunnels:
    #     for node in tunnel:
    #         if(troops_of[str(node)] < VARS['TroopsTunnel'] and owner[str(node)] == my_id):
    #             game.put_one_troop(node)
    #             print(f"One Troop Added to Tunnel on node {node}")
    #             return
    

    
    
    return
    
    
 
def turn(game: Game):
    
    global flag
#getting turn number
    my_id = game.get_player_id()['player_id']
    turn_number = game.get_turn_number()['turn_number']
    print ("TURN NUMBER: ",turn_number)

#VARIABLES
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
    defender_troops = VARS["number_of_defender_troops"]
    sort_chance_of_attacks = -1
    reinforcment_soldiers = VARS['ReainForce_strategics_everyround']
    moving_fraction = VARS['moving_fraction']
    my_best_strategic  = []
    enemy_best_strategic = []
    for i in strategic_nodes:
        if (owner[str(i)] == my_id) and (i not in my_best_strategic):
            my_best_strategic.append(i)
        elif (owner[str(i)]!=-1) and (i not in enemy_best_strategic):
            enemy_best_strategic.append(i)
#The first state! DEPLOYMENT OF TROOPS!---------------------------------------------------------------------------

#START TASK -1
    # اگه سه تا استراتژیک داشتیم و یه همسایه از استراتژیک داشتیم میایم
    # میایم هرچی سرباز داریم میریزم توی همسایه استراتژیکی ازش  به اونی که نداریم اتک میدیدم !


    count_startegic_node = 0
    maxi = -1
    max_id = -1

    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            count_startegic_node += 1
    
    if(count_startegic_node == 3 and turn_number > 126):

        dict_best_node_for_attak = {}
        for i in strategic_nodes:
            if(owner[str(i)] != my_id):
                for j in adjacents[str(i)]:
                    if(owner[str(j)] == my_id or owner[str(j)] == -1):
                        dict_best_node_for_attak[str(j)] = [number_of_troops[str(j)], number_of_troops[str(i)] + number_of_fort_troops[str(i)]]
                        
        for i in dict_best_node_for_attak:
            best_node_to_attack = dict_best_node_for_attak[str(i)][0] / dict_best_node_for_attak[str(i)][1]

            if(best_node_to_attack > maxi):
                maxi = best_node_to_attack
                max_id = i
            
        
        if(max_id == -1):
            pass
        else:
            #my_remaining_troops
            # my_remaining_troops = 0
            print (game.put_troop(max_id, my_remaining_troops) , 
                   'TASK -1 IS DONE: All troops are deployed to get the fourth strategic node!\n')
#FINISH TASK -1        
            
            
#START TASK 0 :
# تقویت ضعیف ترین خونه ی استراتژیک در هر راند !!

    mini = 1000
    mini_id = -1
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    my_remaining_troops = game.get_number_of_troops_to_put()['number_of_troops']
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            if(number_of_troops[str(i)] + number_of_fort_troops[str(i)] < mini):
                mini = number_of_troops[str(i)] + number_of_fort_troops[str(i)]
                mini_id = i
    if(mini_id != -1) and my_remaining_troops >= reinforcment_soldiers:
        my_remaining_troops -= reinforcment_soldiers
        print (game.put_troop(mini_id, reinforcment_soldiers ), 'TASK 0 IN DEPLOYMENT OF TROOPS IS DONE\n')
#FINISH TASK 0



#START TASK 1
    for enemy in strategic_nodes:  
        if owner[str(enemy)] != my_id:
            enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)]) #getting the number of enemy troops on the strategic node
            for my in adjacents[str(enemy)]:    
                if owner[str(my)] == my_id:
                    my_troops_layer1node = number_of_troops[str(my)]  
                    my_troops_on_layer1 = my_troops_layer1node
                    tunnel_number = number_of_tunnel(my,owner,my_id)            
                    if tunnel_number!=-1:   my_troops_on_layer1*=VARS['ValueOfTunnelNode']
                    attack_score = (my_remaining_troops-attack_attemps + my_troops_on_layer1)/enemy_troops_on_node
                    if attack_score > beta: 
                        opurtunity_of_attacks [(my , enemy)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False,"number_of_tunnel":tunnel_number}

    #start putting troops on suitable nodes
    if len(opurtunity_of_attacks) >= 1:
        #sorting the chance of attacking in the dictionary from a high amount to a low one
        sort_chance_of_attacks = sorted(opurtunity_of_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
        for n in sort_chance_of_attacks:
            n_defenders = n[1]['enemy_troops']
            num_of_needed_troops = (int(-(-(beta*n_defenders)//1))+ attack_attemps-1) - n[1]['my_troops_layer1node']
            if my_remaining_troops >= num_of_needed_troops:
                if num_of_needed_troops > 0:
                    print (game.put_troop(n[0][0] , num_of_needed_troops))
                    my_remaining_troops -= num_of_needed_troops 
                n[1]['attackon'] = True 
                print ('TASK 1 IN DEPLOYMENT OF TROOPS IS DONE: Attack is on now for planet %d' %n[0][0] , 'to attack to:' , n[0][1] , '\n')
#FINISH TASK1


#START TASK2
    defend_planets = {}
    for m in strategic_nodes:
        if owner[str(m)] == my_id:
            my_planet_troops = number_of_troops[str(m)] + number_of_fort_troops[str(m)]
            enemy_troops = 0
            for enemy_adj in adjacents[str(m)]:
                if owner[str(enemy_adj)] != my_id:
                    enemy_troops += number_of_troops[str(enemy_adj)]
            defend_planets[str(m)] = enemy_troops/my_planet_troops
    
    defend_planets = dict(sorted(defend_planets.items() , key  = lambda u : u[1] , reverse = True))
    for defend in defend_planets:
        print ('number of my troops is:' , my_remaining_troops)
        print ('server says the number of my troops are: ' , game.get_number_of_troops_to_put()['number_of_troops'])
        if my_remaining_troops >= defender_troops:
            my_remaining_troops -= defender_troops
            print (game.put_troop(int(defend) , defender_troops), '2 SOLDIERS are deployed on %d node' %int(defend) )
#FINISH TASK2

#START TASK 3
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    
    #Opening Tunnel
    open_tunnel = []  #Contains items like (from attack, to attack, our strategic node, check attack!)
    for tunnel in ListOfTunnels:
        if not is_tunnel_activated(tunnel,owner,my_id):
            for i in range(1,len(tunnel)):
                if owner[str(tunnel[i])]!=my_id and owner[str(tunnel[i-1])]==my_id:
                    x= [tunnel[i-1],tunnel[i],tunnel[0], False] #باید چک کنم ببینم در حالت لیست هم درست مرتب سازی میکنه یا گند کاری میشه
                    open_tunnel.append(x)
                    break
    print ('open tunnel IS NOT sorted:' , open_tunnel)
    open_tunnel.sort(key=lambda x: game.get_number_of_troops()[str(x[2])]+game.get_number_of_fort_troops()[str(x[2])]) #باید چک کنم ببینم در حالت لیست هم درست مرتب سازی میکنه یا گند کاری میشه
    print ('open tunnel IS sorted',open_tunnel)
    for item in open_tunnel:
        needed_troops = (game.get_number_of_troops()[str(item[1])] + game.get_number_of_fort_troops()[str(item[1])])*beta+attack_attemps-1
        my_remaining_troops = game.get_number_of_troops_to_put() ['number_of_troops']
        if game.get_number_of_troops()[str(item[0])]+my_remaining_troops>=needed_troops:
            troops_to_put = int(needed_troops-game.get_number_of_troops()[str(item[0])])
            if troops_to_put > 0:   
                my_remaining_troops-=troops_to_put
                print (game.put_troop(item[0] , int(troops_to_put)))
            item[3] = True
            print ('TASK 3 IN DEPLOYMENT OF TROOPS IS DONE:', item)
#FINISH TASK 3

#START TASK 4

    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()

    attack_on_layer1 = []  #Stores cases in form of [attacker node,target node]
    for enemy_stra in enemy_best_strategic:
        sorted_layer1 = [node for node in adjacents[str(enemy_stra)] if owner[str(node)]!=my_id]
        sorted_layer1.sort(key= lambda x: game.get_number_of_troops()[str(x)]+game.get_number_of_fort_troops()[str(x)])
        for layer1_node in sorted_layer1:
            sorted_layer2 = [node for node in adjacents[str(layer1_node)] if owner[str(node)]==my_id]
            if len(sorted_layer2)==0:   continue
            sorted_layer2.sort(key= lambda x: game.get_number_of_troops()[str(x)],reverse=True)
            for layer2_node in sorted_layer2:
                needed_troops = (game.get_number_of_troops()[str(layer1_node)] + number_of_fort_troops[str(layer1_node)])*beta+attack_attemps-1
                if game.get_number_of_troops()[str(layer2_node)]+my_remaining_troops>=needed_troops:
                    troops_to_put = int(needed_troops-game.get_number_of_troops()[str(layer2_node)])
                    if troops_to_put > 0:   
                        my_remaining_troops-=troops_to_put
                        print (game.put_troop(layer2_node , int(troops_to_put)))
                        attack_on_layer1.append([layer2_node,layer1_node])
                        break
#FINISH TASK 4

    print(game.next_state()) #going to the next state
#The second state! attacking!---------------------------------------------------------------------------
    
#START TASK0
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    if(count_startegic_node == 3 and max_id != -1 and turn_number > 126):
        #my_remaining_troops

            near_startegic = 0
            for i in adjacents[str(max_id)]:
                if i in strategic_nodes:
                    near_startegic = i
                    break
            print (game.attack(max_id, near_startegic,beta, 0.5) , 'Attack for geting the fourth node!')
#FINISH TASK 0 
    
#START TASK 1 AND 2
    else:
        if sort_chance_of_attacks!=-1 and len(sort_chance_of_attacks) >= 1:
            for on in sort_chance_of_attacks: 
                if on[1]['attackon'] and game.get_owners()[str(on[0][1])] != my_id and game.get_number_of_troops()[str(on[0][0])] > 1:
                    print (game.attack(on[0][0] , on[0][1] , beta , moving_fraction), 'I attacked from' , str(n[0][0]) , 'to the' , str(n[0][1]))           
#FINISH TASK 1 AND 2

    #   owner = game.get_owners()
    #   random_attacks = {}
    #   for mine in owner:
    #       if owner[mine] == my_id:
    #           for enemies in adjacents[mine]:
    #               if owner[str(enemies)] != -1 and owner[str(enemies)] != my_id:
    #                   enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)])
    #                   my_troops_layer1node = number_of_troops[str(my)]
    #                   attack_score = (my_troops_layer1node)/ enemy_troops_on_node
    #                   if attack_score > beta_plus:
    #                       random_attacks[(int(mine) , enemies)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False}
    #   random_attacks = sorted(random_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
    #   for each_attack in random_attacks:
    #       if game.get_number_of_troops()[str(each_attack[0][0])] > 1:
    #           print (game.attack(each_attack[0][0] , each_attack[0][1] , beta , 0.5))

#START TASK 3
    for each_attack in open_tunnel:
        if each_attack[3] and game.get_owners()[str(each_attack[1])] != my_id and game.get_owners()[str(each_attack[1])] != -1 and game.get_number_of_troops()[str(each_attack[0])]>1:
            print ('TASK 3 IN ATTACKING IS DONE','MY ID IS:',my_id , 'THE OWNER OF TARGET ID IS:' , game.get_owners()[str(each_attack[1])] , 'MY PLANET OWNER ID IS:',  game.get_owners()[str(each_attack[0])])
            print (game.attack(each_attack[0],each_attack[1],beta,1-moving_fraction))
#FINISH TASK 3

#START TASK 4
    for case in attack_on_layer1:   
        if game.get_owners()[str(case[1])]!=my_id and game.get_owners()[str(case[1])]!=-1 and game.get_owners()[str(case[0])]==my_id and game.get_number_of_troops()[str(case[0])]>1:  
            print ('TASK 4 IN ATTACKING IS DONE','MY ID IS:', game.get_owners()[str(my_id)] , 'THE OWNER OF TARGET ID IS:' , game.get_owners()[str(case[1])] , 'MY PLANET OWNER ID IS:',  game.get_owners()[str(case[0])]) 
            print(game.attack(case[0],case[1],beta,moving_fraction),"ATTACK ON LAYER1")
#FINISH TASK 4
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
#START TASK 5 :
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1): 
                    for k in adjacents[str(j)]:
                        if(owner[str(k)] == my_id and (k in strategic_nodes) and number_of_troops[str(k)] >= beta_plus * (number_of_troops[str(j)] + number_of_fort_troops[str(j)]) and number_of_troops[str(k)] >= 2):
                            game.attack(k, j, beta_plus, (1 - moving_fraction))
                            
                        elif(owner[str(k)] == my_id and number_of_troops[str(k)] >= (beta * (number_of_troops[str(j)] + number_of_fort_troops[str(j)])) and number_of_troops[str(k)] >= 2):
                            game.attack(k, j, beta,  moving_fraction)
                        owner = game.get_owners()
                        number_of_troops= game.get_number_of_troops()
                        number_of_fort_troops = game.get_number_of_fort_troops()
                        if(owner[str(j)] == my_id):
                            break

                        

#FINISH TASK 5 
    print(game.next_state())
#THE THIRD STATE MOVING TROOPS-----------------------------------------------------------

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
    if max_node!=destination:   print(game.move_troop(max_node, destination, 1))
    print(game.next_state())



    owner = game.get_owners()
    number_of_fort_troops = game.get_number_of_fort_troops()
    number_of_troops = game.get_number_of_troops()
#THE LAST STATE FORTIFYING---------------------------------------------------------

    # Task 0:
    count_startegic_node = 0 
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            count_startegic_node += 1
    if (count_startegic_node == 3 and flag == False):
        mini = 1000 
        mini_id = -1 
        for i in strategic_nodes:
            if(owner[str(i)] == my_id and number_of_troops[str(i)] < mini and number_of_troops[str(i)] > 4):
                mini = number_of_troops[str(i)]
                mini_id = i
        if mini_id!=-1:
            game.fort(mini_id, number_of_troops[str(mini_id)]-1)
            flag = True
    number_of_fort_troops = game.get_number_of_fort_troops()
    number_of_troops = game.get_number_of_troops()
    if (flag == False and turn_number>162):
        for i in strategic_nodes :
            if(owner[str(i)] == my_id and (number_of_troops[str(i)] in good_list)):
                game.fort(i, number_of_troops[str(i)]-1)
                flag = True
                break        
    # finish Task0 :)

    # get the node with the most troops that I own (default code)
    #if flag == False:
    #   max_node = 0
    #    number_of_troops= game.get_number_of_troops()
    #   troops_in = 0
     #   for stra in strategic_nodes:
    #      if owner[str(stra)] == my_id and number_of_troops[str(stra)] > troops_in:
    #           troops_in = number_of_troops[str(stra)]
    #           max_node = stra
    #   print (game.fort(max_node , troops_in-1))
    #   flag = True\\

    print(game.next_state()) #Finishing Turn

    return