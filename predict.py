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
import pandas as pd
from pathlib import Path
from random import random
import matplotlib.pyplot as plt
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
    num = 0
    csvwriter = csv.writer(f, delimiter = ',',)
    csvwriter.writerow(['BlockId', '2013 CrimeCount', '2014 CrimeCount', '2015 CrimeCount', '2016 CrimeCount'
                        , '2017 CrimeCount', '2018 CrimeCount', '2019 CrimeCount', 'Prediction CrimeCount'])
    for i in range(51):
        #data = [count[i,0], count[i,1], count[i,2], count[i,3], count[i,4], count[i,5], count[i,6]]
        data = count[i]
        if(data.sum() != 0):
            # fit model
            # fit model
            data1 = data[[0, 2, 4, 6]]
            data2 = data[[1, 3, 5]]
            mean1 = data1.mean()
            mean2 = data2.mean()
            std1 = np.std(data1)
            std2 = np.std(data2)
            if((2 * abs(mean1 - mean2) / (mean1 + mean2) > 0.5) or (2 * abs(std1 - std2) / (std1 + std2) > 0.5)):
                num += 1
            model = ARMA(data, order=(0, 1))
            model_fit = model.fit(disp=False)
            # make prediction
            predict = model_fit.predict(len(data), len(data))
            """data_new = np.hstack([data, predict])
            fc, se, conf = model_fit.forecast(2, alpha=0.05)
            tr_series = pd.Series(data_new, [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
            pr_series = pd.Series(fc, [2020, 2021])
            lower_series = pd.Series(conf[:, 0], [2020, 2021])
            upper_series = pd.Series(conf[:, 1], [2020, 2021])
            
            # Plot
            plt.figure(figsize=(12,5), dpi=100)
            plt.plot(pr_series, label='prediction')
            plt.plot(tr_series, label='previous')
            plt.fill_between(lower_series.index, lower_series, upper_series, 
                             color='k', alpha=.15)
            plt.title('Count of Crimes')
            plt.xlabel('Year')
            plt.ylabel('Crime Count')
            plt.legend(loc='upper left', fontsize=8)
            plt.show()"""
        else:
            predict = [0]
        csvwriter.writerow([i, int(count[i,0]), int(count[i,1]), int(count[i,2]), int(count[i,3])
        , int(count[i,4]), int(count[i,5]), int(count[i,6]), int(predict[0])])
    print(num)
