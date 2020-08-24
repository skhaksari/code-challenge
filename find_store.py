"""Find Store.

Usage:
  find_store.py --address="<address>"
  find_store.py --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store.py --zip=<zip>
  find_store.py --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>            Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)        Display units in miles or kilometers [default: mi]
  --output=(text|json)   Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]
  
"""

from docopt import docopt
from geopy.geocoders import Nominatim
import csv
import sys
import pgeocode
import math

'''if __name__ == '__main__':'''

def printclosest(row):
    print('The closest store is at ' + row['Store Name'] + ' at' + row['Address'] + ', ' + row['City']
    + ', ' + row['State'] + ' ' + row['Zip Code'])
def calcdist(lat1, long1, lat2, long2):
  R = 6372800
  phi1, phi2 = math.radians(lat1), math.radians(lat2)
  dphi = math.radians(lat2 - lat1)
  dlambda = math.radians(long2-long1)
  a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
  return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def zip(zipcode):
  with open('store-locations.csv') as store_locations:
    reader = csv.DictReader(store_locations)
    distdict = {}
    for row in reader:
      dist = pgeocode.GeoDistance('US')
      distdict[row['Zip Code']] = dist.query_postal_code(zipcode, row['Zip Code'][0:5])
    min_value = min(distdict.values())
    min_list = [key for key, value in distdict.items() if value == min_value]
    for row in filter(min_list[0] in row.values(), reader): 
      printclosest(row)

def addr(address):
  with open('store-locations.csv') as store_locations:
    reader = csv.DictReader(store_locations)
    distdict = {}
    geolocator = Nominatim(user_agent="find_store")
    for row in reader:
      coords = geolocator.geocode(address)
      distdict[row['Store Name']] = calcdist(coords.latitude, coords.longitude, row['Latitude'], row['longitude'])
    min_value = min(distdict.values())
    min_list = [key for key, value in distdict.items() if value == min_value]
    for row in filter(min_list[0] in row.values(), reader): 
      printclosest(row)
      

arguments = docopt(__doc__)
print(arguments)
if arguments['--zip'] is not None:
  zip(arguments['--zip'])
if arguments['--address'] is not None:
  addr(arguments['-address'])