#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:01:56 2020

@author: xinc4
"""

import os
import sys
import csv
import numpy as np
from pathlib import Path
from random import random
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
np.set_printoptions(threshold=sys.maxsize)

mapCoords = {}
#mappedLocsDir = Path(r'..\Crime_Logs\Mapped_Locations')
mappedLocsDir = Path(r'./')


count = np.zeros((51,7))
year = 0

for File in os.listdir(mappedLocsDir):
    if(File.startswith('2')):
        with open(os.path.join(mappedLocsDir, File),'r', encoding="latin-1") as f:
            f.readline()
            lines = f.readlines()
            for line in lines:
                tok = line.split(',')
                index = int(tok[-1].strip('\n'))
                for i in range(51):
                    if(i == index):
                        count[i, year] += 1
        year+=1

                #print(tok[2].split(',')[0])
                #print(tok[3].split('}')[0])
    
with open('prediction.csv','w', encoding = "latin-1") as f:
    csvwriter = csv.writer(f, delimiter = ',',)
    csvwriter.writerow(['BlockId', '2013 CrimeCount', '2014 CrimeCount', '2015 CrimeCount', '2016 CrimeCount'
                        , '2017 CrimeCount', '2018 CrimeCount', '2019 CrimeCount', 'Prediction CrimeCount'])
    for i in range(51):
        #data = [count[i,0], count[i,1], count[i,2], count[i,3], count[i,4], count[i,5], count[i,6]]
        data = count[i]
        if(data.sum() != 0):
            # fit model
            # fit model
            model = ARMA(data, order=(0, 1))
            model_fit = model.fit(disp=False)
            # make prediction
            predict = model_fit.predict(len(data), len(data))
        else:
            predict = [0]
        csvwriter.writerow([i, int(count[i,0]), int(count[i,1]), int(count[i,2]), int(count[i,3])
        , int(count[i,4]), int(count[i,5]), int(count[i,6]), int(predict[0])])
