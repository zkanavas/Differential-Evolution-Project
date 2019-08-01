# -*- coding: utf-8 -*-
"""
Created on Thu May 30 09:04:23 2019

@author: zkana
"""
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

Saturation = ['Sat_0_83','Sat_0_77','Sat_0_71']

for z in range(len(Saturation)):
    Sat = Saturation[z]
    file = sio.loadmat(Sat + '/Data.mat')
    Data = file['Data']
    
    l_1 = Data[0::2,0]
    meanWidth = Data[0::2,7]
    inv_meanWidth = 1/meanWidth
    arcLength = Data[0::2,5]
    Euclidean = Data[0::2,4]
    min_Width = Data[0::2,8]
    inv_min_Width = 1/min_Width
    l_2 = Data[1::2,0]
    
    H_arcL = arcLength
    if z == 0:
        Arc_Length_Sat_0_81 = H_arcL
    if z == 1:
        Arc_Length_Sat_0_77 = H_arcL
    if z == 2:
        Arc_Length_Sat_0_71 = H_arcL
    
    H_Euc = Euclidean
    for p in range(len(H_Euc)):
        if H_Euc[p] == 0:
            H_Euc[p] = 4e-5
            H_Euc = H_Euc
    if z == 0:
        Euc_Sat_0_81 = H_Euc
    if z == 1:
        Euc_Sat_0_77 = H_Euc
    if z == 2:
        Euc_Sat_0_71 = H_Euc
    
    H_Thin = min_Width
    if z == 0:
        Thin_Sat_0_81 = H_Thin
    if z == 1:
        Thin_Sat_0_77 = H_Thin
    if z == 2:
        Thin_Sat_0_71 = H_Thin
    
    H_MeanWidth = meanWidth
    if z == 0:
        MeanWidth_Sat_0_81 = H_MeanWidth
    if z == 1:
        MeanWidth_Sat_0_77 = H_MeanWidth
    if z == 2:
        MeanWidth_Sat_0_71 = H_MeanWidth
        
    H_Thick = inv_meanWidth
    if z == 0:
        Thick_Sat_0_81 = H_Thick
    if z == 1:
        Thick_Sat_0_77 = H_Thick
    if z == 2:
        Thick_Sat_0_71 = H_Thick
        
    H_LT = (arcLength)*(inv_meanWidth)
    if z == 0:
        LT_Sat_0_81 = H_LT
    if z == 1:
        LT_Sat_0_77 = H_LT
    if z == 2:
        LT_Sat_0_71 = H_LT
    
    H_widBot = inv_min_Width
    if z == 0:
        widBot_Sat_0_81 = H_widBot
    if z == 1:
        widBot_Sat_0_77 = H_widBot
    if z == 2:
        widBot_Sat_0_71 = H_widBot
    
    H_EucThick = (Euclidean)*(inv_meanWidth)
    if z == 0:
        EucThick_Sat_0_81 = H_EucThick
    if z == 1:
        EucThick_Sat_0_77 = H_EucThick
    if z == 2:
        EucThick_Sat_0_71 = H_EucThick   
        
    H_Quino = np.exp(-1/meanWidth)
    if z == 0:
        Quino_Sat_0_81 = H_Quino
    if z == 1:
        Quino_Sat_0_77 = H_Quino
    if z == 2:
        Quino_Sat_0_71 = H_Quino  
        
    H_Tortuosity = (arcLength/Euclidean)**2
    if z == 0:
        Tortuosity_Sat_0_81 = H_Tortuosity
    if z == 1:
        Tortuosity_Sat_0_77 = H_Tortuosity
    if z == 2:
        Tortuosity_Sat_0_71 = H_Tortuosity
    
    H_Straightness = 1/H_Tortuosity
    if z == 0:
        Straightness_Sat_0_81 = H_Straightness
    if z == 1:
        Straightness_Sat_0_77 = H_Straightness
    if z == 2:
        Straightness_Sat_0_71 = H_Straightness

    H_Volume = arcLength*(min_Width**2)*np.pi
    if z == 0:
        Volume_Sat_0_81 = H_Volume
    if z == 1:
        Volume_Sat_0_77 = H_Volume
    if z == 2:
        Volume_Sat_0_71 = H_Volume

    H_AspectRatio = arcLength/min_Width
    if z == 0:
        AspectRatio_Sat_0_81 = H_AspectRatio
    if z == 1:
        AspectRatio_Sat_0_77 = H_AspectRatio
    if z == 2:
        AspectRatio_Sat_0_71 = H_AspectRatio
    
    H_Poiseuille = (meanWidth**4)/arcLength
    if z == 0:
        Poiseuille_Sat_0_81 = H_Poiseuille
    if z == 1:
        Poiseuille_Sat_0_77 = H_Poiseuille
    if z == 2:
        Poiseuille_Sat_0_71 = H_Poiseuille
    
    H_Connectivity = Data[0::2,6]
    if z == 0:
        Connectivity_Sat_0_81 = H_Connectivity
    if z == 1:
        Connectivity_Sat_0_77 = H_Connectivity
    if z == 2:
        Connectivity_Sat_0_71 = H_Connectivity

    for i in range(len(H_Euc)):
        if H_Euc[i] == 0:
            print (i)
    
