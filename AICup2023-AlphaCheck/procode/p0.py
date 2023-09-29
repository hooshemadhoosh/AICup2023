VARS={'strategic_troops_number': 17.0, 'mytroops/enemytroops (beta)': 1.1, 'beta_plus': 1.2, 'TroopsTunnel': 1.0, 'number_of_attack_attemps': 3.0, 'troops_to_put_on_strategics': 1.0, 'moving_fraction': 0.9, 'number_of_defender_troops': 2.0, 'ValueOfTunnelNode': 10.0, 'ReainForce_strategics_everyround': 7.0}
flag = False
check_get_one = False
ListOfTunnels = []
good_list = [5, 6, 7]
father = {}
dp = {}
mark = {}
def Tunnel(start, dict_adj):
    dp = [10000] * (len(dict_adj))
    mark = [0] * (len(dict_adj))
    uplist = [-1] * (len(dict_adj))
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

def Tunnel_with_depth(start,dict_adj):
    dp = [10000] * (len(dict_adj))
    mark = [0] * (len(dict_adj))
    uplist = [-1] * (len(dict_adj))
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
    
    return (uplist,dp)

def uplist_to_list(uplist,node):
    Tunnel_listt = []
    x = node
    while(x != -1):
        Tunnel_listt.append(x)
        x = uplist[x]

    Tunnel_listt.reverse()
    return Tunnel_listt

def total_troops_of_way(way,troops_of,fort_troops_of):
    counter = 0
    for node in way[:-1]:
        counter+= troops_of[str(node)]+fort_troops_of[str(node)]
    return counter

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
            
def best_path(enemy_stra,adj,owner,my_id,troops_of,fort_troops_of):
    uplist,depth = Tunnel_with_depth(enemy_stra,adj)
    list_of_starts = [node for node in owner if owner[node]==my_id or owner[node]==-1]
    list_of_starts.sort(key=lambda node: depth[int(node)])
    list_of_ways = []
    for node in list_of_starts[:20]:
        way = uplist_to_list(uplist,int(node))
        for i in way[1:]:
            if owner[str(i)]==my_id or owner[str(i)] == -1:
                way = way[:way.index(i)+1]
                break
        if way not in list_of_ways:   list_of_ways.append(way)
    list_of_ways.sort(key= lambda way: total_troops_of_way(way,troops_of,fort_troops_of))
    list_of_ways = [my_way for my_way in list_of_ways if len(my_way)>1]
    if len(list_of_ways):   
        return (list_of_ways[0],total_troops_of_way(list_of_ways[0],troops_of,fort_troops_of))
    else:   return -1
    

def initializer(game):
    global ListOfTunnels 
    global VARS  
    strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    score = game.get_strategic_nodes()['score']
    strategic_nodes = list(zip(strategic_nodes, score))
    strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    strategic_nodes, score = list(zip(*strategic_nodes))
    owner = game.get_owners()
    my_id = game.get_player_id()['player_id']
    if my_id == 0:
        VARS={'strategic_troops_number': 17, 
              'mytroops/enemytroops (beta)': 1.01, 
              'beta_plus': 1.2, 
              'TroopsTunnel': 1, 
              'number_of_attack_attemps': 6, 
              'troops_to_put_on_strategics': 1, 
              'moving_fraction': 0.7, 
              'number_of_defender_troops': 2, 
              'ValueOfTunnelNode': 10, 
              'ReainForce_strategics_everyround': 8}
    elif my_id == 1:
        VARS={'strategic_troops_number': 17, 
              'mytroops/enemytroops (beta)': 1.01, 
              'beta_plus': 1.2, 
              'TroopsTunnel': 1, 
              'number_of_attack_attemps': 3, 
              'troops_to_put_on_strategics': 1, 
              'moving_fraction': 0.7, 
              'number_of_defender_troops': 2, 
              'ValueOfTunnelNode': 10, 
              'ReainForce_strategics_everyround': 8}
    elif my_id == 2:
        VARS={'strategic_troops_number': 17, 
              'mytroops/enemytroops (beta)': 1.05, 
              'beta_plus': 1.5, 
              'TroopsTunnel': 1, 
              'number_of_attack_attemps': 3, 
              'troops_to_put_on_strategics': 1, 
              'moving_fraction': 0.7, 
              'number_of_defender_troops': 2, 
              'ValueOfTunnelNode': 10, 
              'ReainForce_strategics_everyround': 8}
    adj = game.get_adj()
    troops_of = game.get_number_of_troops()
    remaining_troops = game.get_number_of_troops_to_put()['number_of_troops']
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
    #print("Turn Number: ",game.get_turn_number())
    #print(f"STRATEGIC NODES: {strategic_nodes}\n SCORE: {score}")

    #Filling Strategic Nodes...
    for i in strategic_nodes:
        if owner[str(i)] == -1:
            print(game.put_one_troop(i), "-- putting one troop on", i)
            return 
        
    #Filling Adjacents of Strategic nodes ordered
    strategic_nodes = list(strategic_nodes)
    strategic_nodes.sort(key=lambda node: len([i for i in adj[str(node)] if owner[str(i)]==my_id]))
    for i in strategic_nodes:
        if remaining_troops<= 2*VARS['strategic_troops_number']:    break
        ordered_adj = [k for k in adj[str(i)]]
        ordered_adj.sort(key= lambda adjacent: any([adjacent in tunn for tunn in ListOfTunnels]) , reverse=True)
        for j in ordered_adj:
            if owner[str(j)] == -1:
                game.put_one_troop(j)
                return
                   

    #Filling tunnels with troop
    for tunnel in ListOfTunnels:
        if remaining_troops<= 2*VARS['strategic_troops_number']:    break
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

    
    
    return
    
    
 
