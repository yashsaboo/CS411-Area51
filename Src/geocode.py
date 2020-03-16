import googlemaps
import config
from docx.api import Document
from datetime import datetime

gmaps = googlemaps.Client(key=config.api_key)

# Open .doc(x) file and get 'General location' col (col # 5)
doc = Document(r'Crime_Logs\2013.docx')
table = doc.tables[0]
for row in table.rows:
    for cell in row.cells:
        print(cell.text)

# Geocoding an address
# geocode_result = gmaps.geocode('506 West Springfield Ave., Champaign')
# print(geocode_result[0]['geometry']['location'])
