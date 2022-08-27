import json

from flask import Flask, request, jsonify
#from utils import search_title, search_by_years, search_movie_rating
from utils import *

app = Flask(__name__)

@app.get('/movie/<title>/')
def movie_search(title):
    movie = search_title(title)
    return movie

@app.get('/movie/<year_1>/to/<year_2>/')
def movie_search_by_years(year_1, year_2):
    movie = search_by_years(year_1, year_2)
    return movie

@app.get('/movie/rating/<rating>/')
def search_movie_by_rating(rating):
    movie = search_movie_rating(rating)
    return movie

@app.get('/movie/genre/<genre>/')
def search_movie_by_genre(genre):
    movie = search_genre(genre)
    return movie

if __name__ == "__main__":
    app.run(port=5000)
