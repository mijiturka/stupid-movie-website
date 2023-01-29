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

class Film:
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
            # TODO iterate and let user choose
        except IndexError as e:
            logger.debug("We only found 1 movie. Everything is fine")
            pass
