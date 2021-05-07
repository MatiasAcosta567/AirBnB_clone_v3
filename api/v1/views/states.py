#!/usr/bin/python3
"""State View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states(state_id=None):
    new_dict = storage.all(State)
    if request.method == 'GET':
        if state_id is None:
            json = []
            for key, value in new_dict.items():
                json.append(value.to_dict())
            return jsonify(json)
        else:
            for key, value in new_dict.items():
                if state_id == value.id:
                    return jsonify(value.to_dict())
            abort(404)
    elif request.method == 'DELETE':
        if state_id is not None:
            for key, value in new_dict.items():
                if state_id == value.id:
                    storage.delete(value)
                    return jsonify({}), 200
            abort(404)
    elif request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if 'name' not in json.keys():
            abort(400, 'Missing name')
        else:
            new_state = State(**json)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
    elif request.method == 'PUT':
        if state_id is not None:
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            state = storage.get(State, state_id)
            if state is not None:
                for key, value in json.items():
                    setattr(state, key, value)
                state.save()
                return jsonify(state.to_dict()), 200
            else:
                abort(404)
