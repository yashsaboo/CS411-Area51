# Script to ouput the locations not geocoded by GoogleMaps API

import os
import re
import csv
from pathlib import Path

# Dict of all locations in .csv
locs = {}
# Set of [potentially] incomplete geocoded locations
geocoded = set()
allCSVs = Path(r'..\Crime_Logs\CSV')
mappedLocsDir = Path(r'..\Crime_Logs\Mapped_Locations')

# Populate geocoded set w/ locations properly acquired by GoogleMaps API
for txtFile in os.listdir(mappedLocsDir):
    # Open mapped locations .txt file
    with open(os.path.join(mappedLocsDir, txtFile), 'r') as f:
        lines = f.readlines()
    # Populate set
    for l in lines:
        geocoded.add(l[: l.find(': ')])

    # Open corresponding .csv
    with open(os.path.join(allCSVs, txtFile[: -4] + '.csv'), 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        rowNum = 0
        for row in csv_reader:
            # If curr. line has a date in it, then add loc to set
            if re.match('\d.*/\d.*/\d.*', row[1]):
                if row[5] not in locs:
                    locs[row[5]] = [rowNum]
                else:
                    locs[row[5]] += [rowNum]
            rowNum += 1

    print('Locations missing from ' + txtFile + ': ')
    for l in locs:
        if l not in geocoded:
            print(l, ', ', locs[l])
    print('\n')

    # Reset
    locs.clear()
    geocoded.clear()