def turn(game):
    global check_get_one
    global VARS  
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
    beta = VARS["mytroops/enemytroops (beta)"]
    reinforcment_soldiers = VARS['ReainForce_strategics_everyround']
    moving_fraction = VARS['moving_fraction']
    larg_num = VARS['ValueOfTunnelNode']
    beta_plus = VARS['beta_plus']
    my_best_strategic  = []
    enemy_best_strategic = []
    for i in strategic_nodes:
        if (owner[str(i)] == my_id) and (i not in my_best_strategic):
            my_best_strategic.append(i)
        elif (owner[str(i)]!=-1) and (i not in enemy_best_strategic):
            enemy_best_strategic.append(i)
#The first state! DEPLOYMENT OF TROOPS!---------------------------------------------------------------------------
#Start Protocol 1
    fort_target = -1
    if my_id==1:
        if len(my_best_strategic)==2 and flag==False:
            fort_target = my_best_strategic[0]
            print (game.put_troop(my_best_strategic[1], my_remaining_troops) , '\nProtocol 1 IN DEPLOYMENT IS DONE')
            flag = True
    else:
        if len(my_best_strategic)==2 and flag==False:
            fort_target = my_best_strategic[0]
            flag = True
#Finish Protocol 1

            
#FINISH TASK -1        
    my_fort_target = fort_target
    dict_deployment = {}
    dict_all_defendings = {}
