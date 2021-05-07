#!/usr/bin/python3
"""City View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        if request.method == 'GET':
            city_list = state.cities
            new_list = []
            for city in city_list:
                new_list.append(city.to_dict())
            return jsonify(new_list)
        else:
            json = request.get_json()
            print(json)
            if json is None:
                abort(400, 'Not a JSON')
            if 'name' not in json.keys():
                abort(400, 'Missing name')
            print("Creando city")
            json['state_id'] = state_id
            new_city = City(**json)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def cities(city_id=None):
    city = storage.get(City, city_id)
    if city is not None:
        if request.method == 'GET':
            return jsonify(city.to_dict())
        elif request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            for key, value in json.items():
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
    else:
        abort(404)
