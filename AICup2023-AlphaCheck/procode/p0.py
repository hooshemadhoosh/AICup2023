VARS={'strategic_troops_number': 13.0, 'mytroops/enemytroops (beta)': 1.3, 'beta_plus': 1.6, 'TroopsTunnel': 1.0, 'number_of_attack_attemps': 6.0, 'troops_to_put_on_strategics': 1.0, 'moving_fraction': 0.7, 'number_of_defender_troops': 2.0, 'ValueOfTunnelNode': 10.0, 'ReainForce_strategics_everyround': 2.0}
flag = False
ListOfTunnels = []
good_list = [5, 6, 7]
father = {}
dp = {}
mark = {}
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
    #print('THIS IS ORDERED LIST OF TUNNELS ',result)
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

def findend (tunnel , owner , my_id):
    x = 0
    for n in range (1,len(tunnel)-1):
        if owner[str(tunnel[n])] != my_id and owner[str(tunnel[n])] != -1:
            x = n
            break
    return x

def findmove (tunel , end , number_of_troops , max_troops , sourcenode , detinationnode ):
    for eachnode in tunel[1:end]:
        if number_of_troops[str(eachnode)] > max_troops:
            max_troops = number_of_troops[str(eachnode)]
            sourcenode = eachnode
            detinationnode = tunel[0]
    return max_troops , sourcenode , detinationnode

def find_way_with_min_number_of_enemy(node, weigh_of_each_node, adj):
    dont_filled_node = [node]
    dp[str(node)] = [0, 0]
    mark[str(node)] = 1
    for j in range(0, 100):
        mini = 10000
        mini_id = -1
        mini_father = -1
        for i in dont_filled_node:
            for k in adj[str(i)]:
                if(mark[str(k)] == 0):
                    if(weigh_of_each_node[str(k)] + dp[str(i)][0] < dp[str(k)][0]):
                        dp[str(k)][1] = dp[str(i)][1] + 1
                        dp[str(k)][0] = min(weigh_of_each_node[str(k)] + dp[str(i)][0], dp[str(k)][0])
                        
                    if(dp[str(k)][0] < mini):
                        mini = dp[str(k)][0]
                        mini_id = k
                        mini_father = i
        if(mini_id == -1):
            break
        else:
            father[str(mini_id)] = mini_father
            mark[str(mini_id)] = 1
            dont_filled_node.append(mini_id)
            
            

def initializer(game):
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
    #print("Turn Number: ",game.get_turn_number())
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
                game.put_one_troop(j)
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
                #print(f"One Troop Added to Tunnel on node {node}")
                return
    
    #Reinforcement Of our Strategic Nodes
    for i in strategic_nodes:
        if owner[str(i)]==my_id and troops_of[str(i)]<VARS['strategic_troops_number']:
            game.put_one_troop(i)
            return
    
    # give 3 troops to all Tunnelnode  :)
    # for tunnel in ListOfTunnels:
    #     for node in tunnel:
    #         if(troops_of[str(node)] < VARS['TroopsTunnel'] and owner[str(node)] == my_id):
    #             game.put_one_troop(node)
    #             print(f"One Troop Added to Tunnel on node {node}")
    #             return
    

    
    
    return
    
    
 
def turn(game):
    
    global flag
    global good_list
#getting turn number
    my_id = game.get_player_id()['player_id']
    turn_number = game.get_turn_number()['turn_number']
    #print ("TURN NUMBER: ",turn_number)

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
            best_node_to_attack = dict_best_node_for_attak[i][0] / dict_best_node_for_attak[i][1]

            if(best_node_to_attack > maxi):
                maxi = best_node_to_attack
                max_id = int(i)
            
        
        if(max_id == -1):
            pass
        else:
            game.put_troop(max_id, my_remaining_troops) 
            my_remaining_troops = 0
            