#START TASK 0 :
    number_of_troops= game.get_number_of_troops()
    mini = 1000
    mini_id = -1

    enemy_maxi = 1
    enemy_maxi_id = -1
    count_our_stra = 0
    for i in strategic_nodes:
        if owner[str(i)] == my_id and (number_of_troops[str(i)] + number_of_fort_troops[str(i)]) < mini:
            mini = number_of_troops[str(i)] + number_of_fort_troops[str(i)]
            mini_id = i
            count_our_stra += 1
            if mini_id == my_fort_target and flag:
                mini_id = -1
                mini = 1000
                my_fort_target = -2
        elif owner[str(i)] != my_id and number_of_troops[str(i)] > enemy_maxi:
            enemy_maxi = number_of_troops[str(i)]
            enemy_maxi_id = i

    my_remaining_troops = game.get_number_of_troops_to_put()['number_of_troops']
    if mini < 30 and enemy_maxi > 14 and count_our_stra < 3 and turn_number < 112 and my_remaining_troops > 0 and mini_id != -1:
        if my_remaining_troops > reinforcment_soldiers:
            game.put_troop(mini_id , reinforcment_soldiers)
            print('mini troops is runned')
            number_of_troops[str(mini_id)] += reinforcment_soldiers
            my_remaining_troops -= reinforcment_soldiers
        else:
            game.put_troop(mini_id , my_remaining_troops)
            number_of_troops[str(mini_id)] += my_remaining_troops
            my_remaining_troops = 0
    
    my_remaining_troops = game.get_number_of_troops_to_put()['number_of_troops']
    all_id = [0,1,2]
    all_id.remove(my_id)
    #example: {(enemy's node or attacker , my node or defender): {'fraction':1.2 , 'deployed?' : False , 'attack' : false}}
    #if deployed and attack = False, it means we don't have to put any troops
    #if deployed = False and attack = True, it means we can deploy troops to attack but for some reasons we didn't do this
    #if deployed and attack = True, it means we deployed troops on a node and we are ready to attack enemy node!
    maxi0 , maxid0 = 0 , -1
    maxi1 , maxid1 = 0 , -1
    for i in owner:
        if owner[i] == all_id[0] and number_of_troops[i] > maxi0:
            maxid0 = int(i)
            maxi0 = number_of_troops[i]
        elif owner[i] == all_id[1] and number_of_troops[i] > maxi1:
            maxi1 = number_of_troops[i]
            maxid1 = int(i)
    
    for stra in strategic_nodes:
        if owner[str(stra)] != all_id[0] and maxid0 != -1:
            dict_all_defendings[(maxid0 , stra)] = {'deployed' : False ,
                                                    'fraction' : (number_of_troops[str(maxid0)] + larg_num)/(number_of_troops[str(stra)] + number_of_fort_troops[str(stra)]),
                                                    'attack' : False,
                                                    'min num of needed troops' : (number_of_troops[str(maxid0)] + larg_num) - (number_of_troops[str(stra)] + number_of_fort_troops[str(stra)]),
                                                    'tunel' : -1}
        elif owner[str(stra)] != all_id[1] and maxid1 != -1:
            dict_all_defendings[(maxid1 , stra)] = {'deployed' : False ,
                                                    'fraction' : (number_of_troops[str(maxid1)] + larg_num)/(number_of_troops[str(stra)] + number_of_fort_troops[str(stra)]),
                                                    'attack' : False,
                                                    'min num of needed troops' : (number_of_troops[str(maxid1)] + larg_num) - (number_of_troops[str(stra)] + number_of_fort_troops[str(stra)]),
                                                    'tunel' : -1}
            
    dict_all_defendings = (sorted(dict_all_defendings.items() , key = lambda item: item[1]['fraction'] , reverse=True))
    for puttroop in dict_all_defendings:
        if owner[str(puttroop[0][1])] == my_id:
            dict_deployment[puttroop[0]] = puttroop[1]
