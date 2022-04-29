"""The view that will manage the comunication with the database.
It might have a user interface, but only an overview over the standards."""
import os
import json
from website.settings import APP_STATICFILES_DIR
from flask import Blueprint
from flask import request, jsonify, render_template
from flask import Markup

rugoz_view = Blueprint('rugoz_view', __name__)


@rugoz_view.route('/rugoz')
def rugozitate():
    if request.method == 'GET':
        return render_template("rugoz.html")

