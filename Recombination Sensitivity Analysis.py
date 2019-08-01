from Differential_Evol_and_Shortest_Path_Analysis import find_path, callback
import time
import datetime
import csv
import numpy as np
from scipy.optimize import differential_evolution

Experiment_Name = 'Recombination Sensitivity'

# Samples to test with, remember to manually change the tier in the find_path function
tier0df = pd.read_csv('tier0samples.csv', index_col = 0, sep = "\t")
Testing_Samples = [string.split("'")[1] for string in tier0df.Sample_Names.to_list()]

# Initial Population
DR_Reduced = ([0,0,0,0,0,0,1,0,0,0,0,0,0,0],
             [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
             [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,1,0,0,0,0,0])

# setting bounds for parameters (w's)
bounds = [(0,10) for x in range(14)]

# setting link function
link = 'exp'

# define the recombination constants to test
CR = np.arange(0.4,1,0.1)

# initializaing empty weighing scheme, individual accuracy, & mean accuracy
w = np.empty([len(CR),len(bounds)])
Accuracy = np.empty([len(CR),3])
Average_Accuracy = np.empty([len(CR),1])

# run the differential evolution
for p,k in enumerate(CR):
   tic =time.time()
   res = differential_evolution(find_path, bounds = bounds,
                                                 seed = 1, 
                                                 mutation = (0.5,1),
                                                 recombination = k,
                                                 strategy = 'best1bin',
                                                 atol = 0, tol = 0.01,
                                                 polish = True,
                                                 init = DR_Reduced,
                                                 callback = callback,
                                                 args = Testing_Samples)
   w[p,:] = res.x
   Accuracy[p,:] = find_path(w[p,:],accflag=False)
   Average_Accuracy[p,:] = np.mean(Accuracy[p])
   print(res)
   
   csvdict ={}
   csvdict['CR'] = k
   metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Quino','Curvature','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']
   
   for i,m in enumerate(metrics):
       csvdict[m] = w[p,i]
   Sample_Names = ['71% Saturation Accuracy','77% Saturation Accuracy', '100% Saturation Accuracy']
   for i,s in enumerate(Sample_Names):
       csvdict[s] = Accuracy[p,i]
   csvdict['Average Accuracy'] = Average_Accuracy[p,0]

   toc = time.time()
   runtime = toc-tic
   alpha = 0.98
   average_runtime = 600
   average_runtime = (1-alpha)*runtime + alpha*average_runtime
   timeleft = average_runtime*(len(CR)-p)
   
   timefinish = datetime.datetime.now() + datetime.timedelta(seconds = timeleft) 
   print('average runtime = ', average_runtime,
         'timeleft = ', timeleft,
         'timefinish = ', timefinish)
   csvdict['RunTime'] = runtime
   
   with open(Experiment_Name+'.csv', 'a') as csvFile:
       writer = csv.DictWriter(csvFile, fieldnames = csvdict.keys())
       writer.writerow(csvdict) 