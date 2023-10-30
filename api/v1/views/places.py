#!/usr/bin/python3
"""
Script that creates a new view for Place objects that handles
all default RESTful API
"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''This return places in the city using GET'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_list = [p.to_dict() for p in city.places]
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''This returns a place and its ID using GET'''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''This deletes a place object given its ID'''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''This create a new place object through city'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    obj_data = request.get_json()
    if "name" not in obj_data or "user_id" not in obj_data:
        return jsonify({"error": "Missing name or user_id"}), 400
    city = storage.get("City", city_id)
    user = storage.get("User", obj_data['user_id'])
    if city is None or user is None:
        abort(404)
    obj_data['city_id'] = city.id
    obj_data['user_id'] = user.id
    obj = Place(**obj_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''This updates an existing place object using PUT'''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ("id", "user_id", "created_at", "updated_at")
    for key, value in obj_data.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON
    in the body of the request
    
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description='Not a JSON')

    states_ids = data.get('states', [])
    cities_ids = data.get('cities', [])
    amenities_ids = data.get('amenities', [])

    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places_result = set()

    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places_result.update(city.places)

    for city_id in cities_ids:
        city = storage.get(City, city_id)
        if city:
            places_result.update(city.places)

    if amenities_ids:
        amenities = [
            storage.get(Amenity, amenity_id)
            for amenity_id in amenities_ids]
        for place in list(places_result):
            if not all(amenity in place.amenities for amenity in amenities):
                places_result.remove(place)

    return jsonify([place.to_dict() for place in places_result])
    """
    """endpoint to retrieves all PlaceObj using passed JSON"""
    abortMSG = "Not a JSON"
    if request.get_json() is None:
        abort(400, description=abortMSG)
    data = request.get_json()
    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        placesList = []
        placesList = [place.to_dict() for place in places]
        res = json.dumps(placesList)
        response = make_response(res, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    placesList = []
    if states:
        statesObj = [storage.get(State, s_id) for s_id in states]
        for state in statesObj:
            if state:
                for city in state.cities:
                    if city:
                        placesList.extend(place for place in city.places)
    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in placesList:
                        placesList.append(place)
    if amenities:
        if not placesList:
            placesList = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        placesList = [place for place in placesList
                      if all([am in place.amenities
                             for am in amenities_obj])]
    places = []
    for aPlace in placesList:
        filtered = aPlace.to_dict()
        filtered.pop('amenities', None)
        places.append(filtered)
    res = json.dumps(places)
    response = make_response(res, 200)
    response.headers['Content-Type'] = 'application/json'
    return response