#FINISH TASK -1        
            
            
#START TASK 0 :
# تقویت ضعیف ترین خونه ی استراتژیک در هر راند !!
    number_of_troops= game.get_number_of_troops()
    mini = 1000
    mini_id = -1

    for i in strategic_nodes:
        if owner[str(i)] == my_id and (number_of_troops[str(i)] + number_of_fort_troops[str(i)] < mini):
            mini = number_of_troops[str(i)] + number_of_fort_troops[str(i)]
            mini_id = i
    if(mini >= 50 and count_startegic_node != 3 and mini_id!=-1):
        count = 0 
        for j in adjacents[str(mini_id)]:
            if(owner[str(j)] == my_id and my_remaining_troops >= reinforcment_soldiers):
                my_remaining_troops -= reinforcment_soldiers
                print (game.put_troop(j, reinforcment_soldiers) , '\nTASK 0 IN DEPLOYMENT OF TROOPS IS DONE\n')
                number_of_troops[str(j)] += reinforcment_soldiers
                count += 1
            if(count == 3):
                break  
    else:
        if(count_startegic_node == 3):
            reinforcment_soldiers += 3
        if(mini_id != -1) and my_remaining_troops >= reinforcment_soldiers:
            my_remaining_troops -= reinforcment_soldiers
            print (game.put_troop(mini_id, reinforcment_soldiers ) , '\nTASK 0 IN DEPLOYMENT OF TROOPS IS DONE\n')
            number_of_troops[str(mini_id)] += reinforcment_soldiers
        if(count_startegic_node == 3):
            reinforcment_soldiers -= 3
#FINISH TASK 0


#START TASK 1
    for enemy in strategic_nodes:  
        if owner[str(enemy)] != my_id:
            enemy_troops_on_node = number_of_troops[str(enemy)] + number_of_fort_troops[str(enemy)] #getting the number of enemy troops on the strategic node
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
                    game.put_troop(n[0][0] , num_of_needed_troops)
                    my_remaining_troops -= num_of_needed_troops 
                    number_of_troops[str(n[0][0])] += num_of_needed_troops
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
                    enemy_troops += number_of_troops[str(enemy_adj)] + number_of_fort_troops[str(enemy_adj)]
            defend_planets[str(m)] = enemy_troops/my_planet_troops
    
    defend_planets = dict(sorted(defend_planets.items() , key  = lambda u : u[1] , reverse = True))
    for defend in defend_planets:
        if my_remaining_troops >= defender_troops:
            my_remaining_troops -= defender_troops
            number_of_troops[defend] += defender_troops
            game.put_troop(int(defend) , defender_troops)
            print ('TASK 2 IN DEPLOYMENT OF TROOPS IS DONE')
#FINISH TASK2

#START TASK 3
    owner = game.get_owners()
    #Opening Tunnel
    open_tunnel = []  #Contains items like [from attack, to attack, our strategic node, check attack!]
    for tunnel in ListOfTunnels:
        if not is_tunnel_activated(tunnel,owner,my_id):
            for i in range(1,len(tunnel)):
                if owner[str(tunnel[i])]!=my_id and owner[str(tunnel[i-1])]==my_id:
                    x= [tunnel[i-1],tunnel[i],tunnel[0], False] 
                    open_tunnel.append(x)
                    break
    print ('open tunnel IS NOT sorted:' , open_tunnel)
    open_tunnel.sort(key=lambda x: number_of_troops[str(x[2])]+ number_of_fort_troops[str(x[2])])
    print ('open tunnel IS sorted',open_tunnel)
    for item in open_tunnel:
        needed_troops = (number_of_troops[str(item[1])] + number_of_fort_troops[str(item[1])])*beta+attack_attemps-1
        if (number_of_troops[str(item[0])] + my_remaining_troops) >= needed_troops:
            troops_to_put = int(needed_troops-number_of_troops[str(item[0])])
            if troops_to_put > 0:   
                my_remaining_troops-=troops_to_put
                number_of_troops[str(item[0])] += int(troops_to_put)
                game.put_troop(item[0] , int(troops_to_put))
            item[3] = True
            print ('\nTASK 3 IN DEPLOYMENT OF TROOPS IS DONE:', item , '\n')
#FINISH TASK 3

