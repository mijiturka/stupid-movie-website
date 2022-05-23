from flask import Flask, abort, render_template, request
import json
from pathlib import Path

import client

app = Flask(__name__)

def dummy_response():
    return json.loads(Path('testdata/search_response2.json').read_text())

def actual_search(term):
    return client.search(term).json()

def clean(input):
    allowed_symbols = [' ', '-']
    return ''.join([c for c in input if c.isalpha() or c in allowed_symbols])

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method != 'POST':
        main()

    cleaned = clean(request.form.get('search'))

    # return render_template('results.html', movies=dummy_response()['Search'])
    return render_template('results.html', movies=actual_search(cleaned)['Search'])
