import scipy.io as sio
import numpy as np
import networkx as nx
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt
import time
import datetime
import csv
import h5py
import os
import pandas as pd
from skimage.transform import rescale, resize, downscale_local_mean
import random
start = time.time()

dataDirectory = os.path.normpath(r'C:\Users\zkana\Box Sync\Morales Lab\Z_Kanavas\Differential Evolution Project\01_COMSOL_automation\05_Cygwin\All_Samples_001\Sample_A')

# alternative sample calling method:
#folder_suffix = ('E01_','E02_','E03_','E05_','E07_','E09_')
#SampleDict = {k: [] for k in folder_suffix}
#
#for path, subdirectories, files in os.walk(dataDirectory):
#    for name in subdirectories:
#        if name.endswith(folder_suffix):
#            if os.path.isfile(r'C:\Users\zkana\Box Sync\Morales Lab\Z_Kanavas\Differential Evolution Project\01_COMSOL_automation\03_Images\2_PT_MatlabData\Sample_A\Eroding_' + name[-3:-1] + "/" + name + '.mat'):
#                SampleDict[name[-4:]].append(name)    
#S = SampleDict.values()

#Samples = [item for sublist in S for item in sublist]

def find_path(w,accflag=True, *SamplestoUse):
    w_arcL = w[0]
    w_Euc = w[1]
    w_Thin = w[2]
    w_MeanWidth = w[3]
    w_Thick = w[4]
    w_LT = w[5]
    w_widBot = w[6]
    w_Quino = w[7]
    w_Curvature = w[8]
    w_Straightness = w[9]
    w_Volume = w[10]
    w_AspectRatio = w[11]
    w_Poiseuille = w[12]
    w_Connectivity = w[13]
#    w_EucThick = w[7]

    sat_acc = np.zeros([len(SamplestoUse)])
    for z in range(len(SamplestoUse)):
        os.chdir(dataDirectory+'/'+SamplestoUse[z])
        with h5py.File('Data.hdf5','r') as f:
            Data = f.get('default').value #data is now an ndarray
        
        l_1 = Data[0::2,0]
        meanWidth = Data[0::2,7]
        inv_meanWidth = 1/meanWidth
        arcLength = Data[0::2,5]
        Euclidean = Data[0::2,4]
        min_Width = Data[0::2,8]
        inv_min_Width = 1/min_Width
        l_2 = Data[1::2,0]
        
        H_arcL = arcLength/(np.std(arcLength))
        H_Euc = Euclidean/(np.std(Euclidean))
        H_Thin = min_Width/(np.std(min_Width))
        H_MeanWidth = meanWidth/(np.std(meanWidth))
        H_Thick = inv_meanWidth/(np.std(inv_meanWidth))
        H_LT = (arcLength/(np.std(arcLength)))*(inv_meanWidth/(np.std(inv_meanWidth)))
        H_widBot = inv_min_Width/(np.std(inv_min_Width))
