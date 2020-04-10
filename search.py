#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:42:41 2020

@author: xinc4
"""

import numpy as np

def search(lat, lon):
    block_raw = np.loadtxt('BlockLocation.csv', delimiter = ',', skiprows = 1)
    block = np.zeros((50, 8))
    for i in range(50):
        block[int(block_raw[i,0]) - 1] = block_raw[i,1:] 
    
    index = 0
    for j in range(50):
        if((lat < block[j][0]) & (lat > block[j][6]) 
        & (lon < block[j][3]) & (lon > block[j][1])):
            index = j + 1
    print(index)
    return index

search(40.1065086, -88.22124749999999)

        