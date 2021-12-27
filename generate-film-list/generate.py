import jinja2
import json
from pathlib import Path
import random

def template(file_name):
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
    return env.get_template(file_name)

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

def film_pages():
    # Get info on all films
    all_films = json.loads(Path('./list.json').read_text())['films']

    # Generate a page with the full list of films
    html = template('template_films.html').render(films=all_films.items())
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
                html = template('template_films.html').render(
                    films=films_on_page,
                    next_page=f'{file_name_prefix}-{page_number+1}.html'
                )
            else:
                html = template('template_films.html').render(
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
    html = template('template_films.html').render(films=films_on_page)
    write(html, f'{file_name_prefix}-{page_number}.html')

def single_film_page(film):
    film_title = json.loads(Path('./list.json').read_text())['films'][film]
    review = json.loads(Path(f'../reviews-json/{film}.json').read_text())
    html = template('template_single_film.html').render(
        film = film,
        film_title = film_title,
        film_grade = review['grade'],
        review_both_start = review.get('review_both_start', None),
        review_shmentina = review['shmentina'],
        review_capellyana = review['capellyana'],
        dumbometers = review.get('dumbometers', None),
        review_both_end = review.get('review_both_end', None),
        timestamp = review['timestamp']
    )
    write(html, f'{film}.html')
