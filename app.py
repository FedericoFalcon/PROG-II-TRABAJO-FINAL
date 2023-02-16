from flask import Flask, request, redirect, render_template, jsonify
import json
import urllib.request
from movies import movies

app = Flask(__name__)

# FLASK_APP = "nombre que queramos"

# @app.route("/")
# def home():
#     return "Hello, Flask! <br> Lalala"

@app.route('/')
def index():
    return render_template('login.html')


users = {
    'elmago24': 'elmago22',
    'bokitabebianchi': 'la12',
    'marcelocarp': 'gallardoteamo'
}

movies = [
    {
        "title": "The Matrix",
        "director": "The Wachowskis",
        "release_year": 1999,
        "rating": 8.7
    },
    {
        "title": "Inception",
        "director": "Christopher Nolan",
        "release_year": 2010,
        "rating": 8.8
    },
    {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "release_year": 1994,
        "rating": 9.3
    }
]

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return redirect('/home')
    else:
        return redirect('/home_guest')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home_guest')
def home_guest():
    return render_template('home_guest.html')


@app.route('/home_guest', methods=['POST'])
def handle_click():

    pelis = ""

    for i in movies:
       pelis = pelis + "<br>" + (i["title"])

    return pelis

@app.route('/movies')
def getMovies():
    return jsonify({"Peliculas": movies, "mensaje": "Lista de peliculas"})

@app.route('/movies/<string:movie_title>')
def getMovie(movie_title):
    PeliBuscada = [peli for peli in movies if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):  
        return jsonify({"Pelicula": PeliBuscada[0]})
        
    return jsonify({'Mensaje': "Pelicula no encontrada"})
    


app.run(debug=True)

