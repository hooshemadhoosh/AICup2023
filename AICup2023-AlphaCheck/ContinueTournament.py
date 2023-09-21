with open('Result.txt','r',encoding='UTF-8') as f:
    data = f.read()
data = data.split('*')[-1].strip().split('=')[1]
data = eval(data)
import Tournament
Tournament.pvars = data
Tournament.volume = len(Tournament.pvars[0])
Tournament.main()