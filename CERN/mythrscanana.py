#!/usr/bin/env python3

import argparse
import json
import numpy as np
import math
import os
from alpidedaqboard import decoder
from tqdm import tqdm
from scipy import optimize
from scipy import special
from matplotlib import pyplot as plt

def Run(argspath="./", argsfit=False, argsdebugpolts=False, argsoutput='thresholds.npy'):

    def sigmoid(x,Threshold, Noise):
        y=(params['ntrg'] / 2) * (1 + special.erf( ((x - Threshold) / (np.sqrt(2) *Noise))  ) )
        return (y)



    tempraw = ""
    tempjson = ""
    for file in os.listdir(argspath):
        if file.endswith(".raw"):
            tempraw = file
        if file.endswith(".json"):
            tempjson = file
    

    outfilename=tempraw.split("/")[-1].split(".")[0]
    
    input1=f"{argspath}{tempraw}"
    input2=f"{argspath}{tempjson}"
    
    with open('%s'%(input2),'r') as f:
        params=json.loads(f.read())
    with open('%s'%(input1),'rb') as f:
        data=f.read()


    dvmin,dvmax=params['dvmin'],params['dvmax']
    if params['row']==None: params['row']=range(512)
    ntrg = params['ntrg']
    pbar=tqdm(total=len(data), position=0, leave=True)
    thresholds=np.zeros((512,1024))
    noise=np.zeros((512,1024))
    dead=[]
    bad=[]

    i=0
    for row in params['row']:
        rowhits=np.zeros((dvmax-dvmin+1,1024))
        for dv in range(dvmin,dvmax+1):
            for itrg in range(params['ntrg']):
                hits,iev,tev,j=decoder.decode_event(data,i)
                pbar.update(j-i)
                i=j
                for x,y in hits:
                    if y!=row:
                        print('warning: hit from bad row: hit=(%d,%d) row=%d \n'%(x,y,row))
                    else:
                        rowhits[dv-dvmin,x]+=1
        if not argsfit:
            d=np.diff(rowhits,axis=0)
            nhits = np.sum(d,axis=0)
            if np.any(nhits<ntrg):
                bad.extend([(col,row) for col in np.where(nhits<ntrg)[0]])
            if np.any(nhits==0):
                dead.extend([(col,row) for col in np.where(nhits==0)[0]])
            nhits[nhits<ntrg] = np.nan # exclude from calculation
            d/=nhits
            dv=np.linspace(0.5,rowhits.shape[0]-1.5,rowhits.shape[0]-1)[:,np.newaxis]
            t=np.sum(d*dv,axis=0)
            n=np.sqrt(np.sum((dv-t)**2*d,axis=0))
            thresholds[row,:]=t
            noise[row,:]=n
        else:
            dvx=np.linspace(0,rowhits.shape[0]-1,rowhits.shape[0])[:,np.newaxis]
            for index in range(rowhits.shape[1]):
               if rowhits[:,index].max()==0:
                   dead.append((index,row))
                   continue
               p0 = [(dvmax-dvmin)/2,0.5]  # initial guess
               try:
                  popt, pcov = optimize.curve_fit(sigmoid, dvx[:,0],rowhits[:,index] ,p0,method='lm')
               except RuntimeError:
                  if argsdebugpolts:
                     plt.plot(dvx[:,0],rowhits[:,index],'ro')
                     plt.title('Warning: Bad Fit for a pixel at row %d column %d'%(row,index))
                     plt.xlabel('dV')
                     plt.ylabel('Successful triggers from %d'%(params['ntrg']))
                     plt.savefig('%s/%s-BadPixel_%d_%d.png'%(argspath,outfilename,row,index))
                     plt.clf()
                  bad.append((index,row))
                  continue
               thresholds[row,index]=popt[0]
               noise[row,index]=popt[1]
    pbar.close()
    np.save('%s/%s'%(argspath,argsoutput),thresholds)

    #plt.imshow(thresholds)
    #plt.colorbar()
    plt.xlabel('column')
    plt.ylabel('row')

    #edit
    plt.gca().invert_yaxis()
    plt.pcolor(thresholds,vmin=0,vmax=15)
    plt.colorbar()

    plt.savefig('%s/%s-thresholdmap.png'%(argspath,outfilename))
    plt.clf()
       
    thresholds[thresholds==0]=np.nan
    print('Threshold: %.2f +/- %.2f DAC (based on %d pixels)'%(np.nanmean(thresholds),np.nanstd(thresholds),np.sum(~np.isnan(thresholds))))
    thresholds_draw = thresholds.ravel()
    n, bins, patches = plt.hist(thresholds_draw,bins=1*dvmax,range=(0,dvmax))
    plt.xlim(0,dvmax)
    plt.title('Threshold: $\mu=%.2f,\ \sigma=%.2f$'%(np.nanmean(thresholds),np.nanstd(thresholds)))
    plt.xlabel('Threshold (DAC)')
    plt.ylabel('Pixels')
    plt.savefig('%s/%s-threshold.png'%(argspath,outfilename))
    plt.clf()


    noise[noise==0]=np.nan
    print('Noise: %.2f +/- %.2f DAC (based on %d pixels)'%(np.nanmean(noise),np.nanstd(noise),np.sum(~np.isnan(noise))))
    noise_draw = noise.ravel()
    n, bins, patches = plt.hist(noise_draw,bins=100,range=(0,5))
    plt.xlim(0,5)
    plt.title('Noise: $\mu=%.2f,\ \sigma=%.2f$'%(np.nanmean(noise),np.nanstd(noise)))
    plt.xlabel('Noise (DAC)')
    plt.ylabel('Pixels')
    plt.savefig('%s/%s-noise.png.png'%(argspath,outfilename))
    plt.clf()

    print(f"Found {len(bad)} bad pixels (with <{ntrg} hits)")
    #print(f"  of which {len(dead)} dead (with 0 hits).")
