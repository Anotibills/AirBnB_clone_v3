#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''The methods allowed for the states endpoint.'''


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    '''The method handler for the states endpoint.'''
    handlers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    '''This gets state name with the given id or all states'''
    all_states = storage.all(State).values()
    if state_id:
        res = next((x for x in all_states if x.id == state_id), None)
        if res:
            return jsonify(res.to_dict())
        raise NotFound()
    all_states = [x.to_dict() for x in all_states]
    return jsonify(all_states)


def add_state(state_id=None):
    '''This adds a new state to the list'''
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def remove_state(state_id=None):
    '''This removes a state with the given id'''
    all_states = storage.all(State).values()
    res = next((x for x in all_states if x.id == state_id), None)
    if res:
        storage.delete(res)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def update_state(state_id=None):
    '''This updates the state name with the given id'''
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = next((x for x in all_states if x.id == state_id), None)
    if res:
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Not a JSON')
        old_state = res
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
