# Grove coding challenge
------
This repo is my solution to the Grove coding challenge, as described in [this readme](https://github.com/groveco/code-challenge). This coding challenge asks the participant to create a CLI that allows for a user to find the closest store (provided in a CSV file of stores) to the entered zip code or address. 

Solution description
-----
My approach in this solution was to write this in Python, since docopt is mainly employed in Python, and so that command argument parsing would become easier. Once I was able to use docopt to parse the commands, I then took the command arguments and passed them through methods depending on whether the user put an address or a zipcode. I also used helper methods to calculate distance based on whether the units were in miles or kilometers, and to print the distance between the closest store and the user input zipcode or address in JSON or through text. In order to calculate distance between two coordinates, I used the Haversine formula implementation as described in [this blog](https://janakiev.com/blog/gps-points-distance-python/). For zipcode, I did not use coordinates, since zipcodes often describe a geographical area as opposed to a specific set of coordinates, and for this, I used the [pgeocode library](https://pypi.org/project/pgeocode/), which is also required to run this code. 