#checking for attack on layer1 node 
    enemy_numbers = [1,2,3,4,5,6 ,7 ,8 ,9 ,10,11]
    my_numbers    = [4,5,7,8,9,10,11,12,14,15,17]
    for enemy in strategic_nodes:  
        if owner[str(enemy)] != my_id:
            enemy_troops_on_node = number_of_troops[str(enemy)] + number_of_fort_troops[str(enemy)] #getting the number of enemy troops on the strategic node
            for my in adjacents[str(enemy)]:
                min_needed_troops = 10000
                need_troops = 10000
                fraction = -1
                if enemy_troops_on_node in enemy_numbers:
                    min_needed_troops = my_numbers[enemy_troops_on_node-1] - number_of_troops[str(my)]
                else:
                    min_needed_troops = int(1.5*enemy_troops_on_node) + 1 - number_of_troops[str(my)]

                if owner[str(my)] == my_id or owner[str(my)] == -1:
                    if my_remaining_troops == min_needed_troops:
                        fraction = (min_needed_troops + number_of_troops[str(my)]) / enemy_troops_on_node
                        need_troops = my_remaining_troops
                    elif min_needed_troops < my_remaining_troops <= (min_needed_troops+ 3):
                        fraction = (my_remaining_troops + number_of_troops[str(my)]) / enemy_troops_on_node
                        need_troops = my_remaining_troops
                    elif my_remaining_troops > (min_needed_troops + number_of_troops[str(my)] + 3):
                        fraction = (min_needed_troops + number_of_troops[str(my)] + 3) / enemy_troops_on_node
                        need_troops = min_needed_troops + 3

                    if fraction >= 1.5:    fraction *= larg_num
                    if need_troops != 10000 and fraction != -1:
                        dict_deployment[(enemy , my)] = {'deployed' : False ,
                                                         'fraction' : fraction , 
                                                         'attack' : True ,
                                                         'min num of needed troops' : need_troops,
                                                         'tunel' : -1} 
    for enemy in strategic_nodes:
        fraction = -1
        min_needed_troops = 10000
        need_troops = 10000
        if owner[str(enemy)] != my_id:
            path = (best_path(enemy,adjacents,owner,my_id,number_of_troops,number_of_fort_troops))
            if path != -1:
                my = path[0][-1]
                enemy_troops_on_path = path[1]
                if enemy_troops_on_path in enemy_numbers:
                    min_needed_troops = my_numbers[enemy_troops_on_path-1] - number_of_troops[str(my)]
                else:
                    min_needed_troops = int(1.5*enemy_troops_on_path) + 1 - number_of_troops[str(my)]
                if my_remaining_troops == min_needed_troops:
                    fraction = (min_needed_troops + number_of_troops[str(my)]) / enemy_troops_on_path
                    need_troops = my_remaining_troops
                elif min_needed_troops < my_remaining_troops <= (min_needed_troops + 3):
                    need_troops = my_remaining_troops
                    fraction = (my_remaining_troops + number_of_troops[str(my)]) / enemy_troops_on_path
                elif my_remaining_troops > (min_needed_troops + number_of_troops[str(my)] + 3):
                    need_troops = min_needed_troops + 3
                    fraction = (min_needed_troops + number_of_troops[str(my)] + 3) / enemy_troops_on_path
                if fraction >= 1.5:    fraction*=larg_num
                if need_troops != 10000 and fraction != -1:
                    dict_deployment[(enemy , my)] = {'deployed' : False ,
                                                     'fraction' : fraction , 
                                                     'attack' : True ,
                                                     'min num of needed troops' : need_troops,
                                                     'tunel' : path[0]} 

#finish checking layer1 node
    
    deployment_list = sorted(dict_deployment.items() , key=lambda fra: fra[1]['fraction'] , reverse=True)

    for each_dep in deployment_list:
        if each_dep[1]['attack'] and my_remaining_troops >= each_dep[1]['min num of needed troops'] and 1.2 < each_dep[1]['fraction']:
            if each_dep[1]['min num of needed troops'] > 0:
                game.put_troop(each_dep[0][1] , each_dep[1]['min num of needed troops'])
                each_dep[1]['deployed'] = True
                my_remaining_troops -= each_dep[1]['min num of needed troops']
                number_of_troops[str(each_dep[0][1])] += each_dep[1]['min num of needed troops']
            else:
                each_dep[1]['deployed'] = True
        elif not each_dep[1]['attack'] and my_remaining_troops >= each_dep[1]['min num of needed troops'] and 1.2 < each_dep[1]['fraction']:
            if each_dep[1]['min num of needed troops']:
                game.put_troop(each_dep[0][1] ,each_dep[1]['min num of needed troops'])
                my_remaining_troops -= each_dep[1]['min num of needed troops']
                number_of_troops[str(each_dep[0][1])] += each_dep[1]['min num of needed troops']
            


#FINISH TASK 0

#START TASK 1
    if(check_get_one == False):
        check_get_one = True
        dict_mini_depth = {}
        for i in owner.keys():
            dict_mini_depth[str(i)] = 10000
        for i in strategic_nodes:
            uplist1,depth1 = Tunnel_with_depth(i, adjacents)
            for j in range(0, len(adjacents)):
                dict_mini_depth[str(j)] = min(dict_mini_depth[str(j)], depth1[j])
        maxi5 = 0
        maxi5_ = -1
        for j in dict_mini_depth.keys():
            if(dict_mini_depth[str(j)] > maxi5 and owner[str(j)] == -1):
                maxi5 = dict_mini_depth[str(j)]
                maxi5_ = int(j)
        if(my_remaining_troops > 0 and maxi5_!=-1):
            game.put_troop(maxi5_, 1)
            # print(maxi5_)
            my_remaining_troops -= 1 
    else:
        check_get_one = False
