import datetime
from subprocess import run
import procode.p0 as p0
import procode.p1 as p1
import os
import json
import matplotlib.pyplot as plt
from subprocess import run
ai_address  = "procode//ai.py"
check_address  = "procode//check.py"
def UPDATE_VARS(dict,test=True):
    if test:
        with open(check_address,'r') as f:
            lines = f.readlines()
        with open(check_address,'w') as f:
            lines[0]= f"VARS={str(dict)}\n"
            f.write(''.join(lines))
    else:
        with open(ai_address,'r') as f:
            lines = f.readlines()
        with open(ai_address,'w') as f:
            lines[0]= f"VARS={str(dict)}\n"
            f.write(''.join(lines))
def dicp(dictionary):
    result = ''
    for key in dictionary:
        result+=str(key)+':'+str(dictionary[key])+'\n'
    return result
def percent(score,wins):
    total = wins[0]+wins[1]+wins[2]
    return f"{round(score,2)}"


run(['py','main.py'],shell=True)

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
        'color':  'blue',
        'weight': 'normal',
        'size': 12,
        }
font2 = {'family': 'consolas',
        'color':  'orange',
        'weight': 'normal',
        'size': 12,
        }
axe.text(-1.6,-1.6, f"P0 VARS:\n{dicp(p0.VARS)}",fontdict=font)
axe.text(0.5,-1.6, f"P1 VARS:\n{dicp(p1.VARS)}",fontdict=font2)
plt.savefig("analysis//" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f") + ".png")