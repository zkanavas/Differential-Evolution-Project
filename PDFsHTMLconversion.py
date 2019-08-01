# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:46:58 2019

@author: zkana
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 26 12:05:16 2019

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
Experiment_Name = 'Structural Attributes PDFs'

bodystr = '<div class = "p-3"> <p>Shown below are the resulting probability density functions (PDFs) for each structural attribute. Figures 1, 2, & 3 contain the PDFs for each sample. Figure 4 is the PDF of the structural attribute information for all of the samples combined. <p> The structural attributes we can immediately identify as having littel to no variation include:' +'<strong> Arc Length, Euclidean, Min Thickness, Mean Thickness, Quino, Tortuosity, Volume, Poiseuille, and Node Degree. </strong>'+ '<p> The attributes with significant variation througout the samples include: <strong>  Max Thickness, Long & Thick, Widest Bottleneck, Euclidean & Thick, Straightness, and Aspect Ratio.</strong></p> </div>'
image1 = ('PDFs for Sat_0_71.png')
image2 = ('PDFs for Sat_0_77.png')
image3 = ('PDFs for Sat_0_83.png')
image4 = ('PDFs for all Sample Structures.png')
cap1 = 'Figure 1. PDFs for each structural attribute for the 71% saturated sample.'
cap2 = 'Figure 2. PDFs for each structural attribute for the 77% saturated sample.'
cap3 = 'Figure 3. PDFs for each structural attribute for the 83% saturated sample.'
cap4 = 'Figure 4. PDFs for each structural attribute for all of samples.'

imgstr1 = wrapcol('<div class = "text-center"><figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure></div>'.format(image1,cap1))
imgstr2 = wrapcol('<div class = "text-center"><figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure></div>'.format(image2,cap2))
imgstr3 = wrapcol('<div class = "text-center"><figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure></div>'.format(image3,cap3))
imgstr4 = wrapcol('<div class = "text-center"><figure class="figure"><img src="{0}" class="figure-img img-fluid rounded" alt="..."><figcaption class="figure-caption text-center">{1}</figcaption></figure></div>'.format(image4,cap4))


with open("PDFs.html", "w") as text_file:
    #the style to use
    text_file.write('<head><link rel="stylesheet" href="css/bootstrap.css"></head>')
    text_file.write('<div class="container-fluid">')
    text_file.write(wraprow(wrapcol('<h1 class="text-center">'+Experiment_Name+'</h1>')))
    for strings in [bodystr,imgstr1,imgstr2,imgstr3,imgstr4]:
        text_file.write(wraprow(strings))
    text_file.write('</div>')