#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 00:00:47 2020

@author: xinc4
"""

import os
import sys
import numpy as np
from pathlib import Path
np.set_printoptions(threshold=sys.maxsize)

mapCoords = {}
#mappedLocsDir = Path(r'..\Crime_Logs\Mapped_Locations')
mappedLocsDir = Path(r'./Union')

block_raw = np.loadtxt('BlockLocation.csv', delimiter = ',', skiprows = 1)
block = np.zeros((50, 8))
for i in range(50):
    block[int(block_raw[i,0]) - 1] = block_raw[i,1:] 

for File in os.listdir(mappedLocsDir):
    if(File.startswith('2')):
        with open(os.path.join(mappedLocsDir, File),'r', encoding="latin-1") as f:
            lines = f.readlines()
            num = len(lines)
            location = np.zeros((num,2))
            i = 0
            for line in lines:
                tok = line.split(':')
                #print(tok)
                if(len(tok)==4):
                    location[i,0] = float(tok[2].split(',')[0])
                    location[i,1] = float(tok[3].split('}')[0])
                    i += 1  
                elif (len(tok) > 2):
                    location[i,0] = float(tok[3].split(',')[0])
                    location[i,1] = float(tok[4].split('}')[0])
                    i += 1
                elif (len(tok) == 1):
                    num-=1
                    #print(tok)
                    # there may exist '\n' in some files
    
        index = np.zeros((num,1))
        for i in range(num):
            for j in range(50):
                if((location[i][0] < block[j][0]) & (location[i][0] > block[j][6]) 
                & (location[i][1] < block[j][3]) & (location[i][1] > block[j][1])):
                    index[i] = j + 1
                    break
                if(j == 49):
                    index[i] = 0
        np.savetxt(File + '.csv', index, fmt = '%f')
