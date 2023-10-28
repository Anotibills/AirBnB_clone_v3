#!/usr/bin/python3
"""
Script that creates a new view for Amenity objects that handles all default
RESTful API for class Amenity
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''This returns all amenity objects in JSON form'''
    amenities = [
                 amenity.to_dict() for amenity in storage.all(Amenity).values()
    ]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    '''This return amenity with the given ID'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    '''This creates a new amenity object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''This deletes an amenity object given an amenity ID'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''This updates an existing amenity object'''
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if 'name' in data:
        amenity.name = data['name']
        amenity.save()
    return jsonify(amenity.to_dict()), 200
