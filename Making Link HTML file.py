# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 09:47:33 2019

@author: zkana
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def wraprow(stringin):
    return '<div class="row">' + stringin + '</div>'

def wrapcol(stringin):
    return '<div class="col">' + stringin + '</div>'

# specifiying the experiment that I am creating the HTML file for
Experiment_Name = 'Link Function'

# reading in the csv file that contains the results
df = pd.read_csv(Experiment_Name+'.csv',sep = ',',header = 0, index_col = 0)

#Norm_Weights = np.empty([len(df),14])
##making bar chart
##columns of interest
#colint = df.columns[14:]
##making a new dataframe WITHOUT the columns in colint
#newdf = df.drop(colint, axis = 1)
##summing all of the weights together
#summed_by_rows = np.sum(newdf, axis = 1)
##need to make two dataframes of the same shape to divide them
#d = {'col1': summed_by_rows, 'col2': summed_by_rows, 'col3': summed_by_rows, 
#     'col4': summed_by_rows, 'col5': summed_by_rows, 'col6': summed_by_rows,
#     'col7': summed_by_rows, 'col8': summed_by_rows, 'col9': summed_by_rows, 
#     'col10': summed_by_rows, 'col11': summed_by_rows, 'col12': summed_by_rows,
#     'col13': summed_by_rows, 'col14': summed_by_rows}
#divide_df = pd.DataFrame(data=d)
#Norm_Weight = (np.divide(newdf,divide_df))*100
#ax = Norm_Weight.plot(kind='barh',stacked = True,use_index = False, figsize=(15,7), colormap = 'tab20')
#ax.set_yticklabels(['identity','inverse','natural log','exp','inverse squared','inverse square root','logit','inverse logit'])
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=8)
#ax.set_xlabel('Relative Importance')
#ax.set_ylabel('Link Function')
#plt.savefig(Experiment_Name+'.png',bbox_inches='tight')

image1 = (Experiment_Name+'.png')
cap1 = "<strong> Figure 1. </strong> Relative Importance of each Structural Attribute for each Experiment"
imgstr1 = wrapcol('<div class = "text-center"><figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure></div>'.format(image1,cap1))

 #dividing up the dataframe to be more readable
colint2 = df.columns[:14]
newdf2 = (df.drop(colint2, axis = 1))
# creating the table of attributes & their weight
htmlstr1 = wrapcol(newdf.to_html(classes='table table-responsive table-striped table-hover'))
#creating the table of experiments & accuracies & runtimes
htmlstr2 = wrapcol(newdf2.to_html(classes='table table-responsive table-striped table-hover')) 

Tablestr1 = '<div class = "px-3"><h3> <strong> Table 1. </strong> Weight Assigned to Each Structural Attribute</h3></div>'
Tablestr2 = '<div class = "px-3"><h3> <strong> Table 2. </strong> Associated Accuracies and Runtime (in sec)</h3></div>'

Introstr = '<div class="px-3"><p>The purpose of this analysis is to understand how the results of the differential evolution algorithm respond to a nonlinear objective function. This is done by introducing a <em> link </em> function to the objective function - the function that defines the weighting scheme of the pore network. The objective function previously has been a simple linear combination of the structural attributes of interest. The following 8 link functions were tested:</p></div>'
Introstr2 = '<table class = "table table-striped"><thead><tr><th scope="col">Link Function</th><th scope="col">Objective Function Transformation</th></tr></thead><tbody> <tr> <td>Identity</td><td>obj = obj</td></tr><tr><td>Inverse</td><td> obj = obj<sup>-1</sup></td></tr><tr><td>Natural Log</td><td>obj = ln(obj)</td></tr><tr><td>exp</td><td>obj = e<sup>obj</sup></td></tr><tr><td>Inverse Squared</td><td>obj = obj<sup>-2</sup></td></tr><tr><td>Inverse Square Root</td><td> obj = obj<sup>-1/2</sup></td></tr><tr><td>Logit</td><td>obj = ln(obj/(1-obj))</td></tr><tr><td>Inverse Logit</td><td>obj = e<sup>obj</sup>/(1+e<sup>obj</sup>)</td></tr></tbody></table>'
Introstr3 = '<div class ="px-3"><p>This project uses the SciPy function: optimize.differential_evolution. The seed was kept constant at 1 to ensure experiment reproducibility; each structural attribute weight was bounded between 0 and 10; the recombination constant was set to 0.8; the mutation constant was the tuple (0.5,1) which employs dithering (dithering randomly changes the mutation constant on a generation by generation basis); the absolute tolerance was set to 0 and the relative tolerance was set to 0.01; the strategy was set to "best1bin"; polish was set to true meaning scipy.optimize.minimize is used to polish the best population member at the end, which can improve the minimization slightly; and the initial population was DR-All (the identity matrix with 10 along the diagonal). With those function input parameters set, the link function was changed for each experiment to compare the accuracy, runtime, and weights assigned to each structural parameter, as shown in Tables 1 & 2. </p> </div>'

