# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 19:01:05 2019

@author: Jakob
"""
from argparse import ArgumentParser
import matplotlib.pylab as plt
import numpy as np
import os
import sys

sys.path.insert(0, '../Helper')
sys.path.insert(0, '../IV_Mixer_Analysis')
sys.path.insert(0, '../Superconductivity')


from IV_Class import IV_Response,kwargs_IV_Response_John
from plotxy import plot,newfig,pltsettings,lbl


parser = ArgumentParser()
parser.add_argument('-f', '--folder', action='store',default = 'Superposition_of_IV_Curves_Default_Folder', help='The folder in which the result is stored in.')
args = parser.parse_args()

directory = args.folder+'/'
if not os.path.exists(directory):
        os.makedirs(directory)

kwargs_IV_Response_John['fixedOffset']=[0.101802-0.0095, 9.880048347102433]

IV = IV_Response('../IV_Mixer_Analysis/DummyData/John/Unpumped.csv',**kwargs_IV_Response_John)

##############################################
##### Introduce a factor to the IV curve #####
##############################################

#factor = np.arange(.7,1.5,.05) Does not work since it gets weird small values
factor = np.divide(np.arange(7,15,.5),10)

IVbyFactor = dict()
for i in factor:    
    IVbyFactor[i] = np.vstack([IV.binedIVData[0],np.multiply(i,IV.binedIVData[1])])
    
    
title = newfig('Sum_Factor_1_1')    
plot(IVbyFactor[1.],label = 'Factor 1.')
plot(IVbyFactor[1.],label = 'Factor 1.')
plt.plot(IVbyFactor[1.][0],IVbyFactor[1.][1]+IVbyFactor[1.][1],label='Sum')
pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                xlim=[0,2.7],ylim=[0,30],title=None,legendColumns=1,skip_legend=False)

title = newfig('Sum_Factor_1._1.2')    
plot(IVbyFactor[1.],label = 'Factor 1.')
plot(IVbyFactor[1.2],label = 'Factor 1.2')
plt.plot(IVbyFactor[1.][0],IVbyFactor[1.][1]+IVbyFactor[1.2][1],label='Sum')
pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                xlim=[0,2.7],ylim=[0,30],title=None,legendColumns=1,skip_legend=False)

title = newfig('Sum_Factor_1._.85')    
plot(IVbyFactor[1.],label = 'Factor 1.')
plot(IVbyFactor[.85],label = 'Factor .85')
plt.plot(IVbyFactor[1.][0],IVbyFactor[1.][1]+IVbyFactor[.85][1],label='Sum')
pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                xlim=[0,2.7],ylim=[0,30],title=None,legendColumns=1,skip_legend=False)

###############################
##### Offset the IV curve #####
###############################

#IV.binWidth
#0.005997001499250375
# 2 bins correspond with an offset of approximately 12 uV
binOffset = np.arange(1,101,1)
IVOffseted = dict()
IVOffsetedSum = dict()
for i in binOffset:    
    positiveOffset = np.vstack([IV.binedIVData[0,:-i],IV.binedIVData[1,i:]])
    negativeOffset = np.vstack([IV.binedIVData[0,i:],IV.binedIVData[1,:-i]])
    IVOffseted[i] = np.vstack([[negativeOffset],[positiveOffset]])
    IVOffsetedSum[i] = np.vstack([IV.binedIVData[0,i:-i] ,
                                     np.add(positiveOffset[1,i:],negativeOffset[1,:-i])])
    #Sum has been tested with IV.binedIVData = np.vstack([np.arange(-10,10,.1),np.square(np.arange(-10,10,.1))])
    
offsetsplotted = [1,10,25,50,100]
for i in offsetsplotted:
    title = newfig('Offset_%d_bins'%(2*i))    
    plot(IVOffseted[i][0],label = 'Negative Offseted %d bins'%i)
    plot(IVOffseted[i][1],label = 'Positive Offseted %d bins'%i)
    plot(IVOffsetedSum[i],label = 'Sum Offseted %d bins total'%(2*i))
    plt.annotate("%d bins correspond with %.1f uV"%(i,IV.binWidth*1e3),
                     (-1,-20),xytext=(-1,-20),
                     linespacing=linespacing, size=fontsize, bbox=dict(boxstyle="round", fc="w",alpha=0.8) )
    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=False, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                        xlim=[-2.7,2.7],ylim=[-30,30],
                        title=None,legendColumns=1,skip_legend=False)  



#binOffset = np.arange(10,100,10)
#for i in binOffset:
#    IVoffseted = np.vstack([IV.binedIVData[0,:-i],IV.binedIVData[1,i:]])
#    IVoffsetedSum = np.vstack([IVoffseted[0],IVoffseted[1]+IV.binedIVData[1,:-i]])
#    title = newfig('Offseted_Factor_1._1._%.0f_bins'%i)    
#    plot(IV.binedIVData,label = 'Original')
#    plot(IVoffseted,label = 'Offseted %.0f bins'%i)
#    plot(IVoffsetedSum,label='Sum Offset')
#    plt.plot(IV.binedIVData[0],IV.binedIVData[1]*2,label='Sum without Offset')
#    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['mV'],ylabel=lbl['uA'], 
#                    xlim=[-2.7,2.7],ylim=[-30,30],
#                    title=None,legendColumns=1,skip_legend=False)
#    
#for i in binOffset:
#    IVoffseted = np.vstack([IV.binedIVData[0,:-i],IV.binedIVData[1,i:]])
#    IVoffsetedSum = np.vstack([IVoffseted[0],IVoffseted[1]+IVbyFactor[1.2][1,:-i]])
#    title = newfig('Offseted_Factor_1._1.2_%.0f_bins'%i)    
#    plot(IVbyFactor[1.2],label = 'Original Factor 1.2')
#    plot(IVoffseted,label = 'Offseted %.0f bins'%i)
#    plot(IVoffsetedSum,label='Sum Offset')
#    plt.plot(IV.binedIVData[0],IVbyFactor[1.][1]+IVbyFactor[1.2][1],label='Sum without Offset')
#    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['mV'],ylabel=lbl['uA'], 
#                    xlim=[-2.7,2.7],ylim=[-30,30],
#                    title=None,legendColumns=1,skip_legend=False)
    
    
