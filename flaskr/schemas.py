from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from .models import Genres, Directors, Films, Users


class GenresSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres


class DirectorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Directors


class FilmsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Films

    genres = Nested(GenresSchema, many=True)
    directors = Nested(DirectorsSchema, many=True)


class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_only = "password"
