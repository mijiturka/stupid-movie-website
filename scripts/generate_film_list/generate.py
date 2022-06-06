import jinja2
import json
import logging
from pathlib import Path
import random

import film_utilities

logger = logging.getLogger(__name__)

def template(file_path):
    env = jinja2.Environment(loader = jinja2.FileSystemLoader(Path(file_path).parent))
    return env.get_template(Path(file_path).name)

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

def random_order(titles_list):
    selection_positions = list(range(len(titles_list)))
    random.shuffle(selection_positions)

    return selection_positions

def pages_of_lists(films, positions,
    template_path='templates/template_films.html', films_per_page=20,
    generated_file_name_prefix = "films",
    with_scores=False):

    logger.info(f'Generating pages of {films_per_page} films per page '
                f'using template {template_path}. '
                f'Files will be written as {generated_file_name_prefix}-*.html'
    )

    films_on_page = []
    num_films_on_page = 0
    page_number = 1
    for position in positions:
        film = films[position]
        logger.debug(f'Adding {film} to page {page_number}')

        parameters_for_template = (film, film_utilities.fulltext_title(film))
        if with_scores:
            parameters_for_template.append(position+1)
        films_on_page.append(parameters_for_template)

        num_films_on_page += 1

        if num_films_on_page == films_per_page:
            # Generate page

            # Workaround for the fact that I can't get Jinja to recognise None
            html = ''
            if page_number == 1:
                html = template(template_path).render(
                    films=films_on_page,
                    next_page=f'{generated_file_name_prefix}-{page_number+1}.html'
                )
            else:
                html = template(template_path).render(
                    films=films_on_page,
                    prev_page=f'{generated_file_name_prefix}-{page_number-1}.html',
                    next_page=f'{generated_file_name_prefix}-{page_number+1}.html'
                )
            logger.debug(f'Writing page {page_number} to {generated_file_name_prefix}-{page_number}.html')
            write(html, f'{generated_file_name_prefix}-{page_number}.html')
            # Move to next page
            page_number += 1
            # Start it fresh
            num_films_on_page = 0
            films_on_page = []

    # Generate the last page
    html = template(template_path).render(films=films_on_page)
    logger.debug(f'Writing page {page_number} to {generated_file_name_prefix}-{page_number}.html')
    write(html, f'{generated_file_name_prefix}-{page_number}.html')

def all_film_pages():
    # Generate pages with 20 randomly arranged films on each

    all_films = json.loads(Path('./list.json').read_text())['films']
    titles_list = list(all_films.keys())
    selection_positions = random_order(titles_list)

    pages_of_lists(titles_list, selection_positions)

def single_film_page(film):
    film_title = json.loads(Path('./list.json').read_text())['films'][film]
    review = json.loads(Path(f'../../reviews-json/{film}.json').read_text())
    html = template('templates/template_single_film.html').render(
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

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
