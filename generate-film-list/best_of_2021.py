import argparse
import json
from pathlib import Path

import generate

# A page to vote on

def generate_voting_page():
    all = json.loads(Path('./list.json').read_text())['films']
    seen_in_2021 = Path('./seen-in-2021.md').read_text().splitlines()

    positions = generate.random_order(seen_in_2021)

    generate.pages_of_lists(
        seen_in_2021,
        positions,
        template_file='template_vote.html',
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
        generated_file_name_prefix='voting-results'
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate pages for vote-sorted movies')
    parser.add_argument(
        '--vote',
        help='Generate a page of the movies seen in 2021, with voting buttons',
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
        generate_voting_page()
    if args.results:
        generate_results_page(json.loads(args.results))
