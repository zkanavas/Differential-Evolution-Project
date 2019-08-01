# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:05:20 2019

@author: zkana
"""
#ROW & COLUMN TITLES NEED TO BE ADDED SEPARATELY
import csv
from pandas import read_csv
Experiment_Name = 'Initial Condition Sensitivity'
metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Euclidean & Thick','Quino','Tortuosity','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']

#Educated_Guess = ([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                  [5.37408615,6.30523493,7.04174803,4.42997039,0.34805929,
#                   5.14335228,0.06030729,6.43193521,7.09649569,6.12087949,
#                   2.77427426,3.87107653,0.84209286,8.93141041,7.24596446],
#                   [0,0,0,0,0,7,1,0,0,0,0,0,0,0,0],
#                   [0,1,0,0,0,3,0,0,0,0,0,0,0,0,0],
#                   [0.5,0.5,0,0,0,7,1,0,0,0,0,0,0,0,0])
#for p in range(len(Educated_Guess)):
#    IC1dict ={}
##    IC1dict['IC'] = ('Vector 1','Vector 2','Vector 3','Vector 4','Vector 5')
#    for i,m in enumerate(metrics):
#        IC1dict[m] = Educated_Guess[p][i]
#    with open(Experiment_Name+'EducatedGuessIC.csv', 'a') as csvFile:
#        writer = csv.DictWriter(csvFile, fieldnames = IC1dict.keys())
#        writer.writerow(IC1dict)
#        
#Educated_Guess_Uniform = ([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])
#for p in range(len(Educated_Guess_Uniform)):
#    IC2dict ={}
##    IC2dict['IC'] = ('Vector 1','Vector 2','Vector 3','Vector 4','Vector 5')
#    for i,m in enumerate(metrics):
#        IC2dict[m] = Educated_Guess_Uniform[p][i]
#    with open(Experiment_Name+'EducatedGuessUniformIC.csv', 'a') as csvFile:
#        writer = csv.DictWriter(csvFile, fieldnames = IC2dict.keys())
#        writer.writerow(IC2dict)
#        
#Uniform_Distribution = ([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                        [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5],
#                        [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
#                        [7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5,7.5],
#                        [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10])
#for p in range(len(Uniform_Distribution)):
#    IC3dict ={}
#    for i,m in enumerate(metrics):
#        IC3dict[m] = Uniform_Distribution[p][i]
#    with open(Experiment_Name+'UniformDistributionIC.csv', 'a') as csvFile:
#        writer = csv.DictWriter(csvFile, fieldnames = IC3dict.keys())
#        writer.writerow(IC3dict)
#
#Educated_Guess_Simplified = ([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
#                             [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
#                             [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0])
#for p in range(len(Educated_Guess_Simplified)):
#    IC4dict ={}
#    for i,m in enumerate(metrics):
#        IC4dict[m] = Educated_Guess_Simplified[p][i]
#    with open(Experiment_Name+'EducatedGuessSimplifiedIC.csv', 'a') as csvFile:
#        writer = csv.DictWriter(csvFile, fieldnames = IC4dict.keys())
#        writer.writerow(IC4dict)

Distributed_Representation_All = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],)

for p in range(len(Distributed_Representation_All)):
    IC5dict ={}
    for i,m in enumerate(metrics):
        IC5dict[m] = Distributed_Representation_All[p][i]
    with open(Experiment_Name+'DistributedRepAllIC.csv', 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = IC5dict.keys())
        writer.writerow(IC5dict)
        
Distributed_Representation_NoMinMeanVolume = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                              [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                              [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                              [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                              [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                              [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                              [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                              [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                              [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                              [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                                              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],)
for p in range(len(Distributed_Representation_NoMinMeanVolume)):
    IC6dict ={}
    for i,m in enumerate(metrics):
        IC6dict[m] = Distributed_Representation_NoMinMeanVolume[p][i]
    with open(Experiment_Name+'DistributedRepNoMinMeanVolumeIC.csv', 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = IC6dict.keys())
        writer.writerow(IC6dict)

Distributed_Representation_NoMinMeanVolumePoiseuille = ([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                                        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                                        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                                        [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                                        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                                        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                                        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                                        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                                        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                                        [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],)
for p in range(len(Distributed_Representation_NoMinMeanVolumePoiseuille)):
    IC7dict ={}
    for i,m in enumerate(metrics):
        IC7dict[m] = Distributed_Representation_NoMinMeanVolumePoiseuille[p][i]
    with open(Experiment_Name+'DistributedRepNoMinMeanVolumePoiseuilleIC.csv', 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames = IC7dict.keys())
        writer.writerow(IC7dict)