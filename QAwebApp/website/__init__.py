from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Initiate Database
db = SQLAlchemy()
DB_NAME = "database.db"

#Create app function
def create_app():
    from .models import User, Case, Note
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///QAappDB'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#Create database function
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')