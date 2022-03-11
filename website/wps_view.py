"""The view to crate a WPS."""
from flask import Blueprint


wps_view = Blueprint('wps_view', __name__)

@wps_view.route('/')
def home():
    """The homepage."""
    return "<h1>Create your WPS here</h1>"
