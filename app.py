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

    return movies


@app.route('/movies',  methods=['GET'])
def nada():
    print(request.form)
    return "ok"




@app.route('/movies')
def getMovies():
    return jsonify({"Peliculas": movies, "mensaje": "Lista de peliculas"})

@app.route('/movies/<string:movie_title>')
def getMovie(movie_title):
    PeliBuscada = [peli for peli in movies if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):  
        return jsonify({"Pelicula": PeliBuscada[0]})
        
    return jsonify({'Mensaje': "Pelicula no encontrada"})

@app.route('/movies', methods=['POST'])
def addMovie():
    new_movie = {
        "title": request.json['title'],
        "director": request.json['director'],
        "release_year": request.json['release_year'],
        "rating": request.json['rating']
    }

    movies.append(new_movie)

    return jsonify({"message": "Pelicula agregada correctamente", "Movies": movies})

@app.route('/movies/<string:movie_title>', methods=['PUT'])
def editMovie(movie_title):
    PeliBuscada = [peli for peli in movies if peli['title'] == movie_title]
    
    if(len(PeliBuscada) > 0):
        PeliBuscada[0]['title'] = request.json['title']
        PeliBuscada[0]['director'] = request.json['director']
        PeliBuscada[0]['release_year'] = request.json['release_year']
        PeliBuscada[0]['rating'] = request.json['rating']
        
        return jsonify({"message": "Pelicula actualizada", "Pelicula": PeliBuscada[0]})
    return jsonify({"message": "Pelicula no encontrada"})

@app.route('/movies/<string:movie_title>', methods = ['DELETE'])
def deleteMovie(movie_title):
    PeliBuscada = [peli for peli in movies if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):
        movies.remove(PeliBuscada[0])
        return jsonify({ "message": "Pelicula eliminada correctamente", "Movies": movies})
    
    return jsonify({"message": "Pelicula no encontrada"})


app.run(debug=True)

