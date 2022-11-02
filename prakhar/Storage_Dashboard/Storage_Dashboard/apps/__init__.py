# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from importlib import import_module


db = SQLAlchemy()
new_db = MySQL()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Root@123'
    app.config['MYSQL_DATABASE_DB'] = 'USERMGT'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    new_db.init_app(app)

    register_extensions(app)

    app.register_blueprint(github_blueprint, url_prefix="/login")
    
    register_blueprints(app)
    configure_database(app)
    return app
