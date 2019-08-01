from Differential_Evol_and_Shortest_Path_Analysis import find_path, callback
import time
import datetime
import csv
import numpy as np
from scipy.optimize import differential_evolution

Experiment_Name = 'Seed Sensitivity'

# Samples to test with, remember to manually change the tier in the find_path function
tier0df = pd.read_csv('tier0samples.csv', index_col = 0, sep = "\t")
Testing_Samples = [string.split("'")[1] for string in tier0df.Sample_Names.to_list()]

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

# set which seeds to test
Seed = [1,2,3]

# initializaing empty weighing scheme, individual accuracy, & mean accuracy
w = np.empty([len(Seed),len(bounds)])
Accuracy = np.empty([len(Seed),3])
Average_Accuracy = np.empty([len(Seed),1])

# run the differential evolution
for p,k in enumerate(Seed):
   tic = time.time()
   res = differential_evolution(find_path, bounds = bounds,
                                seed = k,
                                mutation = (0.5,1),
                                recombination = 0.8,
                                strategy = 'best1bin',
                                atol = 0, tol = 0.01,
                                polish = True,
                                init = DR_All,
                                callback = callback,
                                args = Testing_Samples)
   w[p,:] = res.x
   Accuracy[p,:] = find_path(w[p,:],accflag=False)
   Average_Accuracy[p,:] = np.mean(Accuracy[p])
   print(res)
   csvdict ={}
   csvdict['Seed'] = k
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
   timeleft = average_runtime*(len(Seed)-p)
   
   timefinish = datetime.datetime.now() + datetime.timedelta(seconds = timeleft) 
   print('average runtime = ', average_runtime,
         'timeleft = ', timeleft,
         'timefinish = ', timefinish)
   csvdict['RunTime'] = runtime
   
   with open(Experiment_Name+'.csv', 'a') as csvFile:
       writer = csv.DictWriter(csvFile, fieldnames = csvdict.keys())
       writer.writerow(csvdict)