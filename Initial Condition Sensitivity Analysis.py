from Differential_Evol_and_Shortest_Path_Analysis import find_path, callback
import time
import datetime
import csv
import numpy as np
from scipy.optimize import differential_evolution

Experiment_Name = 'Initial Condition Sensitivity'

# Samples to test with, remember to manually change the tier in the find_path function
tier0df = pd.read_csv('tier0samples.csv', index_col = 0, sep = "\t")
Testing_Samples = [string.split("'")[1] for string in tier0df.Sample_Names.to_list()]

# Initial Conditions
# Educated Guess
M1 = ([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],[5.37408615,6.30523493,7.04174803,4.42997039,0.34805929,
      5.14335228,0.06030729,6.43193521,7.09649569,6.12087949,
      2.77427426,3.87107653,0.84209286,8.93141041,7.24596446],
    [0,0,0,0,0,7,1,0,0,0,0,0,0,0,0],[0,1,0,0,0,3,0,0,0,0,0,0,0,0,0],
    [0.5,0.5,0,0,0,7,1,0,0,0,0,0,0,0,0])

# Best Guess Uniform - Emphasizing Long&Thick Attribute
M2 = ([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])

# Uniformly Distributed Across Bounds
M3 = ([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5],
    [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    [7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5],
    [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10])

# Latin Hypercube sampling tries to maximize coverage of the available parameter space
M4 = 'latinhypercube'

# ‘random’ initializes the population randomly - this has the drawback that 
# clustering can occur, preventing the whole of parameter space being covered
M5 = 'random'

# Distributed Representation (DR) Series. Note each vector is of length 14, the inital populations above have vectors
# of length 15, this is because there was an attribute that was removed while this sensitivity analysis was ongoing.
# For completeness, both sets have been included, but there are currently only 14 different structural attributes 
# being analyzed.

# full identity matrix, note this was later changed to 10 along the diagonal to fit the bounds
DR_All = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,1],)

# the following attributes were removed: min thickness, mean thickness, volume
DR_NoMinMeanVol = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,1],)

# the following attributes were removed: min thickness, mean thickness, volume, poiseuille
DR_NoMinMeanVolPoiseuille = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,1],)

# this initial population only highlights the long&thick, widest bottleneck, aspect ratio, thick, & quino attributes
DR_Reduced = ([0,0,0,0,0,0,1,0,0,0,0,0,0,0],
             [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
             [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,1,0,0,0,0,0])

# setting bounds for parameters (w's)
bounds = [(0,10) for x in range(14)]

# setting link function
link = 'exp'

# define which inital populations to use
M = ([DR_All,DR_NoMinMeanVol,DR_NoMinMeanVolPoiseuille,DR_Reduced,M4])

# initializaing empty weighing scheme, individual accuracy, & mean accuracy
w = np.empty([len(M),len(bounds)])
Accuracy = np.empty([len(M),3]) #the second variable of the sample space is how many samples are being tested
Average_Accuracy = np.empty([len(M),1])

# run the differential evolution
for p,k in enumerate(M):
   tic =time.time()
   res = differential_evolution(find_path, bounds = bounds,
                                     seed = 1, 
                                     mutation = (0.5,1),
                                     recombination = 0.7,
                                     strategy = 'best1bin',
                                     atol = 0, tol = 0.01,
                                     polish = True,
                                     init = k,
                                     callback=callback,
                                     args = Testing_Samples)
   w[p,:] = res.x
   Accuracy[p,:] = find_path(w[p,:],accflag=False)
   Average_Accuracy[p,:] = np.mean(Accuracy[p])
   print(res)
   csvdict ={}
   csvdict['IC'] = k
   metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Quino','Curvature','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']
   
   for i,m in enumerate(metrics):
       csvdict[m] = w[p,i]
   Sample_Names = ['71% Saturation Accuracy','77% Saturation Accuracy']
   for i,s in enumerate(Sample_Names):
       csvdict[s] = Accuracy[p,i]
   csvdict['Average Accuracy'] = Average_Accuracy[p,0]

   toc = time.time()
   runtime = toc-tic
   alpha = 0.98
   average_runtime = 600
   average_runtime = (1-alpha)*runtime + alpha*average_runtime
   timeleft = average_runtime*(len(M)-p)
   
   timefinish = datetime.datetime.now() + datetime.timedelta(seconds = timeleft) 
   print('average runtime = ', average_runtime,
         'timeleft = ', timeleft,
         'timefinish = ', timefinish)
   csvdict['RunTime'] = runtime
   
   with open(Experiment_Name+'.csv', 'a') as csvFile:
       writer = csv.DictWriter(csvFile, fieldnames = csvdict.keys())
       writer.writerow(csvdict)
    