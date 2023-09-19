import json
import os
from subprocess import Popen
import subprocess
from tqdm import tqdm, trange
import time
p0_address  = "procode//p0.py"
p1_address  = "procode//p1.py"
p2_address  = "procode//p2.py"
VARS={'strategic_troops_number':[6,9,12],
      'mytroops/enemytroops (beta)': [1.01,1.05,1.2], 
      'beta_plus':[1.5],
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
def game(p0dict,p1dict,p2dict):
    UPDATE_VARS(p0dict,p0_address)
    UPDATE_VARS(p1dict,p1_address)
    UPDATE_VARS(p2dict,p2_address)
    p=Popen(["py", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = p.communicate()
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
    best_p0 = box[1][0]
    box.sort(key=lambda result: result[0][1],reverse=True)
    best_p1 = box[1][1]
    box.sort(key=lambda result: result[0][2],reverse=True)
    best_p2 = box[1][2]
    return [best_p0,best_p1,best_p2]

# recursive(0)
# for i in trange(10):
#     print(game(vars_ls[0],vars_ls[0],vars_ls[0]))