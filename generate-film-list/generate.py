import jinja2
import json
from pathlib import Path
import random

import film_utilities

def template(file_name):
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
    return env.get_template(file_name)

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

def random_order(titles_list):
    selection_positions = list(range(len(titles_list)))
    random.shuffle(selection_positions)

    return selection_positions

def pages_of_lists(films, positions, template_file='template_films.html', films_per_page=20):
    file_name_prefix = "films"

    films_on_page = []
    num_films_on_page = 0
    page_number = 1
    for position in positions:
        film = films[position]
        films_on_page.append((film, film_utilities.fulltext_title(film)))
        num_films_on_page += 1

        if num_films_on_page == films_per_page:
            # Generate page

            # Workaround for the fact that I can't get Jinja to recognise None
            html = ''
            if page_number == 1:
                html = template(template_file).render(
                    films=films_on_page,
                    next_page=f'{file_name_prefix}-{page_number+1}.html'
                )
            else:
                html = template(template_file).render(
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
    html = template(template_file).render(films=films_on_page)
    write(html, f'{file_name_prefix}-{page_number}.html')

def all_film_pages():
    # Generate pages with 20 randomly arranged films on each

    all_films = json.loads(Path('./list.json').read_text())['films']
    titles_list = list(all_films.keys())
    selection_positions = random_order(titles_list)

    pages_of_lists(titles_list, selection_positions)

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