#START TASK 4

    owner = game.get_owners()
    attack_on_layer1 = []  #Stores cases in form of [attacker node,target node]
    for enemy_stra in enemy_best_strategic:
        sorted_layer1 = [node for node in adjacents[str(enemy_stra)] if owner[str(node)]!=my_id]
        sorted_layer1.sort(key= lambda x: number_of_troops[str(x)]+ number_of_fort_troops[str(x)])
        for layer1_node in sorted_layer1:
            sorted_layer2 = [node for node in adjacents[str(layer1_node)] if owner[str(node)]==my_id]
            if len(sorted_layer2)==0:   continue
            sorted_layer2.sort(key= lambda x: number_of_troops[str(x)],reverse=True)
            for layer2_node in sorted_layer2:
                needed_troops = (number_of_troops[str(layer1_node)] + number_of_fort_troops[str(layer1_node)])*beta+attack_attemps-1
                if number_of_troops[str(layer2_node)]+my_remaining_troops>=needed_troops:
                    troops_to_put = int(needed_troops-number_of_troops[str(layer2_node)])
                    if troops_to_put > 0:   
                        my_remaining_troops-=troops_to_put
                        number_of_troops[str(layer2_node)] += int(troops_to_put)
                        print (game.put_troop(layer2_node , int(troops_to_put)), '\n TASK 4 IN DEPLOYMENT OF TROOPS IS DONE!\n')
                        attack_on_layer1.append([layer2_node,layer1_node])
                        break
#FINISH TASK 4
# Start task 5 
    if(turn_number > 162):
        owner = game.get_owners()
        x = 0
        while(my_remaining_troops > 2 and x < 100):
            x += 1
            for i in owner.keys():
                if(owner[str(i)] == -1):
                    game.put_troop(i, 3)
                    my_remaining_troops -= 3
                    owner[str(i)] = my_id
                    break
        x = 0
        while(my_remaining_troops > 0 and x < 100):
            x += 1
            for i in owner.keys():
                if(owner[str(i)] == my_id):
                    game.put_troop(i, 1)
                    my_remaining_troops -= 1
                    break
                

    game.next_state() #going to the next state
#The second state! attacking!---------------------------------------------------------------------------
# Start Task -1 :
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    node = "-1"
    
    for i in strategic_nodes:
        if(owner[str(i)] == my_id and number_of_troops[str(i)] > 48):

            node = str(i)
            weigh_of_each_node = {}
            dp.clear()
            mark.clear()
            father.clear()
            for i in owner.keys():
                if(owner[str(i)] != my_id and owner[str(i)] != -1):
                    weigh_of_each_node[str(i)] = number_of_troops[str(i)] + number_of_fort_troops[str(i)]
                dp[str(i)] = [10000, 0]
                mark[str(i)] = 0
                if(owner[str(i)] == my_id):
                    weigh_of_each_node[str(i)] = 0 
                if(owner[str(i)] == -1 or owner[str(i)] == my_id):
                    mark[str(i)] = 1
            
            
            
            father[str(node)] = -1
            find_way_with_min_number_of_enemy(node, weigh_of_each_node, adjacents)
            mini = 100000
            mini_id = -1
            for i in strategic_nodes:
                if(owner[str(i)] != my_id and dp[str(i)][0] != 10000 and dp[str(i)][0] < mini):
                    mini = dp[str(i)][0]
                    mini_id = i
            if(mini_id == -1):
                maxi = 0
                max_id = -1
                for i in owner.keys():
                    if(dp[str(i)][0] + dp[str(i)][1] <= 20 and owner[str(i)] != my_id and maxi <= dp[str(i)][0] + dp[str(i)][1]):
                        maxi = dp[str(i)][0] + dp[str(i)][1]
                        max_id = i

                way = []
                x = 0
                while(x < 100 and max_id != -1):
                    x +=1
                    way.append(max_id)
                    max_id = father[str(max_id)]   
                way.reverse()     
                if(len(way) >= 2):
                    game.attack(way[0], way[1], VARS['beta_plus'], 0.5)
                    for i in range(1, len(way) - 1):
                        if (number_of_fort_troops[str(way[i + 1])]+number_of_troops[str(way[i + 1])])*beta>=number_of_troops[str(way[i])] or number_of_troops[str(way[i])]<2 :    break
                        game.attack(way[i], way[i + 1], VARS['mytroops/enemytroops (beta)'], VARS['moving_fraction'])
                    

            else:
                x = 0
                way = []
                while(x < 100 and mini_id != -1):
                    x += 1  
                    way.append(mini_id)
                    mini_id = father[str(mini_id)]
                way.reverse()
                if(len(way) >= 2):
                    game.attack(way[0], way[1], VARS['beta_plus'], 0.5)
                    for i in range(1, len(way) - 1):
                        if (number_of_fort_troops[str(way[i + 1])]+number_of_troops[str(way[i + 1])])*beta>=number_of_troops[str(way[i])] or number_of_troops[str(way[i])]<2 :    break
                        game.attack(way[i], way[i + 1], VARS['mytroops/enemytroops (beta)'], VARS['moving_fraction'])

            owner = game.get_owners()
            number_of_troops= game.get_number_of_troops()
            number_of_fort_troops = game.get_number_of_fort_troops()            
                
               



