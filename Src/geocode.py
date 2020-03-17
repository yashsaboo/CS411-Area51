import os
import re
import csv
import time
import json
import config
import googlemaps
from pathlib import Path
from datetime import datetime

# Enter Google Maps API
gmaps = googlemaps.Client(key=config.api_key)

# Open .csv
mapCoords = {}
allCSVs = Path(r'..\Crime_Logs\CSV')
mappedLocsDir = Path(r'..\Crime_Logs\Mapped_Locations')

for csvFile in os.listdir(allCSVs):
    with open(os.path.join(allCSVs, csvFile), 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            # If curr. line has a date in it, then look for location entry
            if re.match('\d.*/\d.*/\d.*', row[1]):
                # print(row[5])
                if row[5] not in mapCoords:
                    # Add geocoded loc to dict
                    coords = None
                    # If API call fails (due to dynamically set IP), retry
                    retry = 0
                    while not coords and retry <= 5:
                        try:
                            coords = gmaps.geocode(row[5] + ', Champaign')
                        except googlemaps.exceptions.ApiError:
                            pass
                        retry += 1
                        print('retrying...', retry)
                    if retry == 5:
                        continue

                    # Add to dict if result of geocode is not empty
                    if coords:
                        mapCoords[row[5]] = coords[0]['geometry']['location']
                    else:
                        continue
                    # Write dict entry to file
                    with open(os.path.join(mappedLocsDir, csvFile[:-4] + '.txt'), 'a') as f2:
                        f2.write(row[5] + ': ' +
                                 json.dumps(mapCoords[row[5]]) + '\n')
                    # time.sleep(1)


# Geocoding an address
# geocode_result = gmaps.geocode('506 West Springfield Ave., Champaign')
# print(geocode_result[0]['geometry']['location'])
