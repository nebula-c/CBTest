import argparse
import json
import numpy as np
import math
from alpidedaqboard import decoder
from tqdm import tqdm
from scipy import optimize
from scipy import special
from matplotlib import pyplot as plt
import os


def Run(argspath="./") :

    thresholds = np.load(f"{argspath}thresholds.npy")
    
    tempjson = ""
    for file in os.listdir(argspath):
        if file.endswith(".json"):
            tempjson = file
    
    input1=f"{argspath}{tempjson}"
    with open('%s'%(input1),'r') as f:
        params=json.loads(f.read())
    
    outfilename=tempjson.split("/")[-1].split(".")[0]
    
    dvmin,dvmax=params['dvmin'],params['dvmax']

    
    thresholds[thresholds==0]=np.nan
    print('Threshold: %.2f +/- %.2f DAC (based on %d pixels)'%(np.nanmean(thresholds),np.nanstd(thresholds),np.sum(~np.isnan(thresholds))))
    thresholds_draw = thresholds.ravel()
    n, bins, patches = plt.hist(thresholds_draw,bins=1*dvmax,range=(0,dvmax),color='r')
    plt.xlim(0,dvmax)
    plt.title('Threshold: $\mu=%.2f,\ \sigma=%.2f$'%(np.nanmean(thresholds),np.nanstd(thresholds)))
    plt.xlabel('Threshold (DAC)')
    plt.ylabel('Pixels')
    plt.savefig('%s/%s-threshold.png'%(argspath,outfilename))
    plt.clf()
