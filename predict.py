#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:01:56 2020

@author: xinc4
"""

import os
import math
import sys
import csv
import copy
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
        data = copy.copy(count[i])
        if(data.sum() > 10 and data.min() > 0):
            data1 = data[[0, 2, 4, 6]]
            mean1 = data1.mean()
            mean2 = data.mean()
            std1 = np.std(data1)
            std2 = np.std(data)
            # the criteria of stationary here
            if((mean1 / mean2 < 0.75) or (mean1 / mean2 > 1.25) or
            (std1/ std2 < 0.75) or (std1/ std2 > 1.25)):
                # NUM of blocks which don't satisfy stationary condition
                num += 1
    print("Num of unqualified blocks is ", num)
    num = 0
    for i in range(51):
        data = copy.copy(count[i])
        if(data.sum() > 10 and data.min() > 0):
            temp1 = data[0]
            temp2 = data[1]
            #for i in range(len(data) - 1):
            #    data[i] = (np.log(data[i+1]) - np.log(data[i]))
            #data[len(data) - 1] = (np.log(temp) - np.log(data[len(data) - 1]))
            #data = np.log(data)

            # for i in range(len(data) - 2):
            #     data[i] = np.log(data[i + 2]) + np.log(data[i + 1]) + np.log(data[i])
            #data[len(data) - 1] = np.log(temp1) + np.log(temp2) + np.log(data[len(data) - 1])
            #data[len(data) - 2] = np.log(temp1) + np.log(data[len(data) - 1]) + np.log(data[len(data) - 2])

            for i in range(len(data) - 2):
                data[i] = pow(data[i + 2], 0.5) + pow(data[i + 1], 0.5) + pow(data[i], 0.5)
            data[len(data) - 1] = pow(temp1, 0.5) + pow(temp2, 0.5) + pow(data[len(data) - 1], 0.5)
            data[len(data) - 2] = pow(temp1, 0.5) + pow(data[len(data) - 1], 0.5) + pow(data[len(data) - 2], 0.5)


            #data = np.log(data)
            #data = pow(data, 0.000000000001)
            data1 = data[[0, 2, 4, 6]]
            mean1 = data1.mean()
            mean2 = data.mean()
            std1 = np.std(data1)
            std2 = np.std(data)
            if((mean1 / mean2 < 0.75) or (mean1 / mean2 > 1.25) or
            (std1/ std2 < 0.75) or (std1/ std2 > 1.25)):
                # NUM of blocks which don't satisfy stationary condition
                num += 1
    print("Num of unqualified blocks is ", num)
    
    for i in range(51):
        #data = [count[i,0], count[i,1], count[i,2], count[i,3], count[i,4], count[i,5], count[i,6]]
        data = copy.copy(count[i])
        #print(data)
        if(data.sum() > 10 and data.min() > 0):
            temp1 = data[0]
            temp2 = data[1]
            for j in range(len(data) - 2):
                data[j] = pow(data[j + 2], 0.5) + pow(data[j + 1], 0.5) + pow(data[j], 0.5)
            data[len(data) - 1] = pow(temp1, 0.5) + pow(temp2, 0.5) + pow(data[len(data) - 1], 0.5)
            data[len(data) - 2] = pow(temp1, 0.5) + pow(data[len(data) - 1], 0.5) + pow(data[len(data) - 2], 0.5)
            #print(data)
            model = ARMA(data, order=(0, 1))
            model_fit = model.fit(disp=False)
            # make prediction
            predict = model_fit.predict(len(data), len(data))
            #print(predict)
            predict = pow(max((predict - pow(temp1, 0.5) - pow(temp2, 0.5)), 0), 2)
            # Draw the trend of crime
            """data_new = np.hstack([data, predict])
            data, temp, con = model_fit.forecast(2, alpha=0.05)
            series1 = pd.Series(data_new, [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
            series2 = pd.Series(data, [2020, 2021])
            # lower boundary of prediction
            lower = pd.Series(con[:, 0], [2020, 2021])
            # higher boundary of prediction
            upper = pd.Series(con[:, 1], [2020, 2021])
            plt.figure(figsize=(12,6))
            plt.plot(series1, label='previous')
            plt.plot(series2, label='prediction')
            plt.fill_between(lower.index, lower, upper, alpha=.2)
            plt.legend(loc='upper left', fontsize=10)
            plt.xlabel('Year')
            plt.ylabel('Crime Count')
            plt.show()
            plt.title('Count of Crimes')"""
        else:
            predict = [int(data.sum() / 7)]
        csvwriter.writerow([i, int(count[i,0]), int(count[i,1]), int(count[i,2]), int(count[i,3])
        , int(count[i,4]), int(count[i,5]), int(count[i,6]), int(predict[0])])
