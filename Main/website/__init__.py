from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
from flask_login import LoginManager
import google.generativeai as genai

DB_NAME = "database.db"

db = SQLAlchemy()  # Initialize db *outside* create_app()
login_manager = LoginManager() #Initialize login_manager outside create_app()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "JJkhfdsahioiksf"

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"


    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    


    create_database(app)
    return app

    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database Created!")



