from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_login import LoginManager


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'success'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/films'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
