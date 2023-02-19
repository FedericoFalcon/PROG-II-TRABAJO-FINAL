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

# Importamos los directores as dataDirectors
with open('directors.json') as d:
    dataDirectors = json.load(d)

# Importamos los generos as dataGenres
with open('genres.json') as g:
    dataGenres = json.load(g)

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

# Endpoint directores
@app.route('/directors')
def handle_click3():
    return dataDirectors

# Endpoint generos
@app.route('/genres')
def handle_click4():
    return dataGenres

# Buscar pelicula
@app.route('/search')
def searchMovie():
    movie_title = request.args.get('movie_title').lower()
    PeliBuscada = [peli for peli in data if peli['title'].lower() == movie_title]

    if (len(PeliBuscada) > 0):
        return jsonify({"Pelicula": PeliBuscada[0]})

    return jsonify({'Mensaje': "Pelicula no encontrada"})

# Agrega una peli al listado (solo usuarios registrados)
@app.route('/movies/add_movie', methods=['POST'])
def addMovie():
    if request.method == 'POST':
        new_movie = {
            "title": request.form["title"],
            "director": request.form["director"],
            "release_year": request.form["release_year"],
            "rating": request.form["rating"],
            "genre": request.form["genre"],
            "sinopsis": request.form["sinopsis"],
            "comments": request.form["comments"],
            "cast": request.form["cast"],
            "img": request.form["img"]
        }

        data.append(new_movie)
        with open("movies.json", "w") as f:
            json.dump(data, f)
        
    return jsonify({"Agregada correctamente. Movies": data})

# Borra una pelicula 
@app.route('/movies/delete_movie')
def deleteMovie():

    movie_title = request.args.get('movie_title').lower()
    PeliBuscada = [peli for peli in data if peli['title'].lower() == movie_title]
  

    if (len(PeliBuscada) > 0):
        for movie in data:
            if PeliBuscada[0]['comments'] == "":
                if movie['title'].lower() == PeliBuscada[0]['title'].lower():
                    data.remove(movie)
                    with open("movies.json", "w") as f:
                        json.dump(data, f)
                    return jsonify({"OK. Peliculas Actualizadas": data})

    return jsonify({'Mensaje': "Pelicula no encontrada o con un comentario existente."})

# Busqueda de peliculas por director
@app.route('/search_director')
def searchDirector():
    movie_director = request.args.get('movie_director').lower()
    DirectorSearch = [director for director in data if director['director'].lower() == movie_director]

    if len(DirectorSearch) > 0:
        movies = [movie for movie in data if movie['director'].lower() == movie_director.lower()]
        return jsonify({"Peliculas": movies})

    return jsonify({'Mensaje': "Director no encontrado"})

# Busqueda de peliculas por actor
@app.route('/search_cast')
def searchCast():
    movie_cast = request.args.get('movie_cast').lower()
    castSearch = [cast for cast in data if cast['cast'].lower() == movie_cast]

    if len(castSearch) > 0:
        movies = [movie for movie in data if movie['cast'].lower() == movie_cast.lower()]
        return jsonify({"Peliculas": movies})

    return jsonify({'Mensaje': "Actor no encontrado"})

# Endpoint buscar pelis con portada
@app.route('/search_img')
def searchImg():

        img_movies = [img for img in data if img['img'] != ""]
        return jsonify({"Peliculas con portada":img_movies})


# Editar pelis
@app.route('/movies/edit_movie', methods=['POST'])
def editMovie():
    if request.method == 'POST':
        movie_title = request.form['title'].lower()
        movie = next(movie for movie in data if movie['title'].lower() == movie_title)
        if movie:
                # if request.form['title'] != "":
                #     movie['title'] = request.form['title']
                if request.form['director'] != "":
                    movie['director'] = request.form['director']
                if request.form['release_year'] != "":
                    movie['release_year'] = request.form['release_year']
                if request.form['rating'] != "":
                    movie['rating'] = request.form['rating']
                if request.form['genre'] != "":
                    movie['genre'] = request.form['genre']
                if request.form['sinopsis'] != "":
                    movie['sinopsis'] = request.form['sinopsis']
                if request.form['cast'] != "":
                    movie['cast'] = request.form['cast']
                if request.form['img'] != "":
                    movie['img'] = request.form['img']

                with open("movies.json", "w") as f:
                    json.dump(data, f)
                return jsonify({"Lista actualizada" : data})

        return jsonify({'Mensaje': "No se encontró ninguna película con el titulo proporcionado"})

# Comentar pelis
@app.route('/movies/comment_movie', methods=['POST'])
def commentMovie():
    if request.method == 'POST':
        movie_title = request.form['title'].lower()
        movie = next(movie for movie in data if movie['title'].lower() == movie_title)
        if movie:
            movie['comments'] = movie['comments'] + " ** " + request.form['comments'] + " ** - "

            with open("movies.json", "w") as f:
                json.dump(data, f)
            return jsonify({"Nuevo comentario agregado" : movie})

app.run(debug=True)

