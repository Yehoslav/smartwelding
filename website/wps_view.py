"""The view to crate a WPS."""
from flask import Blueprint
from flask import render_template, request, jsonify
from flask import Markup

wps_view = Blueprint('wps_view', __name__)


@wps_view.route('/')
def homepage():
    return render_template("home.html")


@wps_view.route('/about')
def aboutpage():
    return render_template("about.html")


@wps_view.route('/test', methods=['GET', 'POST'])
def wpss():
    if request.method == 'POST':
        from website.welding.standards import ISO2560, SubType, ISOError
        data = request.get_json()
        try:
            match data:
                case {'electrode': el, 'norm': 'EN ISO 2560-A'}:
                    val = ISO2560().decode(el, SubType.A)
                case {'electrode': el, 'norm': 'EN ISO 2560-B'}:
                    val = ISO2560().decode(el, SubType.B)
                case _:
                    val = data

            print(val)
            return val, 200
        except Exception as err:
            print(err)
            return 'BAD', 200

    elif request.method == 'GET':
        return 'some text'


@wps_view.route('/wps', methods=['GET', 'POST'])
def edit_wps():
    """The homepage."""
    if request.method == 'POST':
        # TODO: Add to chash template.svg, the wps_data, and the generated svg
        from website.welding.svg_edit import WPSData
        from website.welding.svg_edit import generate_svg
        from website.welding.svg_edit import FillerMaterial
        from website.welding.svg_edit import BaseMaterial
        form_data = request.form.to_dict()
        i = 1 if 'similarMaterial' in form_data else 2
        message = WPSData(
            filler_material=FillerMaterial(
                name=form_data['filler-material'],
                norm=form_data['filler-norm'],
                thickness=float(form_data['filler_thickness']),
                dry='dry' in form_data,
                procedure_type=form_data['procedee'],
            ),
            base_material1=BaseMaterial(
                thickness=float(form_data['thickness1']),
                group=form_data['steel-group1'],
                norm=form_data['steel-norm1'],
                name=form_data['steel-grade1']
            ),
            base_material2=BaseMaterial(
                thickness=float(request.form.get(f'thickness{i}')),
                group=form_data[f'steel-group{i}'],
                norm=form_data[f'steel-norm{i}'],
                name=form_data[f'steel-grade{i}']
            )
        )
        print(request.form.to_dict())

        dwg = generate_svg(message)
        return render_template("wps_input.html", dwg=Markup(dwg
                                                            .replace("210mm", "157.5mm")
                                                            .replace("297mm", "222.75mm")))
    return render_template("wps_input.html", dwg="")
