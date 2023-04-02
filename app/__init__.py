from flask import Flask, render_template
import urllib.request, json
from random import choice as randChoice
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/sass', 'static/css', '/static/css')
})


@app.route("/synonym/<word>")
def home(word=None):
    return render_template('home.html', word=getSynonyms(word))

def callMWapi(word):
    with open("./secrets/APIKeys.json") as f:
        APIKeys = json.loads(f.read())
        
    url = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={APIKeys['MWThesaurus']}"
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)


def getSynonyms(word):
    synonyms = callMWapi(word)
    # Ensures that the word tried to find synonyms for is in the MW database. 
    # Their API returns a list of words, in their database, that closely resembles the word of the attempted request.
    # The API is then called again with a random choice fra that list of words.
    while(type(synonyms)==type(list[str])):
        synonyms = callMWapi(randChoice(synonyms))
    # Unpacking the JSON
    synonyms = [i for meaning in synonyms for ii in meaning["meta"]["syns"] for i in ii]
    return synonyms