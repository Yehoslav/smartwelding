"""The view to crate a WPS."""
from flask import Blueprint
from flask import render_template, request
from flask import Markup


wps_view = Blueprint('wps_view', __name__)


@wps_view.route('/')
def homepage():
    return render_template("home.html")


@wps_view.route('/wps', methods=['GET', 'POST'])
def edit_wps():
    """The homepage."""
    if request.method == 'POST':
        # TODO: Add to chash template.svg, the wps_data, and the generated svg
        from website.welding.svg_edit import WPSMessages
        from website.welding.svg_edit import generate_svg
        message = WPSMessages(None)
        message.thickness = request.form.get('thickness')
        dwg = generate_svg(message)
        return render_template("wps_input.html", dwg=Markup(dwg))
    return render_template("wps_input.html", dwg="")
