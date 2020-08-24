# Grove coding challenge
------
This repo is my solution to the Grove coding challenge, as described in [this readme](https://github.com/groveco/code-challenge). This coding challenge asks the participant to create a CLI that allows for a user to find the closest store (provided in a CSV file of stores) to the entered zip code or address. 

Solution description
-----
My approach in this solution was to write this in Python, since docopt is mainly employed in Python, and so that command argument parsing would become easier. Once I was able to use docopt to parse the commands, I then took the command arguments and passed them through methods depending on whether the user put an address or a zipcode. I also used helper methods to calculate distance based on whether the units were in miles or kilometers, and to print the distance between the closest store and the user input zipcode or address in JSON or through text. In order to calculate distance between two coordinates, I used the Haversine formula implementation as described in [this blog](https://janakiev.com/blog/gps-points-distance-python/). For zipcode, I did not use coordinates, since zipcodes often describe a geographical area as opposed to a specific set of coordinates, and for this, I used the [pgeocode library](https://pypi.org/project/pgeocode/), which is also required to run this code. 

Assumptions that were made while writing this code are that the address/zipcode that the user will enter are US-based, and that the user will enter a valid address. Another assumption that was made while writing this code was that the program will terminate after printing the closest store location, and will not continue to run after printing the store. In printing the store location, I chose to only include the store name and address, and not the location, latitude, longitude, or county, as my assumption would be that such information might seem extraneous to a user who wants to find the closest store. Some caveats to this program are that in the interest of time, unfortunately, I did not have runtime in mind, or runtime optimization, and coded mainly for functionality, so the code takes an extremely long time to run, given that the CSV file is over 1000 lines long. This code is also written in Python 3, and in order for it to run properly, needs to have the following libraries installed:
* [docopt](https://pypi.org/project/docopt/)
* [pgeocode](https://pypi.org/project/pgeocode/)
* [geopy](https://pypi.org/project/geopy/)

In order to run this program, clone this repository, navigate to the directory the repository is in, and as an example, run the following command:
```
python3 find_store.py  --address="2401 Honeysuckle Rd, Chapel Hill, NC 27514"
```