#    plt.figure(figsize=(15, 10))
#    plt.suptitle(Sat)
#    metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Euclidean & Thick','Quino','Tortuosity','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']
#    Structural_Attributes = [H_arcL,H_Euc,H_Thin,H_MeanWidth,H_Thick,H_LT,H_widBot,H_EucThick,H_Quino,H_Tortuosity,H_Straightness,H_Volume,H_AspectRatio,H_Poiseuille, H_Connectivity]
#    for i in range(len(Structural_Attributes)):
#        plt.subplot(5,3,i+1)
#        plt.subplots_adjust(hspace = 0.5)
#        sns.distplot(Structural_Attributes[i], hist=True, kde=True, 
#                 bins=int(180/5), color = 'blue', 
#                 hist_kws={'edgecolor':'black'},
#                 kde_kws={'linewidth': 2, 'color': 'black'})
#        plt.title('PDF for '+metrics[i])
#        plt.savefig('PDFs for '+Sat+'.png',bbox_inches='tight')

#Arc_Length = np.concatenate((Arc_Length_Sat_0_71,Arc_Length_Sat_0_77,Arc_Length_Sat_0_81),axis = 0)
#Euclidean = np.concatenate((Euc_Sat_0_71,Euc_Sat_0_77,Euc_Sat_0_81),axis = 0)
#Thin = np.concatenate((Thin_Sat_0_71,Thin_Sat_0_77,Thin_Sat_0_81),axis = 0)
#Thick = np.concatenate((Thick_Sat_0_71,Thick_Sat_0_77,Thick_Sat_0_81),axis = 0)
#MeanWidth = np.concatenate((MeanWidth_Sat_0_71,MeanWidth_Sat_0_77,MeanWidth_Sat_0_81),axis = 0)
#LT = np.concatenate((LT_Sat_0_71,LT_Sat_0_77,LT_Sat_0_81),axis = 0)
#EucThick = np.concatenate((EucThick_Sat_0_71,EucThick_Sat_0_77,EucThick_Sat_0_81),axis = 0)
#widBot = np.concatenate((widBot_Sat_0_71,widBot_Sat_0_77,widBot_Sat_0_81),axis = 0)
#Quino = np.concatenate((Quino_Sat_0_71,Quino_Sat_0_77,Quino_Sat_0_81),axis = 0)
#Tortuosity = np.concatenate((Tortuosity_Sat_0_71,Tortuosity_Sat_0_77,Tortuosity_Sat_0_81),axis = 0)
#Straightness = np.concatenate((Straightness_Sat_0_71,Straightness_Sat_0_77,Straightness_Sat_0_81),axis = 0)
#Volume = np.concatenate((Volume_Sat_0_71,Volume_Sat_0_77,Volume_Sat_0_81),axis = 0)
#AspectRatio = np.concatenate((AspectRatio_Sat_0_71,AspectRatio_Sat_0_77,AspectRatio_Sat_0_81),axis = 0)
#Poiseuille = np.concatenate((Poiseuille_Sat_0_71,Poiseuille_Sat_0_77,Poiseuille_Sat_0_81),axis = 0)
#NodeDegree = np.concatenate((Connectivity_Sat_0_71,Connectivity_Sat_0_77,Connectivity_Sat_0_81),axis = 0)


#plt.figure(figsize=(15, 10))
#plt.suptitle('All Sample Structures')
#metrics = ['Arc Length','Euclidean','Min Thickness','Mean Thickness','Max Thickness','Long & Thick','Widest Bottleneck','Euclidean & Thick','Quino','Tortuosity','Straightness','Volume','Aspect Ratio','Poiseuille','Node Degree']
#Structural_Attributes = [Arc_Length,Euclidean,Thin,MeanWidth,Thick,LT,widBot,EucThick,Quino,Tortuosity,Straightness,Volume,AspectRatio,Poiseuille,NodeDegree]
#for i in range(len(Structural_Attributes)):
#    plt.subplot(5,3,i+1)
#    plt.subplots_adjust(hspace = 0.5)
#    sns.distplot(Structural_Attributes[i], hist=True, kde=True, 
#             bins=int(180/5), color = 'blue', 
#             hist_kws={'edgecolor':'black'},
#             kde_kws={'linewidth': 2, 'color': 'black'})
#    plt.title('PDF for '+metrics[i])
#    plt.savefig('PDFs for all Sample Structures.png',bbox_inches='tight')