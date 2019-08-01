from Differential_Evol_and_Shortest_Path_Analysis import find_path, callback
import time
import datetime
import csv
import numpy as np
from scipy.optimize import differential_evolution
import pandas as pd
import random

Experiment_Name = 'Tiers'

tier0df = pd.read_csv('tier0samples.csv', index_col = 0, sep = "\t")
tier1df = pd.read_csv('tier1samples.csv', index_col = 0, sep = "\t")
tier2df = pd.read_csv('tier2samples.csv', index_col = 0, sep = "\t")

# Initial Population
DR_All = ([10,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,10,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,10,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,10,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,10,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,10,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,10,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,10,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,10,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,10,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,10,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,10,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,10,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,10],)

# setting bounds for parameters (w's)
bounds = [(0,10) for x in range(14)]

# setting link function
link = 'exp'

# define which sample tiers to use
Tiers = [tier0df,tier1df,tier2df]
tier_names = ['tier0','tier1','tier2']

# run the differential evolution
for zoe in range(len(Tiers)):
    tic = time.time()
    w = np.empty([len(Tiers),len(bounds)])
    Accuracy = np.empty([len(Tiers),len(Tiers[zoe])])
    Average_Accuracy = np.empty([len(Tiers),1])
    Validating = False
    Samples = [string.split("'")[1] for string in Tiers[zoe].Sample_Names.to_list()]
    Sample_Size = len(Samples)
    cut = int(0.8 * Sample_Size) #80% of the list
    random.shuffle(Samples) 
    Testing_Samples = Samples[:cut] # first 80% of shuffled list TESTING SET
    res = differential_evolution(find_path, bounds = bounds,
                             seed = 1,
                             mutation = (0.5,1),
                             recombination = 0.8,
                             strategy = 'best1bin',
                             atol = 0, tol = 0.01,
                             polish = True,
                             init = DR_All,
                             callback = callback,
                             args = Testing_Samples)
    print(res)
    w[zoe,:] = res.x
    Testing_Samples = Samples[cut:] # last 20% of shuffled list VALIDATING SET
    Accuracy[zoe,:] = find_path(w[zoe,:],accflag=False)
    Average_Accuracy[zoe,:]=np.mean(Accuracy[zoe])
    csvdict ={}
    csvdict['tier'] = tier_names[zoe]
    metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Quino','Curvature','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']
    
    for ii,m in enumerate(metrics):
        csvdict[m] = w[zoe,ii]
    csvdict['Average Accuracy'] = Average_Accuracy[zoe,0]

    toc = time.time()
    runtime = toc-tic
    alpha = 0.98
    average_runtime = 600
    average_runtime = (1-alpha)*runtime + alpha*average_runtime
    timeleft = average_runtime*(len(Tiers)-zoe)
    
    timefinish = datetime.datetime.now() + datetime.timedelta(seconds = timeleft) 
    print('average runtime = ', average_runtime,
          'timeleft = ', timeleft,
          'timefinish = ', timefinish)
    csvdict['RunTime'] = runtime
    
    with open(Experiment_Name+'.csv', 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = csvdict.keys())
        writer.writerow(csvdict)

