#!/usr/bin/python3
"""
Script for endpoint that retrieves the number of each objects
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    '''This gets the status of the API'''
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    '''This gets the number of objects for each type.'''
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
