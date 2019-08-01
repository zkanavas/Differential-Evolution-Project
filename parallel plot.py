# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 14:59:50 2019

@author: zkana
"""
import numpy as np 
import matplotlib.pyplot as plt
Sat_71 = np.array([0.864833372,0.398914518,0.021164021,0.029917436,0.923076923,1,1])
Sat_77 = np.array([0.526139983,0.94843962,0,0.002953525,1,0.010423939,0.871794872])
Sat_83 = np.array([0,1,0.649029982,1,0,0.101595225,0.58974359])
Sat_100= np.array([1,0,1,0,0.171153846,0,0])
plt.plot(Sat_71,label = 'Sat 71%',marker ='o')# linewidth=4, marker ='o')
plt.plot(Sat_77,label = 'Sat 77%',marker ='o')# linewidth=4,marker ='o')
plt.plot(Sat_83, label = 'Sat 83%',marker ='o')# linewidth=4,marker ='o')
plt.plot(Sat_100,label = 'Sat 100%',marker ='o')# linewidth=4,marker ='o')
plt.gca().set_xticks(range(7))
plt.legend(fontsize=15, loc='lower right', bbox_to_anchor=(1, 0.09))
plt.grid(False)
plt.gca().set_xticklabels(['Arc Length','Euclidean Distance','Thin Channels','Thick Channels','Long&Thick Channels','Widest Bottleneck', 'Accuracy'], fontsize=15)
plt.gca().set_yticklabels([0,'0.0','0.2','0.4','0.6','0.8','1.0'],fontsize=15)
plt.show()
