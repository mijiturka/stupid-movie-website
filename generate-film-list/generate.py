import jinja2
import json
from pathlib import Path
import random

def template():
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
    return env.get_template('template_films.html')

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

# Get info on all films
all_films = json.loads(Path('./list.json').read_text())['films']

# Generate a page with the full list of films
html = template().render(films=all_films.items())
write(html, 'films.html')

# Generate pages with 20 randomly selected films on each
file_name_prefix = "films"
all_titles_list = list(all_films.keys())
selection_positions = list(range(len(all_titles_list)))
random.shuffle(selection_positions)

films_on_page = []
num_films_on_page = 0
page_number = 1
for position in selection_positions:
    film = all_titles_list[position]
    fulltext_title = all_films.pop(film)
    films_on_page.append((film, fulltext_title))
    num_films_on_page += 1

    if num_films_on_page == 20:
        # Generate page

        # Workaround for the fact that I can't get Jinja to recognise None
        html = ''
        if page_number == 1:
            html = template().render(
                films=films_on_page,
                next_page=f'{file_name_prefix}-{page_number+1}.html'
            )
        else:
            html = template().render(
                films=films_on_page,
                prev_page=f'{file_name_prefix}-{page_number-1}.html',
                next_page=f'{file_name_prefix}-{page_number+1}.html'
            )
        write(html, f'{file_name_prefix}-{page_number}.html')
        # Move to next page
        page_number += 1
        # Start it fresh
        num_films_on_page = 0
        films_on_page = []

# Generate the last page
html = template().render(films=films_on_page)
write(html, f'{file_name_prefix}-{page_number}.html')
