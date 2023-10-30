#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Retrieves the list of all State objects'''
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''This adds a new state to the list'''
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_state(state_id):
    '''This removes a state with the given id'''
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''This updates the state name with the given id'''
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            abort(400, description='Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
