import dbclient

import logging

logger = logging.getLogger(__name__)

class Collection:
    def __init__(self):
        self._collection = dbclient.database()['info']

    def get_all(self):
        return dbclient.get_all(self._collection)

    def get(self, title, year=None, imdb_id=None):
        if imdb_id:
            return dbclient.get_by_imdb_id(self._collection, imdb_id)
        if year:
            return dbclient.get_by_title_and_year(self._collection, title=title, year=year)
        return dbclient.get_by_title(self._collection, title=title)

our_collection = Collection()

class PickyUserException(Exception):
    pass

class Film:
    @staticmethod
    def _presentable_details(c):
        return (
            f"{c['Title']} ({c['Year']}) - {c['imdbRating']}/10" + "\n"
            f"Directed by {c['Director']}" + "\n" +
            f"Written by {c['Writer']}" + "\n" +
            f"{c['Plot']}"
        )

    @staticmethod
    def _iterate(cursor):
        # Try to go through peaking at cursor and let the user pick one
        # We don't iterate through so that, if the user doesn't select anything,
        # we can offer a final pick without repeating the query.
        max_attempts = 200
        for attempt in range(max_attempts):
            try:
                c = cursor[attempt]
            except IndexError as e:
                # We've reached the end of our results
                break
            print(f"{attempt+1} {Film._presentable_details(c)}")

            user_said = input("Is it this one? [y/N]")
            if user_said in ['y', 'Y', 'yes', 'Yes']:
                return c

        # Now allow the user to pick one of the movies we've displayed
        user_said = input(f"Is it any of these? Type a number 1-{attempt} ")
        if user_said in [str(p) for p in range(1, attempt)]:
            return cursor[int(user_said)-1]

        # Exhausted options from db
        user_said = input("Look for it on omdb? [Y/n]")
        if user_said in ['y', 'Y', 'yes', 'Yes']:
            logger.info(f"Didn't find {title} ({year}) in our collection. Requesting from omdb")
            # TODO request
            pass
        else:
            raise PickyUserException("Couldn't find movie after user interrogation")

    def _assign_attributes(self, c):
        self.title = c['Title']
        self.year = c['Year']
        self.director = c['Director']
        self.writer = c['Writer']
        self.actors = c['Actors']
        self.plot = c['Plot']
        self.imdb_rating = c['imdbRating']

    def __init__(self, title, year):
        # Search our collection first
        cursor = our_collection.get(title=title, year=year)

        try:
            first_film = cursor[0]
        except IndexError as e:
            # No matching film found in our collection
            logger.info(f"Didn't find {title} ({year}) in our collection. Requesting from omdb")
            # TODO request

        try:
            next_film = cursor[1]
            logger.info("Found multiple movies. Which one?")
            chosen = Film._iterate(cursor)
            self._assign_attributes(chosen)
        except IndexError as e:
            logger.debug("We only found 1 movie. Everything is fine")
            self._assign_attributes(cursor[0])
        except PickyUserException as e:
            logger.error(f"Failed to initialise movie: {e}")
            raise e

    def __str__(self):
        return f"{self.title} ({self.year})"
