"""The view that will manage the comunication with the database.
It might have a user interface, but only an overview over the standards."""
import os
import json
from website.settings import APP_STATICFILES_DIR
from flask import Blueprint
from flask import request, jsonify
from flask import Markup

data_view = Blueprint('data_view', __name__)


@data_view.route('/std/iso544')
def iso544():
    if request.method == 'GET':
        with open(os.path.join(APP_STATICFILES_DIR,
            'standards/json/iso544.json'), 'r', encoding='UTF-8') as file:
            iso544_f = json.load(file)

        request_data = request.args.to_dict()
        w_process = int(request_data['process']) if 'process' in request_data else 111
        field = request_data['field'] if 'field' in request_data else 'diameters'
        diameters: list[float] = []
        for product_type in iso544_f['data']:
            if w_process in product_type['w_process']:
                diameters = product_type['diameters']
                break

        print(diameters)
        return jsonify(diameters), 200

@data_view.route('/std/steels')
def steels():
    """Returns a list of steels, and other requested data, from the selected standard"""
    if request.method == 'GET':
        # request_data = {
        #   'norm': str     # the steel standard
        #   'fields': str    # the requested data
        # }
        request_data = request.args.to_dict()
        with open(os.path.join(APP_STATICFILES_DIR,
            f'standards/json/{request_data["norm"]}.json'), 'r', encoding='UTF-8') as file:
            norm = json.load(file)
        return_data = norm['steels']
        if 'fields' in request_data:
            return_data = [ data[request_data['fields']] for data in return_data ]
        return jsonify(return_data)



