import film

import logging

logging.getLogger('film').setLevel(logging.DEBUG)
logging.basicConfig()

f = film.Film('Carnosaur', '1993')
print()
f = film.Film('Carnosaur', '1994')
print()
