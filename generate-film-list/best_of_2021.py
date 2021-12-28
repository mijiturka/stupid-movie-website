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
        template_file='template_new_year.html',
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

def generate_results_page():
    result = {"film-looking-glass":-1,"film-house":2,"film-chopping-mall":0,"film-pig":3,"film-zombie-apocalypse":2,"film-dont-open-till-christmas":1,"film-the-bet":1,"film-never-too-young-to-die":1,"film-the-bat-people":1,"film-big-bad-wolf":1,"film-31":-1,"film-enter-the-ninja":-1,"film-sharktopus-vs-pteracuda":-1,"film-just-imagine":-1,"film-hellraiser-3-hell-on-earth":1,"film-dead-dont-die-in-dallas":1,"film-empire-of-the-ants":1,"film-samurai-cop":-1,"film-monster-dog":2,"film-flash-gordon":2,"film-they-live":1,"film-the-castle-of-fu-manchu":1,"film-the-pumaman":1,"film-dismal":0,"film-holes":-1,"film-santa-with-muscles":0,"film-exorcist-2-the-heretic":0,"film-street-trash":0,"film-secret-agent-club":0,"film-hard-ticket-to-hawaii":0,"film-teenage-caveman":0,"film-jeepers-creepers-2":0,"film-manos-the-hands-of-fate":0,"film-vampires-kiss-second-viewing":0,"film-prey-for-death":0,"film-high-spirits":0,"film-the-sorcerers-apprentice":0,"film-absurd":0,"film-atm":0,"film-the-spell":0,"film-rotor":0,"film-my-ghost-dog-my-magic-dog":0,"film-sweet-taste-of-souls":0,"film-hellraiser-4-bloodline":0,"film-ben-banks-beauty-and-the-least-the-misadventures-of-ben-banks":0,"film-the-apple-second-viewing":0,"film-night-of-the-comet":0,"film-elves":0,"film-time-changer":0,"film-the-jesus-rolls":0,"film-hellraiser":0,"film-frogs":0,"film-new-world-order-the-end-has-come":0,"film-rubber":0,"film-bigfoot-country":0,"film-the-vengeance-of-fu-manchu":0,"film-the-horror-show-house-3":0,"film-the-blood-of-fu-manchu":0,"film-the-lawnmower-man":0,"film-turbulence":0,"film-dead-silence":0,"film-the-bone-garden":0,"film-troll-3-the-quest-for-the-mighty-sword-hobgoblin-ator-4":0,"film-attack-of-the-giant-leeches":0,"film-hellraiser-5-inferno":0,"film-cabal":0,"film-hellraiser-2-hellbound":0,"film-hellraiser-6-hellseeker":0,"film-best-worst-movie":0,"film-jingle-all-the-way":0,"film-boza":0,"film-the-brides-of-fu-manchu":0,"film-starship-troopers":0,"film-plan-9-from-outer-space":0,"film-the-drone":0,"film-primal":0,"film-plymouth":0,"film-the-sand":0,"film-house-2-the-second-story":0,"film-blood-diner":0,"film-mrs-claus":0,"film-birdemic-shock-and-terror":0,"film-blood-beach":0,"film-almost-an-angel":0,"film-pass-thru":0,"film-microwave-massacre":0,"film-black-roses":0,"film-terrorvision":0,"film-suburban-commando":0,"film-lawnmower-man-2-beyond-cyberspace":0,"film-wrong-target":0,"film-turbulence-3-heavy-metal":0,"film-midnight-chronicles":0,"film-night-of-the-creeps":0,"film-singularity-principle":0}

    films, positions = from_result(result)

    generate.pages_of_lists(
        films,
        positions,
        template_file='template_films.html',
        films_per_page=100,
        generated_file_name_prefix='voting-results'
    )

if __name__ == '__main__':
    generate_voting_page()
    generate_results_page()
