import requests
from pathlib import Path

def base_url():
    return 'http://www.omdbapi.com'

def auth_key():
    return Path('my.key').read_text().strip()

def search(term):
    def endpoint(api_key, search_term):
        return f'/?apikey={api_key}&s={search_term}'

    url = base_url() + endpoint(auth_key(), term)

    return requests.get(url)

def movie_info(imdb_id):
    def endpoint(api_key, imdb_id):
        return f'/?apikey={api_key}&i={imdb_id}'

    url = base_url() + endpoint(auth_key(), imdb_id)

    return requests.get(url)

if __name__ == '__main__':
    response = search('carnosaur')
    print(response)
