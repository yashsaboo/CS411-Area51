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
                    if(i==index):
                        count[i, year]+=1
        year+=1

                #print(tok[2].split(',')[0])
                #print(tok[3].split('}')[0])
    
with open('count.csv','w', encoding="latin-1") as f:
    csvwriter = csv.writer(f, delimiter=',',)
    csvwriter.writerow(['BlockId', '2013 CrimeCount', '2014 CrimeCount', '2015 CrimeCount', '2016 CrimeCount'
                        , '2017 CrimeCount', '2018 CrimeCount', '2019 CrimeCount', 'Total CrimeCount'])
    for i in range(51):
        csvwriter.writerow([i, count[i,0], count[i,1], count[i,2], count[i,3], count[i,4], count[i,5], count[i,6], sum(count[i])])
        