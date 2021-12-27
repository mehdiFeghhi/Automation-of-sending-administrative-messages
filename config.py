import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS()
db = SQLAlchemy()

jwt = JWTManager()


def create_app():
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    file_path = os.path.abspath(os.getcwd()) + "/sample.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    return app
