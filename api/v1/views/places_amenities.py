#!/usr/bin/python3
"""Amenities View"""

from os import getenv
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage_t


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """get amenity information for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'],
                 strict_slashes=False)
def post_amenities(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is not None and amenity is not None:
        if request.method == 'POST':
            if storage_t == 'db':
                place_amenities = place.amenities
            else:
                place_amenities = place.amenity_ids
            if amenity in place_amenities:
                return jsonify(amenity.to_dict())
            place_amenities.append(amenity)
            place.save()
            return make_response(jsonify(amenityto_dict()), 201)
        else:
            if os.getenv('HBNB_TYPE_STORAGE') == 'db':
                place_amenities = place.amenities
            else:
                place_amenities = place.amenity_ids
            if amenity not in place_amenities:
                abort(404)
            place_amenities.remove(amenity)
            place.save()
            return jsonify({})
    abort(404)
