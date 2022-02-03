import os
from alpidedaqboard import decoder

def Run(argspath="./"):
    temppower=""
    
    for file in os.listdir(argspath):
        if file.endswith(".txt"):
            temppower = file
    
    input=f"{argspath}{temppower}"
    
    sum_a=0; sum_d=0; mean_a=0; mean_d=0; time=0;
    
    with open('%s'%(input),'rb') as f:
        for line in f:
            data=line
            str=data.decode('utf-8')
            word=str.split('\t')
            time=time+1
            n=0
            
            for i in word:
                if word[0]=='#time' : continue
                n=n+1
                if n==2 :
                    sum_a=sum_a+float(i)
                
                if n==3 :
                    sum_d=sum_d+float(i)

    mean_a=sum_a/(time-1)
    mean_d=sum_d/(time-1)

    print("---------------------")
    print("mean_a : %f"%(mean_a))
    print("mean_d : %f"%(mean_d))
    print("---------------------")
