from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .models import Genres, Directors


class GenresSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genres


class DirectorsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Directors


