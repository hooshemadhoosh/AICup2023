import random
from src.game import Game
VARS = {"strategic_troops_number":8 , "mytroops/enemytroops (beta)" : 1.2 , "beta_plus": 1.5, "TroopsTunnel" : 3 , "number_of_attack_attemps" : 3 , "troops_to_put_on_strategics" : 3}
flag = False

ListOfTunnels = []
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
        if owner[str(enemy)] != my_id:
            enemy_troops_on_node = int(number_of_troops[str(enemy)]) + int(number_of_fort_troops[str(enemy)]) #getting the number of enemy troops on the strategic node
            for my in adjacents[str(enemy)]:    
                if owner[str(my)] == my_id:
                    my_troops_layer1node = number_of_troops[str(my)]
                                                        #این 3 رو برای این کم کردم که بعد میخوام دوتا اضافه کنم سرباز داشته باشیم و ارور نگیریم ولی نمیدونم چرا همون دو نذاشتم باشه و سه گذاشتم یادم نمیاد..
                    attack_score = (my_remaining_troops-3 + my_troops_layer1node)/enemy_troops_on_node
                    if attack_score > beta: #اگر امتیاز حمله از بتا بزرگ تر بود میاد به دیکشنری با مشخصات مورد نیاز اضافه میکنه در غیر این صورت که نیازی نیست این کار رو بکنه چون سرباز نداریم
                        opurtunity_of_attacks [(my , enemy)] = {'attack_score':attack_score , 'enemy_troops' : enemy_troops_on_node, 'my_troops_layer1node':my_troops_layer1node , 'attackon' : False}
                        #s is enemy node and node is my node  #the chance of attacking #the number of enemy troops on strategic node #the troops i have on layer1 before 
                                                #چرا کلید رو تاپل دادم؟ چون اگر هر کدوم از سیاره های خودمون یا اونارو میدادم تکراری توش پیدا میشد و حذف میکرد...

    #start putting troops on suitable nodes #جهت احتیاط این شرط رو گذاشتم که یه چند تا سربازی هم داشته باشیم تا جاهای دیگه به عنوان مدافع کار بذاریم!
    if len(opurtunity_of_attacks) >= 1:
        #sorting the chance of attacking in the dictionary from a high amount to a low one
        sort_chance_of_attacks = sorted(opurtunity_of_attacks.items(), key = lambda item: item[1]['attack_score'] , reverse=True)
        for n in sort_chance_of_attacks:
            n_defenders = n[1]['enemy_troops']
                                    #توضیح فرمول و مشکلش سر اینکه 5 تا سرباز تو خونه دشمن باشه! که میاد و دو بار حمله رو ادامه میده اما در بقیه حالات تقریبا میشه گفت همش سه بار حمله میکنه
            num_of_needed_troops = (int(-(-(beta*n_defenders)//1))+ VARS['number_of_attack_attemps']-1) - n[1]['my_troops_layer1node']
            #if "num_of_needed_troops" becomes a number which isn't larger than zero I don't need to put any troops of node because I have enough troops
            if my_remaining_troops >= num_of_needed_troops: #برای بهینه تر شدن این شرط ها نظری دارید؟
                                        #if this condition isn't checked, it may raises and error about that "num_of_needed_troops" is zero or a negetive number
                if num_of_needed_troops > 0:
                    print (game.put_troop(n[0][0] , num_of_needed_troops))#put n troops on the best choice of attacking, which n has been rounded up to ensure that the attack will be successful!
                    n[1]['attackon'] = True #it is written to use in the attack state
                    my_remaining_troops -= num_of_needed_troops #it is here to update the troops that i have each time
                else:  
                    n[1]['attackon'] = True
    #if there isn't any suitable node to put troops on we should put our troops on the strategic nodes
    list_of_my_strategics = [] #پیشنهاد: میشه این رو به یه دیکشنری تبدیل کرد که بیاد بر اساس تعداد سرباز موجود توش از کوچک به بزرگ مرتب بشه و سرباز های باقی مونده رو به سیاره هایی که کمترین سرباز رو دارند اضافه کنه
    for x in strategic_nodes:
        if owner[str(x)] == my_id:
            list_of_my_strategics.append(int(x))

    while my_remaining_troops > 2:
        my_remaining_troops -= VARS['troops_to_put_on_strategics']
        print (game.put_troop(random.choice(list_of_my_strategics[0]), VARS['troops_to_put_on_strategics']))

    print(game.next_state()) #going to the next state




    #the second state! attacking!
    number_of_troops= game.get_number_of_troops()
    number_of_fort_troops = game.get_number_of_fort_troops()
    
    if len(sort_chance_of_attacks) >= 1:
        for on in sort_chance_of_attacks:     #ممکنه به یه سیاره بخوایم دو بار حمله کنیم! و بار اول مال ما بشه...
            if on[1]['attackon'] == True and game.get_owners()[str(on[0][1])] != my_id and game.get_number_of_troops()[str(on[0][0])] > 1:
                print (game.attack(on[0][0] , on[0][1] , beta , 0.7))                      #تو همون دوبار حمله کردنه تعداد سرباز هامون کم میشه دیگه پس باید چکش کنیم
    
    random_attacks = {} #توضیح این بخش کد با پینت
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
        if game.get_number_of_troops()[each_attack[0][0]] > 1: #برای اینکه ممکنه چند بار یه سیاره ما به سیار های دیگه حمله کنه...
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
    