from subprocess import run
import Best
import Test
def UPDATE_VARS(dict,test=True):
    if test:
        with open('test.py','r') as f:
            lines = f.readlines()
        with open('test.py','w') as f:
            lines[0]= f"VARS={str(dict)}\n"
            f.write(''.join(lines))
    else:
        with open('Best.py','r') as f:
            lines = f.readlines()
        with open('Best.py','w') as f:
            lines[0]= f"VARS={str(dict)}\n"
            f.write(''.join(lines))

NUMBER_OF_RUNS = 50

Best.VARS['x']=-300
Test.VARS['y']=1600

with open('Best.py','r') as f:
    lines = f.readlines()
with open('Best.py','w') as f:
    lines[0]= f"VARS={str(Best.VARS)}\n"
    f.write(''.join(lines))

run(['py','Test.py'])
run(['py','Best.py'])