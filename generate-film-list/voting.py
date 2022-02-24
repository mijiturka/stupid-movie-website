import argparse
import json
import logging
from pathlib import Path

import generate

logger = logging.getLogger(__name__)

# A page to vote on

def generate_voting_page(movies_file, template_file):
    movies = list(json.loads(Path(movies_file).read_text())['films'].keys())

    positions = generate.random_order(movies)

    logger.debug(f'Movies are {movies}',
                f'Positions are {positions}'
    )

    generate.pages_of_lists(
        movies,
        positions,
        template_file,
        films_per_page=100,
        generated_file_name_prefix='vote'
    )

# A page to display results after voting

def clean_up(title):
    if title.startswith('film-'):
        return title.split('film-')[1]

def from_result(result):
    ordered = list(result.items())
    ordered.sort(key=lambda x: x[1], reverse=True)

    films = [clean_up(title) for (title, rating) in ordered]
    positions = list(range(len(films)))

    return films, positions

def generate_results_page(result):
    films, positions = from_result(result)

    generate.pages_of_lists(
        films,
        positions,
        template_file='template_films_with_scores.html',
        films_per_page=100,
        generated_file_name_prefix='voting-results',
        with_scores=True
    )

# Combined charts generation

if __name__ == '__main__':
    logging.basicConfig(format='%(name)s.%(funcName)s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Generate pages for vote-sorted movies')
    parser.add_argument(
        '--vote',
        help='Generate a page of movies with voting buttons',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--results',
        help='Generate a page of movies based on voting results, sorted by result from best to worst. \
        Expects to get the results in the form the voting page spits out',
    )
    args = parser.parse_args()

    if not args.vote and not args.results:
        parser.error('No action to be taken')
    if args.vote:
        generate_voting_page('./list.json', 'template_vote_new_year.html')
    if args.results:
        generate_results_page(json.loads(args.results))
