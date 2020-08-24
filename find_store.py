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
import json

'''if __name__ == '__main__':'''

def printclosest(row,output):
  if output == "json":
    print(json.dumps(row))
  else:
    print('The closest store is at ' + row['Store Name'] + ' at ' + row['Address'] + ', ' + row['City']
    + ', ' + row['State'] + ' ' + row['Zip Code'])
def distunits(units, dist):
  if units == 'mi':
    return dist * 0.621371
def calcdist(lat1, long1, lat2, long2): #based on the Haversine formula implementation found on this blog: https://janakiev.com/blog/gps-points-distance-python/
  R = 6372800
  lat2, long2 = float(lat2), float(long2)
  phi1, phi2 = math.radians(lat1), math.radians(lat2)
  dphi = math.radians(lat2 - lat1)
  dlambda = math.radians(long2-long1)
  a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
  return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def zip(zipcode, units, output):
  with open('store-locations.csv') as store_locations:
    reader = csv.DictReader(store_locations)
    distdict = {}
    minrow = {}
    min_list = []
    for row in reader:
      dist = pgeocode.GeoDistance('US')
      distdict[row['Zip Code']] = dist.query_postal_code(zipcode, row['Zip Code'][0:5])
    min_value = min(distdict.values())
    min_list = [key for key, value in distdict.items() if value == min_value]
    store_locations.seek(0)
    print(min_list[0])
    for row in reader: 
      if min_list[0] == row['Zip Code']:
        minrow = row
        break
    printclosest(minrow, output)

def addr(address, units, output):
   with open('store-locations.csv') as store_locations:
    reader = csv.DictReader(store_locations)
    distdict = {}
    minrow = {}
    min_list = []
    geolocator = Nominatim(user_agent="find_store")
    for row in reader:
      coords = geolocator.geocode(address)
      distdict[row['Store Name']] = calcdist(coords.latitude, coords.longitude, row['Latitude'], row['Longitude'])
    min_value = min(distdict.values())
    min_list = [key for key, value in distdict.items() if value == min_value]
    store_locations.seek(0)
    for row in reader:
      if min_list[0] == row['Store Name']:
        minrow = row
        break
    printclosest(minrow, output)
      

arguments = docopt(__doc__)
if arguments['--zip'] is not None:
  zip(arguments['--zip'], arguments['--units'], arguments['--output'])
if arguments['--address'] is not None:
  addr(arguments['--address'], arguments['--units'], arguments['--output'])