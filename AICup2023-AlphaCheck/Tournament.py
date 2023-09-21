import json
import os
from subprocess import Popen
import subprocess
from tqdm import tqdm, trange

BOX_NUMBER = 2
p0_address  = "procode//p0.py"
p1_address  = "procode//p1.py"
p2_address  = "procode//p2.py"
VARS={'strategic_troops_number':[9],
      'mytroops/enemytroops (beta)': [1.01,1.05,1.2], 
      'beta_plus':[1.2, 1.5, 1.8],
      'TroopsTunnel':[1,2],
      'number_of_attack_attemps': [3,6],
      'troops_to_put_on_strategics': [1.0] ,
      'moving_fraction':[0.7,0.8,0.9],
      'number_of_defender_troops':[2,3,4],
      'ValueOfTunnelNode': [10.0],
      'ReainForce_strategics_everyround':[2,3]}
keys = [key for key in VARS.keys()]
vars_values = [value for value in VARS.values()]
string = []
vars_ls= []
def recursive(index):
    for i in vars_values[index]:
        string.append(i)
        if index<len(vars_values)-1:  recursive(index+1)
        else:
            vars_ls.append({keys[i]:string[i] for i in range(len(keys))}) 
            string.pop()
def UPDATE_VARS(dict,addr):
    with open(addr,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(addr,'w',encoding="utf8") as f:
        lines[0]= f"VARS={str(dict)}\n"
        f.write(''.join(lines))
def game(dict_list:list):
    p0dict = dict_list[0]
    p1dict = dict_list[1]
    p2dict = dict_list[2]
    UPDATE_VARS(p0dict,p0_address)
    UPDATE_VARS(p1dict,p1_address)
    UPDATE_VARS(p2dict,p2_address)
    p=Popen(["py", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()
    print(errors)
    scores= [0,0,0]
    address = os.listdir('result_log')
    for addr in address:
        addr = 'result_log//'+addr
        with open(addr) as f:
            data = json.load(f)
            score = data['score']
            scores[0]+=score[0]
            scores[1]+=score[1]
            scores[1]+=score[1]
    return (scores,[p0dict,p1dict,p2dict])
def best_in_box(box:list):
    box.sort(key=lambda result: result[0][0],reverse=True)
    best_p0 = box[0][1][0]
    box.sort(key=lambda result: result[0][1],reverse=True)
    best_p1 = box[0][1][1]
    box.sort(key=lambda result: result[0][2],reverse=True)
    best_p2 = box[0][1][2]
    return [best_p0,best_p1,best_p2]

recursive(0)
pvars = [vars_ls,vars_ls,vars_ls]
n = 1
while  len(pvars[0])>1:
    new_pvars = [[],[],[]]
    with open('Result.txt','a',encoding='UTF-8') as f:
        f.write(f"\n\n\n\n\n\n*\n\n\n\n\n\nLayer{n}_Player_VARS={pvars}")
        
    #Fixing the number of players in layer
    for i in range(len(pvars)):
        while len(pvars[i])%BOX_NUMBER!=0:
            new_pvars[i].append(pvars[i].pop())


    #Creating a box and doing tournement on the layer
    box = []
    counter = 0
    for _ in trange(len(pvars[0])):
        dictls = []
        for var in pvars:   dictls.append(var.pop())
        box.append(game(dictls))
        counter+=1
        if counter==BOX_NUMBER:
            best = best_in_box(box)
            for i in range(len(best)):
                new_pvars[i].append(best[i])

            box=[]
            counter=0


    #Updating pvars
    pvars = new_pvars
    n+=1

with open('Result.txt','a',encoding='UTF-8') as f:
    f.write(f"\n\n\n\n\n\n\n\n\n\n\n\nLayer{n}_Player_VARS:{pvars}")