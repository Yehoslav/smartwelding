"""The view for calculating the weldint parameters."""
from flask import Blueprint
from flask import render_template, request, jsonify
from flask import Markup

param_view = Blueprint('param_view', __name__)


@param_view.route('/')
def parameters():
    return 'Aici se calculeaza parametrii de sudare'


@param_view.route('/migmag')
def migmag():
    return render_template('migmag.html')
