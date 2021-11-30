import jinja2
import json
from pathlib import Path
import random

def template():
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
    return env.get_template('films.html')

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

# Get info on all films
all_films = json.loads(Path('./list.json').read_text())['films']

# Generate a page with the full list of films
html = template().render(films=all_films.items())
write(html, 'films.html')

# Generate a page with 20 randomly selected films
all_films_tuples = list(all_films.items())
html = template().render(films=random.choices(all_films_tuples, k=20))
write(html, 'films-1-20.html')