# Finish Task -1 :)     
                
#START TASK0
    if(count_startegic_node == 3 and max_id != -1 and turn_number > 126):
        #my_remaining_troops

            near_startegic = 0
            for i in adjacents[str(max_id)]:
                if i in strategic_nodes and owner[str(i)]!=my_id:
                    near_startegic = i
                    break
            game.attack(max_id, near_startegic,beta, 0.5)
    
        
#FINISH TASK 0 
    
#START TASK 1 AND 2
    else:
        if sort_chance_of_attacks!=-1 and len(sort_chance_of_attacks) >= 1:
            for on in sort_chance_of_attacks: 
                if on[1]['attackon'] and owner[str(on[0][1])] != my_id and game.get_number_of_troops()[str(on[0][0])] > 1:
                    if on[0][0] in strategic_nodes:
                        if game.attack(on[0][0] , on[0][1] , beta , 0.5)['won'] == 1:
                            owner[str(on[0][1])] = my_id
                        print('TASK 1 AND 2 IN ATTACK IS DONE \n')
                    else:
                        if game.attack(on[0][0] , on[0][1] , beta , moving_fraction)['won'] == 1:
                            owner[str(on[0][1])] = my_id
                        print ('TASK 1 AND 2 IN ATTACK IS DONE \n')
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
        if each_attack[3] and owner[str(each_attack[1])] != my_id and owner[str(each_attack[1])] != -1 and game.get_number_of_troops()[str(each_attack[0])]>1:
            if str(each_attack[1]) in adjacents[str(each_attack[0])]: 
                if game.attack(each_attack[0],each_attack[1],beta,1-moving_fraction)['won'] == 1:
                    owner[str(each_attack[1])] = my_id
                print ('\n TASK 3 IN ATTACK IS DONE\n')

#FINISH TASK 3

#START TASK 4
    for case in attack_on_layer1:   
        if owner[str(case[1])]!=my_id and owner[str(case[1])]!=-1 and owner[str(case[0])]==my_id and game.get_number_of_troops()[str(case[0])]>1:  
            if game.attack(case[0],case[1],beta,1-moving_fraction)['won'] == 1:
                owner[str(case[1])] = my_id
            print ('\n TASK 4 IN ATTACK STATE IS DONE\n')
#FINISH TASK 4
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
#START TASK 5 :
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1): 
                    for k in adjacents[str(j)]:
                        if(owner[str(k)] == my_id and (str(k) in strategic_nodes) and number_of_troops[str(k)] >= beta_plus * (number_of_troops[str(j)] + number_of_fort_troops[str(j)]) and number_of_troops[str(k)] >= 2):
                            print (game.attack(k, j, beta_plus, (1 - moving_fraction)) , '\n TASK 5 IN ATTACK STATE IS DONE\n')
                            
                        elif(owner[str(k)] == my_id and number_of_troops[str(k)] >= (beta * (number_of_troops[str(j)] + number_of_fort_troops[str(j)])) and number_of_troops[str(k)] >= 2):
                            print (game.attack(k, j, beta,  1-moving_fraction) , '\n TASK 5 IN ATTACK STATE IS DONE \n')
                        owner = game.get_owners()
                        number_of_troops= game.get_number_of_troops()
                        number_of_fort_troops = game.get_number_of_fort_troops()
                        if(owner[str(j)] == my_id):
                            break

                        

