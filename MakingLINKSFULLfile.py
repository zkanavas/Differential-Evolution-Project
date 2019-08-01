# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:24:02 2019

@author: zkana
"""
import os
import numpy as np
import time
import h5py

#want to get the files (for example): A000E09__Lines.dat & A000E09__Links.dat
#(NOTE 2 UNDERSCORES!) for all 739 files

voxel = 50e-6 #[m]
diameter = 3.6e-3 #[m] Morales et. al Geophysical Research Letters
#DONT MTLPY BY VOXELS
dimx = 754
dimy = 754
dimz = 1
dataDirectory = os.path.normpath(r'C:\Users\zkana\Box Sync\Morales Lab\Z_Kanavas\Differential Evolution Project\01_COMSOL_automation\05_Cygwin\All_Samples_001\Sample_A')
# can only use the following erosion steps bc these are what we have PT info for
folder_suffix = ('E01_','E02_','E03_','E05_','E07_','E09_') 
tic = time.time()
for path, subdirectories, files in os.walk(dataDirectory):
    for name in subdirectories:
        if name.endswith(folder_suffix):
            dataDirectory2 = os.path.join(dataDirectory,name)
            for path2,subdirectories2,files2 in os.walk(dataDirectory2):
                os.chdir(path2)
                for file in files2:
                    if file.endswith('_Lines.dat'):
                        Lines = np.loadtxt(file) #[x y z ArcL_cumulative rmin edgeID]
                        Lines[:,:4] = Lines[:,:4]*voxel
                        Lines[:,4] = Lines[:,4]*2
                    if file.endswith('Links.dat'):
                        Links = np.loadtxt(file) #[l_1 x_1 y_1 z_1 Euc L k_1]
                        Links[:,1:5] = Links[:,1:5]*voxel
                        emptycolumns=np.zeros([len(Links),4])
                        Links = np.append(Links,emptycolumns,axis=1)
# combine channel stats from Lines with Links                         
                        for i in np.arange(0,len(Links),2):
                            ind = np.where(np.logical_and(Links[i,1]==Lines[:,0], np.logical_and(Links[i,2]==Lines[:,1], Links[i,3]==Lines[:,2])))
                            edgeCandidates = np.unique(Lines[ind,5])
                            for ii in range(len(edgeCandidates)):
                                ind2 = np.where(Lines[:,5]==edgeCandidates[ii])
                                Links[i,7]=np.nanmean(Lines[ind2,4]) #[l_1 x_1 y_1 z_1 Euc L k_1 mean(S)]
                                Links[i+1,7] = np.nanmean(Lines[ind2,4])
                                Links[i,8]=np.nanmin(Lines[ind2,4])  #[l_1 x_1 y_1 z_1 Euc L k_1 mean(S) min(S)]
                                Links[i+1,8]=np.nanmin(Lines[ind2,4])
                                Links[i,9]=np.nanmax(Lines[ind2,4])  #[l_1 x_1 y_1 z_1 Euc L k_1 mean(S) min(S) max(S)]
                                Links[i+1,9]=np.nanmax(Lines[ind2,4])
                                Links[i,10]=np.ptp(Lines[ind2,4])    #[l_1 x_1 y_1 z_1 Euc L k_1 mean(S) min(S) max(S) range(S)]
                                Links[i+1,10]=np.ptp(Lines[ind2,4])


                        with h5py.File('all-LinksFullBinned.hdf5','w') as f:
                            dset = f.create_dataset("default",data=Links)
#                        with h5py.File('all-LinksFullBinned.hdf5','r') as f:
#                            newfile = f.get('default').value #data is now an ndarray

# add ult source to top nodes/bottom nodes to ult target into adj matrix
                        Data = Links
# renumber node ID because shortestPath cannot handle nodes called "0", have to add "2" because of the added ultimate source and ultimate target paired rows
                        Data[:,0] += 1 
# finding the x values for ultimate source and ultimate target
                        #select x value for ultimate source
                        x_0=np.unique(np.min(Data[:,1]))-1
                        #select x value for ultimate target
                        x_00=np.unique(np.max(Data[:,1]))+1    
        
# find k values for ultimate source and ultimate target
                        #finding nodes connected to ultimate source
                        ind_top=np.where(Data[:,1]<=(np.min(Data[:,1])+diameter))  
                        #finding nodes connected to ultimate target
                        ind_bottom=np.where(Data[:,1]>=(np.max(Data[:,1])-diameter)) 
                        #node degree at new source
                        k_0=len(ind_top)                              
                        #node degree at new target
                        k_00=len(ind_bottom)                          
                        
# find ID (l_0 & l_00) for ultimate source and ultimate target
                        #node ID for source node
                        l_0=np.min(Data[:,0])-1
                        #node ID for target node                          
                        l_00=np.max(Data[:,0])+1                          
                        
# need to find all ind_top (and ind_bottom) & pair w/ ultimate source (and ultimate target)
                        #node IDs for top nodes
                        L_T = np.unique(Data[ind_top,0])
                        #node IDs for bottom nodes
                        L_B = np.unique(Data[ind_bottom,0])                
                        
# Now we need to add in the ultimate source to top nodes/bottom nodes to ultimate target into the adjacency matrix
                        for j in range(len(L_T)):
                            ind_T=np.where(Data[:,0]==L_T[j])
                            MT=np.array([[l_0, x_0[0], 1, 0, 1, 1, k_0, 1, 1, 1, 1],
                                [L_T[j], Data[ind_T[0][0],1],Data[ind_T[0][0],2],Data[ind_T[0][0],3], 1, 1, Data[ind_T[0][0],6], 1, 1, 1, 1],
                                [L_T[j], Data[ind_T[0][0],1],Data[ind_T[0][0],2],Data[ind_T[0][0],3], 1, 1, Data[ind_T[0][0],6], 1, 1, 1, 1],
                                [l_0, x_0[0], 1, 0, 1, 1, k_0, 1, 1, 1, 1]])
                            MT = np.append(MT, MT, axis=0)
                        Data = np.append(Data, MT, axis=0)
                        for jj in range(len(L_B)):
                            ind_B=np.where(Data[:,0]==L_B[jj])
                            MB=np.array([[l_00, x_00[0], 1, 0, 1, 1, k_00, 1, 1, 1, 1],
                                [L_B[jj], Data[ind_B[0][0],1],Data[ind_B[0][0],2],Data[ind_B[0][0],3], 1, 1, Data[ind_B[0][0],6], 1, 1, 1, 1],
                                [L_B[jj], Data[ind_B[0][0],1],Data[ind_B[0][0],2],Data[ind_B[0][0],3], 1, 1, Data[ind_B[0][0],6], 1, 1, 1, 1],
                                [l_00, x_00[0], 1, 0, 1, 1, k_00, 1, 1, 1, 1]])
                            MB = np.append(MB,MB,axis=0)
                        Data = np.append(Data,MB, axis=0)
                        with h5py.File('Data.hdf5','w') as f:
                            dset = f.create_dataset("default",data=Data)
#                        with h5py.File('Data.hdf5','r') as f:
#                            Datafile = f.get('default').value #data is now an ndarray
toc = time.time()
print('runtime =', toc-tic)