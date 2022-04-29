"""The init file for the website module."""
from flask import Flask


def create_app():
    """Creates the flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PocketEngineer'

    from .wps_view import wps_view
    from .param_view import param_view
    from .data_view import data_view
    from .rugoz_view import rugoz_view

    app.register_blueprint(wps_view, url_prefix='/')
    app.register_blueprint(param_view, url_prefix='/params')
    app.register_blueprint(data_view, url_prefix='/data')
    app.register_blueprint(rugoz_view, url_prefix='/')

    return app
