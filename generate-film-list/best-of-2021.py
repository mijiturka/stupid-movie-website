import json
from pathlib import Path

import generate

all = json.loads(Path('./list.json').read_text())['films']
seen_in_2021 = Path('./seen-in-2021.md').read_text().splitlines()

films = {film: title for (film, title) in all.items() if film in seen_in_2021}

generate.pages_of_lists(films, template_file='template_new_year.html', films_per_page=100)
