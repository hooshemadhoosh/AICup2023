import pandas as pd
file = pd.read_csv('procode//vars.csv')
p0_address  = "procode//p0.py"
p1_address  = "procode//p1.py"
p2_address  = "procode//p2.py"
p0_vars = {file['NAME'][i]:file['p0'][i] for i in range(len(file['NAME']))}
p1_vars = {file['NAME'][i]:file['p1'][i] for i in range(len(file['NAME']))}
p2_vars = {file['NAME'][i]:file['p2'][i] for i in range(len(file['NAME']))}
def UPDATE_VARS(dict,addr):
    with open(addr,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(addr,'w',encoding="utf8") as f:
        lines[0]= f"VARS={str(dict)}\n"
        f.write(''.join(lines))

def dicp(dictionary):
    result = ''
    for key in dictionary:
        result+=str(dictionary[key])+'\n'
    return result
def percent(score,wins):
    total = wins[0]+wins[1]+wins[2]
    return f"{round(score,2)}"
def keys(dic):
    res=''
    for key in dic:
        res+=key+':\n'
    return  res

UPDATE_VARS(p0_vars,p0_address)
UPDATE_VARS(p1_vars,p1_address)
UPDATE_VARS(p2_vars,p2_address)
import datetime
from subprocess import run
import procode.p0 as p0
import procode.p1 as p1
import procode.p2 as p2
import os
import json
import matplotlib.pyplot as plt
from subprocess import Popen,run
import subprocess
import time
start_time = time.time()
run(['py','main.py'],shell=False,capture_output=False)
# p=Popen(["py", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# output, errors = p.communicate()
# print(errors)
# print (output)
print("--- %s seconds ---" % (time.time() - start_time))

wins = [0,0,0]
players = ['P0','P1','P2']
address = os.listdir('result_log')
for addr in address:
    addr = 'result_log//'+addr
    with open(addr) as f:
        data = json.load(f)
        score = data['score']
        wins[score.index(max(score))]+=1
lbl = [f"{round(t/sum(wins)*100,2)}({t} Times)" for t in wins]
fig, axe = plt.subplots(figsize=(10, 10), dpi=300)
axe.pie(wins,textprops=dict(color="black",backgroundcolor="yellow",weight='bold' ),labels=lbl,shadow=True)
axe.legend(players,title="Info")
font = {'family': 'consolas',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }
font0 = {'family': 'consolas',
        'color':  'blue',
        'weight': 'bold',
        'size': 12,
        }
font1 = {'family': 'consolas',
        'color':  'orange',
        'weight': 'bold',
        'size': 12,
        }
font2 = {'family': 'consolas',
        'color':  'green',
        'weight': 'bold',
        'size': 12,
        }
axe.text(-1.6,-1.6, f"\n{keys(file['NAME'])}",fontdict=font)
axe.text(-0.5,-1.6, f"P0\n{dicp(p0.VARS)}",fontdict=font0)
axe.text(-0.3,-1.6, f"P1\n{dicp(p1.VARS)}",fontdict=font1)
axe.text(-0.1,-1.6, f"P2\n{dicp(p2.VARS)}",fontdict=font2)
plt.savefig("analysis//" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png")