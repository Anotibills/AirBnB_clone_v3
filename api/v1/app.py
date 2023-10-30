#!/usr/bin/python3
"""
Sscript for endpoint (route) that will return the API status
"""
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app_host = os.getenv('HBNB_API_HOST')
app_port = os.getenv('HBNB_API_PORT')
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_flask(exception):
    '''This is the Flask app context end event listener.'''
    storage.close()


@app.errorhandler(400)
def error_400(error):
    '''This handles the 400 HTTP error code'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


@app.errorhandler(404)
def error_404(error):
    '''This handles the 404 HTTP error code'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app_host = '0.0.0.0' if app_host is None else app_host
    app_port = '5000' if app_port is None else app_port
    app.run(host=app_host, port=app_port, threaded=True)
