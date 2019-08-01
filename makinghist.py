# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:37:51 2019

@author: zkana
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_table('PercolationThresholds.txt',header=None,names=['Sample_Names','Percolation_Threshold'])
plt.figure(figsize=(18,7))
plt.hist(df.Percolation_Threshold, bins=30,color='pink',edgecolor='black')
plt.xlabel('Percolation Threshold', fontsize = 15)
plt.ylabel('Count', fontsize = 15)
plt.text(2.5, 500,'tier 2: 362 samples',
        verticalalignment='top', horizontalalignment='right',
        color='black', fontsize=15)
plt.text(1.25, 675,'tier 1: 2534 samples',
        verticalalignment='top', horizontalalignment='center',
        color='black', fontsize=12)
plt.text(0.4, 500,'tier 0: 725 samples',
        verticalalignment='top', horizontalalignment='left',
        color='black', fontsize=15)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
#top95 = np.percentile(df.Percolation_Threshold, 95,interpolation='nearest')
#bottom5 = np.percentile(df.Percolation_Threshold, 5,interpolation='nearest')
top20 = np.percentile(df.Percolation_Threshold, 80,interpolation='nearest')
bottom10 = np.percentile(df.Percolation_Threshold, 10,interpolation='nearest')
plt.axvline(top20,label='80th Percentile = 1.48',linestyle='--',color='black')
plt.axvline(bottom10,label='10th Percentile = 1.01',linestyle='-',color='black')
plt.legend(fontsize = 15)
plt.savefig('Histogram of Sample Tiers.png',bbox_inches='tight')
#count = 1
#for i in range(len(df)):
#    if df.Percolation_Threshold[i] <= bottom10:
##        count += 1
#        pass
#    elif df.Percolation_Threshold[i] >= top20:
#        count += 1
#print('count =',count)

#want to get the Sample_Names (A000E01,etc.) & Percolation_Threshold (1.48, etc.)
#for ALL samples equal to or greater than 1.48 PT 
import csv
tier2samples = df[df.Percolation_Threshold >= top20] #PT greater than 1.48
tier2samples = tier2samples.reset_index(drop = True)
tier2samples.to_csv('tier2samples.csv', sep = "\t", quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")
tier1samples = df[(df.Percolation_Threshold >= bottom10) & (df.Percolation_Threshold < top20)] #PT between 1.48 & 1.01
tier1samples = tier1samples.reset_index(drop = True)
tier1samples.to_csv('tier1samples.csv', sep = "\t", quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")
tier0samples = df[df.Percolation_Threshold < bottom10] #PT less than 1.01
tier0samples = tier0samples.reset_index(drop = True)
tier0samples.to_csv('tier0samples.csv', sep = "\t", quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")