#FINISH TASK 1

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
                
    # Finish Task 5
    adj_of_stupednode = -1
    i1 = -1
    # Start 6 put_troops and -2 Attack 

    if(my_remaining_troops > 0):
        
        for i in strategic_nodes:
            if(adj_of_stupednode != -1):
                break
            if(owner[str(i)] != my_id and owner[str(i)] != -1 and number_of_troops[str(i)] >= 20):
                for j in adjacents[str(i)]:
                    if(owner[str(j)] == my_id):
                        adj_of_stupednode = j
                        i1 = i 
                        break
        
        for i in owner.keys():
            if(adj_of_stupednode != -1):
                break
            if(owner[str(i)] != my_id and owner[str(i)] != -1 and number_of_troops[str(i)] >= 20):
                for j in adjacents[str(i)]:
                    if(owner[str(j)] == my_id):
                        adj_of_stupednode = j
                        i1 = i 
                        break
        
        if(adj_of_stupednode != -1):
            game.put_troop(adj_of_stupednode, my_remaining_troops)
            my_remaining_troops = 0
    
    game.next_state() #going to the next state
    if(adj_of_stupednode != -1):
        game.attack(adj_of_stupednode, i1, 0.05, moving_fraction)
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
            mini_id1 = -1
            for i in strategic_nodes:
                if(owner[str(i)] != -1 and owner[str(i)] != my_id and dp[str(i)][0] != 10000 and dp[str(i)][0] < mini):
                    mini = dp[str(i)][0]
                    mini_id1 = i
            
            if(mini_id != -1):
                x = 0
                way = []
                while(x < 100 and mini_id1 != -1):
                    x += 1  
                    way.append(mini_id1)
                    mini_id1 = father[str(mini_id1)]
                way.reverse()
                if(len(way) >= 2):
                    if game.attack(way[0], way[1], VARS['beta_plus'], 0.5)['won'] == 1:
                        for i in range(1, len(way) - 1):
                            if (number_of_fort_troops[str(way[i + 1])]+number_of_troops[str(way[i + 1])])*beta>=number_of_troops[str(way[i])] or number_of_troops[str(way[i])]<2 :    break
                            if game.attack(way[i], way[i + 1], VARS['mytroops/enemytroops (beta)'], 0.9)['won'] != 1:   break
                            owner = game.get_owners()
                            number_of_troops= game.get_number_of_troops()
                            number_of_fort_troops = game.get_number_of_fort_troops() 

            owner = game.get_owners()
            number_of_troops= game.get_number_of_troops()
            number_of_fort_troops = game.get_number_of_fort_troops()            
                
               



# Finish Task -1 :)     
                
    origin = -1
    goal = -1
    
#START TASK 1 AND 2
    for attack in deployment_list:
        if attack[1]['attack'] and attack[1]['deployed'] and owner[str(attack[0][0])] != my_id and game.get_number_of_troops()[str(attack[0][1])]>=2:
            if attack[1]['tunel'] == -1:
                if attack[0][1] in strategic_nodes:
                    if game.attack(attack[0][1] , attack[0][0] , beta_plus , 0.5)['won'] == 1:
                        owner[str(attack[0][0])] = my_id
                else:
                    if game.attack(attack[0][1] , attack[0][0] , 0.5 , 0.9)['won'] == 1:
                        owner[str(attack[0][0])] = my_id
            else:
                way = attack[1]['tunel']
                way.reverse()
                for node in range(0, len(way)-1):
                    betta = 0.5
                    if owner[str(way[node])] == my_id and way[node] in strategic_nodes:
                        betta = 0.99
                    if owner[str(way[node+1])]==my_id or owner[str(way[node])]!=my_id:  break
                    if game.attack(way[node] , way[node+1] , betta , 0.99)['won'] == 1:
                        owner[str(way[node+1])] = my_id
                    elif way[0] in strategic_nodes:
                        goal = way[node]
                        origin = way[0] if node != 0 else -1
                        break
                else:
                    if way[0] in strategic_nodes:
                        goal = way[-1]
                        origin = way[0]
                        



    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
