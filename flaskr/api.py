from flask_restx import Resource
from flask import request

from . import api, db

from .models import Genres, Directors

from .schemas import GenresSchema, DirectorsSchema

genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)
director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)


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
