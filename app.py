from flask import Flask, request, redirect, render_template, jsonify
import json
# import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

with open('users.json') as u:
    dataUsers = json.load(u)

with open('movies.json') as f:
    data = json.load(f)


@app.route('/login', methods=['POST'])  
def login():
    username = request.form['username']
    password = request.form['password']
    
    for user in dataUsers['users']:
        if user['username'] == username and user['password'] == password:
          return redirect('/home')
        else:
            return redirect('/home_guest')

    if username in dataUsers and dataUsers[username] == password:
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

    return data

@app.route('/movies')
def getMovies():
    return jsonify({"Peliculas": data, "mensaje": "Lista de peliculas"})

@app.route('/movies/<string:movie_title>')
def getMovie(movie_title):
    PeliBuscada = [peli for peli in data if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):  
        return jsonify({"Pelicula": PeliBuscada[0]})
        
    return jsonify({'Mensaje': "Pelicula no encontrada"})

@app.route('/movie/add_movie', methods=['POST'])
def addMovie():
    if request.method == 'POST':
        new_movie = {
            "title": request.form['title'],
            "director": request.form['director'],
            "release_year": request.form['release_year'],
            "rating": request.form['rating']
        }

        data.append(new_movie)
        
        return jsonify({"message": "Pelicula agregada correctamente", "Movies": data})

    return render_template('add_movie.html')

@app.route('/movies/<string:movie_title>', methods=['PUT'])
def editMovie(movie_title):
    PeliBuscada = [peli for peli in data if peli['title'] == movie_title]
    
    if(len(PeliBuscada) > 0):
        PeliBuscada[0]['title'] = request.json['title']
        PeliBuscada[0]['director'] = request.json['director']
        PeliBuscada[0]['release_year'] = request.json['release_year']
        PeliBuscada[0]['rating'] = request.json['rating']
        
        return jsonify({"message": "Pelicula actualizada", "Pelicula": PeliBuscada[0]})
    return jsonify({"message": "Pelicula no encontrada"})

@app.route('/movies/<string:movie_title>', methods = ['DELETE'])
def deleteMovie(movie_title):
    PeliBuscada = [peli for peli in data if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):
        data.remove(PeliBuscada[0])
        return jsonify({ "message": "Pelicula eliminada correctamente", "Movies": data})
    
    return jsonify({"message": "Pelicula no encontrada"})


app.run(debug=True)

