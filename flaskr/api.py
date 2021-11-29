from flask_restx import Resource
from flask import request

from . import api, db

from .models import Genres, Directors, Films, Users

from .schemas import GenresSchema, DirectorsSchema, FilmsSchema, UsersSchema

from .parsing import films_parsing

genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)
director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)
film_schema = FilmsSchema()
films_schema = FilmsSchema(many=True)
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


@api.route('/genres')
class GenreListApi(Resource):
    def get(self):
        genres = Genres.query.order_by(Genres.name).all()
        return genres_schema.dump(genres).data

    def post(self):
        genre = genre_schema.load(request.json, session=db.session).data
        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre).data, 201


@api.route('/genres/{genre_id}')
class GenreApi(Resource):
    def get(self, genre_id):
        genre = Genres.query.filter(Genres.genre_id == genre_id).one_or_none()
        if genre is not None:
            return genre_schema.dump(genre).data
        else:
            return {'message': "Genre not found"}, 404

    def put(self, genre_id):
        genre = Genres.query.filter(Genres.genre_id == genre_id).one_or_none()
        if genre is not None:
            genre = genre_schema.load(request.json, instance=genre, session=db.session).data
            db.session.add(genre)
            db.session.commit()
            return genres_schema.dump(genre).data, 201
        else:
            return {'message': "Genre not found"}, 404

    def delete(self, genre_id):
        genre = Genres.query.filter(Genres.genre_id == genre_id).one_or_none()
        if genre is not None:
            db.session.delete(genre)
            db.session.commit()
            return {}, 204
        else:
            return {'message': "Genre not found"}, 404


@api.route('/directors')
class DirectorListApi(Resource):
    def get(self):
        directors = Directors.query.order_by(Directors.name).all()
        return directors_schema.dump(directors).data

    def post(self):
        director = director_schema.load(request.json, session=db.session).data
        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director).data, 201


@api.route('/directors/{director_id}')
class DirectorApi(Resource):
    def get(self, director_id):
        director = Directors.query.filter(Directors.director_id == director_id).one_or_none()
        if director is not None:
            return directors_schema.dump(director).data
        else:
            return {'message': "Genre not found"}, 404

    def put(self, director_id):
        director = Directors.query.filter(Directors.director_id == director_id).one_or_none()
        if director is not None:
            director = director_schema.load(request.json, instance=director, session=db.session).data
            db.session.add(director)
            db.session.commit()
            return directors_schema.dump(director).data, 201
        else:
            return {'message': "Director not found"}, 404

    def delete(self, director_id):
        director = Directors.query.filter(Directors.director_id == director_id).one_or_none()
        if director is not None:
            db.session.delete(director)
            db.session.commit()
            return {}, 204
        else:
            return {'message': "Director not found"}, 404


@api.route('/films')
class FilmListApi(Resource):
    def get(self):
        films = Films.query.order_by(Films.title).all()
        return films_schema.dump(films).data

    def post(self):
        user_input = films_parsing(request.json)
        film = film_schema.load(user_input, session=db.session, transient=True).data
        directors = Directors.query.filter(Directors.director_id == request.json.get('directors')).one_or_none()
        genres = Genres.query.filter(Genres.genre_id == request.json.get('genres')).one_or_none()
        film.directors = directors
        film.genres = genres
        db.session.add(film)
        db.session.commit()
        return film_schema.dump(film).data, 201


@api.route('/films/{film_id}')
class FilmApi(Resource):
    def get(self, film_id):
        film = Films.query.filter(Films.film_id == film_id).one_or_none()
        if film is not None:
            return films_schema.dump(film).data
        else:
            return {'message': "Film not found"}, 404

    def put(self, film_id):
        film = Films.query.filter(Films.film_id == film_id).one_or_none()
        if film is not None:
            user_input = films_parsing(request.json)
            film = film_schema.load(user_input, instance=film, session=db.session).data
            directors = Directors.query.filter(Directors.director_id == request.json.get('directors')).one_or_none()
            genres = Genres.query.filter(Genres.genre_id == request.json.get('genres')).one_or_none()
            film.directors = directors
            film.genres = genres
            db.session.add(film)
            db.session.commit()
            return film_schema.dump(film).data, 201
        else:
            return {'message': "Film not found"}, 404

    def delete(self, film_id):
        film = Films.query.filter(Films.film_id == film_id).one_or_none()
        if film is not None:
            db.session.delete(film)
            db.session.commit()
            return {}, 204
        else:
            return {'message': "Film not found"}, 404


@api.route('/registration')
class UsersApi(Resource):
    def get(self):
        users = Users.query.all()
        return users_schema.dump(users).data

    def post(self):
        user = Users.query.filter(Users.login == request.json.get("login")).one_or_none()
        if user:
            return {"message": f"User with login: {request.json.get('login')} exists!"}
        else:
            user = user_schema.load(request.json, session=db.session)
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user).data, 201

    def put(self):
        user = Users.query.filter(Users.login == request.json.get("login")).one_or_none()
        if user:
            user = user_schema.load(request.json, instance=user, session=db.session)
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user).data, 201
        else:
            return {"message": f"User with login: {request.json.get('login')} not found"}, 404

    def delete(self):
        user = Users.query.filter(Users.login == request.json.get("login")).one_or_none()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        else:
            return {"message": f"User with login: {request.json.get('login')} not found"}, 404
