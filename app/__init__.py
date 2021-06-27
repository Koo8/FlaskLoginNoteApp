from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '22cdgoeiuyt44teagn8'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_Name
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    # create database
    from .models import User, Note
    if not path.exists('app/'+DB_Name):
        db.create_all(app = app)

    # login
    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
