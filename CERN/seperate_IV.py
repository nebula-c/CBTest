#!/usr/bin/env python3

import os

def OnlyV(argspath="./"):

    temptxt = ""
    for file in os.listdir(argspath):
        if file.endswith(".txt"):
            temptxt = file
    
    input=f"{argspath}{temptxt}"
    
    f2=open(f"{argspath}OnlyV.dat","w")
    
    with open('%s'%(input),'rb') as f:
        for line in f:
            data=line
            str=data.decode('utf-8')
            if str[0] == "V":
                #print(str)
                f2.write(str)
    f2.close()
    
def OnlyI(argspath="./"):

    temptxt = ""
    for file in os.listdir(argspath):
        if file.endswith(f".txt"):
            temptxt = file
    
    input=f"{argspath}{temptxt}"
    
    f2=open(f"{argspath}OnlyI.dat","w")
    
    with open('%s'%(input),'rb') as f:
        for line in f:
            data=line
            str=data.decode('utf-8')
            if str[0] == "I":
                #print(str)
                f2.write(str)
    f2.close()
