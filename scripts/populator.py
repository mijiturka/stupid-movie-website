from generate_film_list.film_utilities import all_titles
from movie_data.omdb_finder import client as omdb

if __name__ == '__main__':

    for title in all_titles(data_file_path='generate_film_list/list.json'):
        print(title)

        choice = input('[f]ind, [S]kip?\n')

        if choice == '':
            print('Skipping')
        else:
            print('Searching:')
            response = omdb.search(title)
            print(response.json())
