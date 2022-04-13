"""The init file for the website module."""
from flask import Flask


def create_app():
    """Creates the flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PocketEngineer'

    from .wps_view import wps_view
    from .param_view import param_view

    app.register_blueprint(wps_view, url_prefix='/')
    app.register_blueprint(param_view, url_prefix='/params')

    return app
