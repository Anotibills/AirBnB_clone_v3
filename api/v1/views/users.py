#!/usr/bin/python3
"""
Script that creates a new view for User object that handles all default
RESTful API for class User
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    Return all user objects in JSON form.
    '''
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    '''This returns user with the given ID'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''This create a new user object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''This updates an existing user object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    ignore = {"id", "email", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''This delete a user object given a user ID'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
