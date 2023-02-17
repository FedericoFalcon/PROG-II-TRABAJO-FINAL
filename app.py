from flask import Flask, request, redirect, render_template, jsonify
import json
# import urllib.request

app = Flask(__name__)

# Render Login
@app.route('/')
def index():
    return render_template('login.html')

# Importamos los usuarios as dataUsers
with open('users.json') as u:
    dataUsers = json.load(u)

# Importamos las peliculas as data
with open('movies.json') as f:
    data = json.load(f)

# Login 
@app.route('/login', methods=['POST'])  
def login():
    username = request.form['username']
    password = request.form['password']
    
    for user in dataUsers['users']:
        if user['username'] == username and user['password'] == password:
          return redirect('/home')
        
    return redirect('/home_guest')

# Render home registrado
@app.route('/home')
def home():
    return render_template('home.html')

# Render home invitado
@app.route('/home_guest')
def home_guest():
    return render_template('home_guest.html')

# Endpoint pelis invitado
@app.route('/home_guest', methods=['POST'])
def handle_click():
    return data

# Endpoint pelis registrados
@app.route('/home', methods=['POST'])
def handle_click2():
    return data

# Endpoint pelicula buscada
@app.route('/movies/<string:movie_title>')
def getMovie(movie_title):
    PeliBuscada = [peli for peli in data if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):  
        return jsonify({"Pelicula": PeliBuscada[0]})
        
    return jsonify({'Mensaje': "Pelicula no encontrada"})

@app.route('/search')
def searchMovie():
    movie_title = request.args.get('movie_title')
    PeliBuscada = [peli for peli in data if peli['title'] == movie_title]

    if (len(PeliBuscada) > 0):
        return jsonify({"Pelicula": PeliBuscada[0]})

    return jsonify({'Mensaje': "Pelicula no encontrada"})

@app.route('/movies/add_movie', methods=['POST'])
def addMovie():
    if request.method == 'POST':
        new_movie = {
            "title": request.form["title"],
            "director": request.form["director"],
            "release_year": request.form["release_year"],
            "rating": request.form["rating"]
        }

        data.append(new_movie)
        with open("movies.json", "w") as f:
            json.dump(data, f)
        
        return jsonify({"Movies": data})


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