#        H_EucThick = (Euclidean)*(inv_meanWidth)
        H_Quino = np.exp(-1/(meanWidth/(np.std(meanWidth))))
        H_Curvature = 1-((Euclidean/np.std(Euclidean))/(arcLength/np.std(arcLength)))
        H_Straightness = 1/H_Curvature
        H_Volume = (arcLength/np.std(arcLength))*((min_Width/np.std(min_Width))**2)*np.pi
        H_AspectRatio = (arcLength/np.std(arcLength))/(min_Width/np.std(min_Width))
        H_Poiseuille = ((meanWidth/np.std(meanWidth))**4)/(arcLength/np.std(arcLength))
        H_Connectivity = Data[0::2,6]
        
        obj = w_arcL*H_arcL + w_Euc*H_Euc + w_Thin*H_Thin + w_MeanWidth*H_MeanWidth + w_Thick*H_Thick + w_LT*H_LT + w_widBot*H_widBot + w_Quino*H_Quino + w_Curvature*H_Curvature + w_Straightness*H_Straightness + w_Volume*H_Volume +w_AspectRatio*H_AspectRatio + w_Poiseuille*H_Poiseuille + w_Connectivity*H_Connectivity #w_EucThick*H_EucThick + w_Quino*H_Quino + w_Tortuosity*H_Tortuosity + w_Straightness*H_Straightness + w_Volume*H_Volume +w_AspectRatio*H_AspectRatio + w_Poiseuille*H_Poiseuille + w_Connectivity*H_Connectivity
        if (link == 'identity'):
            obj == obj
        elif link == 'log':
            obj == np.log(obj)
        elif link == 'inverse':
            obj == obj**-1
        elif link == 'exp':
            obj = np.exp(obj)
        elif link =='inverse squared':
            obj == obj**(-2)
        elif link == 'inverse square root':
            obj = obj**(-1/2)
        elif link == 'logit':
            obj = np.abs(np.log(np.abs(obj/(1-obj))))
        elif link == 'inverse logit':
            obj = (np.exp(obj)/(1+np.exp(obj)))
        
        #node ID for source node
        l_0 = np.min(Data[:,0])
        #node ID for target node                      
        l_00 = np.max(Data[:,0])                     
        
        UG = nx.Graph()
        edges = np.array([l_1, l_2, obj])
        tedges = []
        for i in range(len(edges[0,:])):
            tedges.append(tuple(edges[:,i]))
        for i in tedges:
            UG.add_edge(i[0], i[1], weight=i[2])
        try:
            path = nx.dijkstra_path(UG, l_0, l_00)
        except nx.NetworkXNoPath:
            print(SamplestoUse[z], 'has no path!!!')
            continue
        voxel = 50e-6 #[m]
        X = np.zeros(len(path))
        Y = np.zeros(len(path))
        for i in range((len(path))):
            X[i] = np.around((np.unique(Data[np.where(Data[:,0] == path[i]),1]))/voxel)
            Y[i] = np.around((np.unique(Data[np.where(Data[:,0] == path[i]),2]))/voxel)
        
        A = np.loadtxt(SamplestoUse[z] + "0000.txt", dtype='i', delimiter='\t')
        lower = 0
        upper = 1
        threshold = 255
        A = np.where(A>=threshold, upper, lower)
        
        # create zeros matrix to later add the nodes in the shortest path to
        Bi_Shortest_Path = np.zeros(A.shape)  
        #renaming X so that there are no issues when the code loops
        y1=X
        #renaming Y so that there are no issues when the code loops   
        x1=Y   
        y1[0] = 1 
        y1[0] = 1
        for i in range(len(y1)):
            if y1[i] > 1646:
                y1[i] = 1
        for i in range(len(x1)):
            if x1[i] > 1091:
                x1[i] = 1
        x1 = x1.astype(int)
        y1 = y1.astype(int)

        #adding the nodes to the zero matrix
        for i in range(1, len(x1)-1):      
            Bi_Shortest_Path[x1[i],y1[i]]=1
            Bi_Shortest_Path = Bi_Shortest_Path
        bmin = 0
        bmax = 1
        Shortest_Path = (np.where(Bi_Shortest_Path>=1, bmax, bmin))

        PT_file = os.path.normpath(r'C:\Users\zkana\Box Sync\Morales Lab\Z_Kanavas\Differential Evolution Project\01_COMSOL_automation\03_Images\2_PT_MatlabData\Sample_A\Eroding_'+SamplestoUse[z][-3:-1])
        PT = sio.loadmat(PT_file + '/' + SamplestoUse[z] + '.mat')
        PT = PT['plotting_final']
        image_resized = resize(PT, (Shortest_Path.shape[0], Shortest_Path.shape[1]),
                       anti_aliasing=True, preserve_range=True)
        lower = 0
        upper = 1
        threshold = 2.5
        Percolating_Path = np.where(image_resized>=threshold, upper, lower)
        if not accflag:
            lim = len(path)-1
            plt.figure()
            threshold_index = (np.where("'"+SamplestoUse[z]+"'" == Tiers[zoe].Sample_Names))
            plt.title('Sample Name: '+ SamplestoUse[z]+ '; Percolation Threshold: '+ str(Tiers[zoe].Percolation_Threshold[threshold_index[0]].to_list()))
            plt.imshow(Percolating_Path, cmap='Greys')
            plt.plot(X[1:lim],Y[1:lim], '--',c = 'cyan',zorder=1, lw=3)
            plt.scatter(X[1:lim],Y[1:lim], c='red',s=25 ,zorder = 2)
            plt.gca().get_xaxis().set_ticks([])
            plt.gca().get_yaxis().set_ticks([])
            plt.grid(False)
            plt.savefig(link+SamplestoUse[z]+'.png',bbox_inches='tight')
            
        Overlapping_Matrix = np.multiply(Shortest_Path, Percolating_Path)
        Accuracy = -1*(100*((np.sum(Overlapping_Matrix))/(np.sum(Shortest_Path))))
        sat_acc[z] = Accuracy
        print('The accuracy for',SamplestoUse[z], 'is', Accuracy, '%')
    if accflag:
        return np.mean(sat_acc) 
    else:
        return sat_acc
        
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

# callback function to track progress of minimization
def callback(xk, convergence):
    print('xk =',xk, 'val =', convergence)

# setting link function
link = 'exp'

# run the differential evolution
#res = differential_evolution(find_path, bounds = bounds,
#                             seed = 1,
#                             mutation = (0.5,1),
#                             recombination = 0.8,
#                             strategy = 'best1bin',
#                             atol = 0, tol = 0.01,
#                             polish = True,
#                             init = DR_All,
#                             callback = callback)
#print(res)