"""The view for calculating the weldint parameters."""
from flask import Blueprint
from flask import render_template, request, jsonify
from flask import Markup

param_view = Blueprint('param_view', __name__)


@param_view.route('/')
def parameters():
    return 'Aici se calculeaza parametrii de sudare'


@param_view.route('/carb-eq', methods=['GET', 'POST'])
def carb_eq():
    if request.method == 'POST':
        from website.welding.carbon_echivalent import Steel, ceiiw, ceiiw_formula
        data: dict = request.get_json()
        float_data = {key: float(value) for key, value in data.items()}
        steel = Steel(float_data)
        formula = ceiiw_formula(steel)
        ceq = round(ceiiw(steel), 2)
        return jsonify([formula, ceq])
    return 'Calculul carbonului echivalent nu a fost implementat inca'


@param_view.route('/migmag')
def migmag():
    return render_template('migmag.html')
