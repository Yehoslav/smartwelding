"""The view to crate a WPS."""
from flask import Blueprint
from flask import render_template, request, jsonify
from flask import Markup
from website.welding.svg_edit import WPSData, generate_svg, FillerMaterial, BaseMaterial, Refractary, ProjectData, Gas, HeatTreatment

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
            return val, 200

        except Exception as err:
            print(err)
            return 'BAD', 200

    elif request.method == 'GET':
        return 'some text'


@wps_view.route('/wps', methods=['GET', 'POST'])
def generate_wps():
    """Generate and return WPS."""
    if request.method == 'POST':
        # TODO: Add to chash template.svg, the wps_data, and the generated svg
        form_data = request.get_json()
        i = 1 if form_data['similarMaterial'] else 2
        message = WPSData(
            filler_material=FillerMaterial(
                name=form_data['fillerMaterial'],
                norm=form_data['fillerNorm'],
                thickness=float(form_data['fillerThickness']),
                dry='dry' in form_data,
                procedure_type=form_data['process'],
            ),
            base_material1=BaseMaterial(
                thickness=float(form_data['thickness1']),
                group=form_data['steelGroup1'],
                norm=form_data['steelNorm1'],
                name=form_data['steelGrade1']
            ),
            base_material2=BaseMaterial(
                thickness=float(form_data[f'thickness{i}']),
                group=form_data[f'steelGroup{i}'],
                norm=form_data[f'steelNorm{i}'],
                name=form_data[f'steelGrade{i}']
            )
        )

        dwg = generate_svg(message)
        return dwg.replace("210mm", "157.5mm").replace("297mm", "222.75mm")

    return render_template("wps_input.html", dwg="")


@wps_view.route('/wps/preview', methods=['GET', 'POST'])
def preview_wps():
    """Generate and return WPS."""
    if request.method == 'POST':
        # TODO: Add to chash template.svg, the wps_data, and the generated svg
        form_data = request.get_json()
        i = 1 if form_data['similarMaterial'] else 2
        message = WPSData(
            filler_material=FillerMaterial(
                name=form_data['fillerMaterial'],
                norm=form_data['fillerNorm'],
                thickness=float(form_data['fillerThickness']) if form_data['fillerThickness'] else '',
                dry='dry' in form_data,
            ),
            base_material1=BaseMaterial(
                thickness=float(form_data['thickness1']) if form_data['thickness1'] else '',
                group=form_data['steelGroup1'],
                norm=form_data['steelNorm1'],
                name=form_data['steelGrade1']
            ),
            base_material2=BaseMaterial(
                thickness=float(form_data[f'thickness{i}']) if form_data[f'thickness{i}'] else '',
                group=form_data[f'steelGroup{i}'],
                norm=form_data[f'steelNorm{i}'],
                name=form_data[f'steelGrade{i}']
            ),
            refractary=Refractary(
                diameter=form_data['refractaryDiameter'],
                electrode_type=form_data['refractaryType']
            ),
            gas_root=Gas(
                debit=form_data['gasRootDebit'],
                gas_type=form_data['gasRootType']
            ),
            gas_cover=Gas(
                debit=form_data['gasCoverDebit'],
                gas_type=form_data['gasCoverType']
            ),
            project_data=ProjectData(
                position=form_data['position'],
                w_process=form_data['process'],
                joint_type=form_data['jointType']
            ),
            heat_tratment=HeatTreatment(
                preheat=form_data['preheat'],
                postheat=form_data['postheat']
            )
        )

        dwg = generate_svg(message)
        return dwg.replace("210mm", "157.5mm").replace("297mm", "222.75mm")

    return render_template("wps_input.html", dwg="")
