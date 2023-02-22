from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db=SQLAlchemy()

DB_NAME='books_db.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='ni ni ni'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    
    from .models import Book

    create_database(app)

    return app

def create_database(app):
    if not path.exists('Website/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print('database created')

