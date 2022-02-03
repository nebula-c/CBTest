#!/usr/bin/env python3

import argparse
import json
import numpy as np
import math
import os
import itertools


from matplotlib import pyplot as plt


DACs=[
  ('IAUX2'  ,10,1,0),
  ('IRESET' ,11,0,0),
  ('IDB'    ,12,3,0),
  ('IBIAS'  ,13,2,0),
  ('ITHR'   ,14,5,0)
]



def Run(argspath="./", argsfit=False):

    temptxt = "OnlyI.dat"
#    for file in os.listdir(argspath):
#        if file.endswith(".txt"):
#            temptxt = file
    
    input=f"{argspath}{temptxt}"
    
    
    sumfig=plt.figure()
    plt.title('Summary plot')
    plt.xlabel('DAC Setting')
    plt.ylabel('ADC')
    plt.xticks([0,64,128,192,255])

    outfilename=temptxt.split("/")[-1].split(".")[0]

    i=1
    for vdac in DACs:

        inputf=open("%s"%(input),'r')
        
        data=np.loadtxt(itertools.islice(inputf, 256*(i-1), 256*i),usecols=(1, 2))
        inputf.close()   #for now I don't know other way to read file again with loadtxt function
        
        if vdac==0.0:
            fit=np.polyfit(data[0:240,0],data[0:240,1],1)
        else:
            fit=np.polyfit(data[0:186,0],data[0:186,1],1)
            
        fit_fn=np.poly1d(fit)


        plt.figure(sumfig.number)
        plt.plot([x[0] for x in data],[y[1] for y in data],label=vdac[0])
        plt.figure()
        plt.xlabel('DAC Setting')
        plt.ylabel('ADC')
        plt.title('Scan of %s DAC'%vdac[0])
        plt.ylim(bottom=0,top=np.max(data[:,1])*1.1)
        plt.xlim(0,np.max(data[:,0]))

        plt.xticks([0,64,128,192,255])
        plt.plot([x[0] for x in data],[y[1] for y in data])
        x=np.linspace(0,255,256)
        if argsfit:
            plt.plot(x,fit_fn(x))
        plt.savefig('%s/%s-%s.png'%(argspath,outfilename,vdac[0]))
        plt.close()
        
        i+=1

    plt.legend(loc='upper left', fontsize='small')
    plt.savefig('%s/%s-all.png'%(argspath,outfilename))
    plt.close(sumfig)

    print("done")

