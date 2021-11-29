from flaskr import db

from werkzeug.security import generate_password_hash


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    films = db.relationship('Films', backref='users', lazy=True)

    def __repr__(self):
        return f'User: {self.user_id}, name: {self.name}, is_admin: {self.is_admin}'

    def set_password(self, password):
        self.password = generate_password_hash(password)


films_genres = db.Table('films_genres',
                        db.Column('film_id', db.Integer, db.ForeignKey('films.film_id'),
                                  primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id'),
                                  primary_key=True)
                        )


films_directors = db.Table('films_directors',
                           db.Column('film_id', db.Integer, db.ForeignKey('films.film_id'),
                                     primary_key=True),
                           db.Column('director_id', db.Integer,
                                     db.ForeignKey('directors.director_id',
                                                   ondelete="SET DEFAULT"), default='unknown',
                                     primary_key=True))


class Films(db.Model):
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Numeric, nullable=True)
    poster = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    directors = db.relationship('Directors', secondary=films_directors,
                                backref=db.backref('films', lazy='dynamic'))
    genres = db.relationship('Genres', secondary=films_genres,
                             backref=db.backref('films', lazy='dynamic'))

    def __repr__(self):
        return f'Film: {self.film_id}, title: {self.title}, date: {self.release_date}'


class Directors(db.Model):
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'Director: id: {self.director_id}, name:{self.name}'


class Genres(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'Genre: id: {self.genre_id}, name:{self.name}'


db.create_all()
