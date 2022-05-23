import json
from pathlib import Path
import pymongo

def database():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client['movies']

def add(collection, movie_info_json):
    collection.insert_many(movie_info_json)

def get_all(collection):
    for movie in collection.find():
        print(f"""
            {movie['Title']} -
            {movie['imdbRating']}
        """)

def read_from_file():
    return json.loads(Path('testdata/movies.json').read_text())

if __name__ == "__main__":
    db = database()

    collection = db['info']

    add(collection, read_from_file())

    get_all(collection)
