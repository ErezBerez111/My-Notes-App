from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
import os
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()

def create_app():
    port = os.getenv('PORT', '3306')
    host = os.getenv('HOST', '172.17.0.2')
    password = os.getenv('PASSWORD', 'root')
    db_user = os.getenv('DB_USER', 'root')
    db_name = os.getenv('DB_NAME', 'notesdb')  

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjahghkjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{password}@{host}:{port}/{db_name}'
    db.init_app(app)

    metrics = PrometheusMetrics(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


