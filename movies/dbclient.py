import json
from pathlib import Path
import pymongo

def database():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client['movies']

def read_from_file():
    return json.loads(Path('testdata/movies.json').read_text())

def add(collection):
    collection.insert_many(read_from_file())

def get_all(collection):
    for movie in collection.find():
        print(f"""
            {movie['Title']} -
            {movie['imdbRating']}
        """)


if __name__ == "__main__":
    db = database()    

    collection = db['info']

    # add(collection)

    get_all(collection)
