import json
from pathlib import Path
import pymongo

def database():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client['movies']

def add(collection, movie_info_json):
    collection.insert_many(movie_info_json)

def read_from_file():
    return json.loads(Path('testdata/movies.json').read_text())

def bulk_add(collection):
    add(collection, read_from_file())

def get_by_title(collection, title):
    return collection.find(
        {'Title': title}
    )

def get_by_title_and_year(collection, title, year):
    return collection.find(
        {
        'Title': title,
        'Year': year
        }
    )

def get_by_imdb_id(collection, id):
    return collection.find_one(
        {'imdbID': id}
    )

def get_all(collection):
    return collection.find()

def print_all(collection):
    for movie in collection.find():
        print(f"{movie['Title']} - {movie['imdbRating']}")

if __name__ == "__main__":
    db = database()
    collection = db['info']

    get_all(collection)