#FINISH TASK 5 
    owner = game.get_owners()
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
# Start task 6:
    for i in owner:
        if(owner[str(i)] == my_id and (str(i) in strategic_nodes)and number_of_troops[str(i)]>1):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1 and (1<=number_of_troops[str(j)]+number_of_fort_troops[str(j)] <=2)):
                    print (game.attack(i, j, 4.5 , 1-moving_fraction) , '\nTASK 6 IS DONe \n')
                    owner = game.get_owners()
                    number_of_troops= game.get_number_of_troops()
                    number_of_fort_troops = game.get_number_of_fort_troops()
        elif(owner[str(i)] == my_id and number_of_troops[str(i)]>1):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1 ):
                    print (game.attack(i, j, 3.5 , 0.3) , '\n TASK 6 IS DONE')
                    owner = game.get_owners()
                    number_of_troops= game.get_number_of_troops()
                    number_of_fort_troops = game.get_number_of_fort_troops()

# Finish Task ;)
    game.next_state()
#THE THIRD STATE MOVING TROOPS-----------------------------------------------------------
    owner = game.get_owners()
    number_of_troops = game.get_number_of_troops()
    max_troops = 1
    sourcenode = -1
    destinationnode = -1
    for tunel in ListOfTunnels:
        if is_tunnel_activated (tunel , owner , my_id):
            for eachnode in tunel[1:-1]:
                if number_of_troops[str(eachnode)] > max_troops:
                    max_troops = number_of_troops[str(eachnode)]
                    sourcenode = eachnode
                    destinationnode = tunel[0]
        else:
            end = 0
            if owner[str(tunel[0])] == my_id:
                end = findend(tunel , owner , my_id)
                max_troops , sourcenode , destinationnode = findmove (tunel , end , number_of_troops , max_troops , sourcenode , destinationnode)
                if owner[str(tunel[-1])] == my_id: #when both end and start of the tunnel is for us!
                    tunel = list(reversed(tunel))
                    end = findend(tunel , owner , my_id)
                    max_troops , sourcenode , destinationnode = findmove (tunel , end , number_of_troops , max_troops , sourcenode , destinationnode)
            elif owner[str(tunel[0])] != my_id and owner[str(tunel[-1])] == my_id: #we have just end of the tunnel
                tunel = list(reversed(tunel))
                end = findend(tunel , owner , my_id)
                max_troops , sourcenode , destinationnode = findmove (tunel , end , number_of_troops , max_troops , sourcenode , destinationnode)

    if sourcenode != -1 and destinationnode != -1 and destinationnode in game.get_reachable(sourcenode)['reachable']:        print (game.move_troop(sourcenode , destinationnode , number_of_troops[str(sourcenode)]-1))

    game.next_state()


#THE LAST STATE FORTIFYING---------------------------------------------------------

    # Task 0:
    count_startegic_node = 0 
    owner = game.get_owners()
    number_of_troops = game.get_number_of_troops()

    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            count_startegic_node += 1
    if (count_startegic_node == 3 and flag == False):
        mini = 1000 
        mini_id = -1 
        for i in strategic_nodes:
            if(owner[str(i)] == my_id and 4 < number_of_troops[str(i)] < mini):
                mini = number_of_troops[str(i)]
                mini_id = i
        if mini_id!=-1:
            game.fort(mini_id, number_of_troops[str(mini_id)]-1)
            flag = True
    if (flag == False and turn_number > 162):
        maxi = -1
        max_id = -1
        for i in strategic_nodes :
            if(owner[str(i)] == my_id and number_of_troops[str(i)] > maxi):
                maxi = number_of_troops[str(i)]
                max_id = i 
        game.fort(max_id, number_of_troops[str(max_id)]-1)
        flag = True
              
    # finish Task0 :)

    return