Figstr = '<div class ="px-3"><p> </p></div>'

# shortest paths for each strategy
#bodystr1 = '<div class = "px-3"> <h3> Identity </h3> </div>'
#explainingstr1 = '<div class="px-3"><p>The "Best1Bin" strategy combines the best current solution vector with two random vectors from the population to make the mutated vector and is described by the following equation:</p> <p>x<sub>mut</sub>=x<sub>best</sub>+M(x<sub>rand1</sub>-x<sub>rand2</sub>) </p><p> where M is the mutation constant. </p></div>'
#img1 = (Experiment_Name+'best1binSat_0_71.png')
#img2 = (Experiment_Name+'best1binSat_0_77.png')
#img3 = (Experiment_Name+'best1binSat_1_00.png')
#cap1 = "Resulting Shortest Path for 71% Saturated Sample"
#cap2 = "Resulting Shortest Path for 77% Saturated Sample"
#cap3 = "Resulting Shortest Path for 100% Saturated Sample"
#imgstr2 = ''
#for image,caption in zip([img1,img2,img3],[cap1,cap2,cap3]):
#    imgstr2 += wrapcol('<figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure>'.format(image,caption))
#
#bodystr2 = '<div class = "px-3"> <h3> Best2Bin Strategy </h3> </div>'
#explainingstr2 = '<div class="px-3"><p>The "Best2Bin" strategy combines the best current solution vector with four random vectors from the population to make the mutated vectorand is described by the following equation:</p> <p>x<sub>mut</sub>=x<sub>best</sub>+M(x<sub>rand1</sub>-x<sub>rand2</sub>+x<sub>rand3</sub>-x<sub>rand4</sub>) </p><p> where M is the mutation constant. </p></div>'
#img4 = (Experiment_Name+'best2binSat_0_71.png')
#img5 = (Experiment_Name+'best2binSat_0_77.png')
#img6 = (Experiment_Name+'best2binSat_1_00.png')
#cap4 = "Resulting Shortest Path for 71% Saturated Sample"
#cap5 = "Resulting Shortest Path for 77% Saturated Sample"
#cap6 = "Resulting Shortest Path for 100% Saturated Sample"
#imgstr3 = ''
#for image,caption in zip([img1,img2,img3],[cap1,cap2,cap3]):
#    imgstr3 += wrapcol('<figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure>'.format(image,caption))
#
#bodystr3 = '<div class = "px-3"> <h3> RandtoBest1Bin Strategy </h3> </div>'
#explainingstr3 = '<div class="px-3"><p>The "RandtoBest1Bin" strategy is similar to "Best2Bin" in that 4 random vectors are combined with the best current solution vector, but two mutation constants are required and is described by the following equation:</p> <p>x<sub>mut</sub>=x<sub>rand1</sub>+M<sub>1</sub>(x<sub>rand2</sub>-x<sub>rand3</sub>)+M<sub>2</sub>(x<sub>best</sub>-x<sub>rand1</sub>) </p><p> where M<sub>1</sub> and M<sub>2</sub> are the mutation constants. </p> </div>'
#img7 = (Experiment_Name+'randtobest1binSat_0_71.png')
#img8 = (Experiment_Name+'randtobest1binSat_0_77.png')
#img9 = (Experiment_Name+'randtobest1binSat_1_00.png')
#cap7 = "Resulting Shortest Path for 71% Saturated Sample"
#cap8 = "Resulting Shortest Path for 77% Saturated Sample"
#cap9 = "Resulting Shortest Path for 100% Saturated Sample"
#imgstr4 = ''
#for image,caption in zip([img1,img2,img3],[cap1,cap2,cap3]):
#    imgstr4 += wrapcol('<figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure>'.format(image,caption))
#

with open("Website_Uploads/"+Experiment_Name+".html", "w") as text_file:
    #the style to use
    text_file.write('<head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></head>')
    text_file.write('<div class="container-fluid">')
    text_file.write(wraprow(wrapcol('<h1 class="text-center">'+Experiment_Name+'</h1>')))
    for strings in [Introstr,Introstr2,Introstr3,Tablestr1,htmlstr1,imgstr1,Figstr,Tablestr2,htmlstr2]:
        text_file.write(wraprow(strings))
    text_file.write('</div>')

import os
from ftplib import FTP
user = 'zkanavas@jasondekarske.com'
passwd = 'vinny is a dog'
with FTP('ftp.jasondekarske.com') as f: #connect to host, default port
    f.login(user=user,passwd=passwd)
    for root,_,files in os.walk("Website_Uploads"):
        for name in files:
            fullname = os.path.join(os.getcwd(),root,name)
            f.storbinary('STOR {}'.format(os.path.join('zoe/',name)),open(fullname, 'rb'))