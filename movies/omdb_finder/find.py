import client

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find a movie on OMDB')

    endpoint = parser.add_mutually_exclusive_group(required=True)
    endpoint.add_argument('--search', type=str, help='find all movies that match a search term')
    endpoint.add_argument('--info', type=str, help='get info about a single movie based on its imdb id')

    args = parser.parse_args()

    if args.search:
        print(client.search(args.search).json())

    if args.info:
        print(client.movie_info(args.info).json())