#START TASK 5 :
    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1): 
                    for k in adjacents[str(j)]: 
                        if(owner[str(k)] == my_id and k not in strategic_nodes and number_of_troops[str(k)] >= 2):
                            game.attack(k, j, 0.1, 0.6) , '\n TASK 5 IN ATTACK STATE IS DONE \n'
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
    opt_nums = [3,4,5,6]
    for i in owner:
        if(owner[str(i)] == my_id and number_of_troops[str(i)]>1 and int(i) not in strategic_nodes):
            for j in adjacents[str(i)]:
                if(owner[str(j)] != my_id and owner[str(j)] != -1 and number_of_troops[str(i)] in opt_nums):
                    if 1 <= number_of_troops[str(j)] + number_of_fort_troops[str(j)] <= 2:
                        game.attack(i, j, beta , 0.3)
                        owner = game.get_owners()
                        number_of_troops= game.get_number_of_troops()
                        number_of_fort_troops = game.get_number_of_fort_troops()
    game.next_state()
#THE THIRD STATE MOVING TROOPS-----------------------------------------------------------
    owner = game.get_owners()
    number_of_troops = game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    #START PROTOCOL 1

    if origin != -1 and goal != -1 and number_of_troops[str(goal)]>number_of_troops[str(origin)]+number_of_fort_troops[str(origin)]:
        moving_troops = (number_of_troops[str(goal)] - number_of_troops[str(origin)])//2
        if moving_troops > 0:
            game.move_troop(goal , origin , moving_troops)

    #FINISH PROTOCOL 1
    else:
        strategic_nodes = list(strategic_nodes)
        strategic_nodes.sort(key=lambda x: number_of_troops[str(x)]+number_of_fort_troops[str(x)])
        my_best_strategic = [node for node in strategic_nodes if owner[str(node)]==my_id]
        for node in my_best_strategic:
            reachable = [x for x in game.get_reachable(node)['reachable'] if x not in strategic_nodes]
            reachable.sort(key=lambda x: number_of_troops[str(x)],reverse=True)
            source = reachable[0] if len(reachable) else -1
            if source!=-1 and number_of_troops[str(source)]>3:
                game.move_troop(source , node , number_of_troops[str(source)]-1)
                break
        else:   #This part will run only when for loop Ends with no break
            for node in my_best_strategic:
                reachable = [x for x in game.get_reachable(node)['reachable'] if x in strategic_nodes and x!=node]
                reachable.sort(key=lambda x: number_of_troops[str(x)],reverse=True)
                source = reachable[0] if len(reachable) else -1
                if source!=-1 and number_of_troops[str(source)]>10 and number_of_fort_troops[str(source)]+number_of_troops[str(source)]>number_of_fort_troops[str(node)]+number_of_troops[str(node)]:
                    troops = (number_of_troops[str(source)]-number_of_troops[str(node)])//2
                    if troops>0:    game.move_troop(source , node , troops)
                    break



    game.next_state()
#THE LAST STATE FORTIFYING---------------------------------------------------------
    #Start Protocol 1
    number_of_troops = game.get_number_of_troops()
    if fort_target!=-1 and flag==True:
        game.fort(fort_target, number_of_troops[str(fort_target)]-1)
        fort_target=-1
    #Finish Protocol 1
    # Task 0:
    count_startegic_node = 0 
    owner = game.get_owners()
    number_of_troops = game.get_number_of_troops()

    for i in strategic_nodes:
        if(owner[str(i)] == my_id):
            count_startegic_node += 1
    if (count_startegic_node == 3 and flag == False):
        mini = 1000 
        mini_id2 = -1 
        for i in strategic_nodes:
            if(owner[str(i)] == my_id and 4 < number_of_troops[str(i)] < mini):
                mini = number_of_troops[str(i)]
                mini_id2 = i
        if mini_id2!=-1:
            game.fort(mini_id2, number_of_troops[str(mini_id2)]-1)
            flag = True
    if (flag == False and turn_number > 162):
        maxi = -1
        max_id2 = -1
        for i in strategic_nodes :
            if(owner[str(i)] == my_id and number_of_troops[str(i)] > maxi):
                maxi = number_of_troops[str(i)]
                max_id2 = i 
        game.fort(max_id2, number_of_troops[str(max_id2)]-1)
        flag = True
              
    # finish Task0 :)


    return