"""The view to crate a WPS."""
from flask import Blueprint
from flask import render_template, request
from flask import Markup

wps_view = Blueprint('wps_view', __name__)


@wps_view.route('/')
def homepage():
    return render_template("home.html")


@wps_view.route('/about')
def aboutpage():
    return render_template("about.html")


@wps_view.route('/wps', methods=['GET', 'POST'])
def edit_wps():
    """The homepage."""
    if request.method == 'POST':
        # TODO: Add to chash template.svg, the wps_data, and the generated svg
        from website.welding.svg_edit import WPSMessages
        from website.welding.svg_edit import generate_svg
        from website.welding.svg_edit import FillerMaterial
        from website.welding.svg_edit import BaseMaterial
        message = WPSMessages(
            filler_material=FillerMaterial(
                name=request.form.get('filler-material'),
                norm="norma",
                thickness=0,
                dry=True,
            ),
            base_material1=BaseMaterial(
                thickness=float(request.form.get('thickness1')),
                group='grupa',
                norm='norma',
                name=request.form.get('steel-grade1')
            ),
            base_material2=BaseMaterial(
                thickness=float(request.form.get('thickness2')),
                group='grupa',
                norm='norma',
                name=request.form.get('steel-grade2')
            )
        )

        dwg = generate_svg(message)
        return render_template("wps_input.html", dwg=Markup(dwg
                                                            .replace("210mm", "157.5mm")
                                                            .replace("297mm", "222.75mm")))
    return render_template("wps_input.html", dwg="")
