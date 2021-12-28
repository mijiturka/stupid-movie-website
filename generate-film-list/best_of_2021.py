import json
from pathlib import Path

import generate

all = json.loads(Path('./list.json').read_text())['films']
seen_in_2021 = Path('./seen-in-2021.md').read_text().splitlines()

positions = generate.random_order(seen_in_2021)

generate.pages_of_lists(
    seen_in_2021,
    positions,
    template_file='template_new_year.html',
    films_per_page=100
)
