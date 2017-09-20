"""
Paranuara API
-------------

Defines a Flask-based API to implement Paranuara's government requirements.
"""

from datetime import datetime
import json
import os
import logging
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_restful import Api
from app.models import Company, Person

app = Flask(__name__)
api = Api(app)

logging.info("initialising logs...")
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

@app.route('/sitemap')
def sitemap():
    """List all available endpoints in this server."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@app.route('/v1/companies/<index>/employees')
def company(index):
    """List all employees for a company."""
    company = Company.objects(index=index).first()
    if not company:
        raise ValueError('Company not found')
    return mongo_to_json(company.employees())

@app.route('/v1/people/<index>/special-common-friends-with')
def special_common_friends_with(index):
    """List all common friends to other person (i.e. using query parameter `index_other`) which have brown eyes and are still alive."""
    person = Person.objects(index=index).first()
    if not person:
        raise ValueError('Person not found')
    if not 'index_other' in request.args:
        raise ValueError('Must provide other person to match')
    other_person = Person.objects(index=request.args['index_other']).first()
    if not other_person:
        raise ValueError('Other person not found')
    return mongo_to_json(person.special_common_friends_with(other_person))

@app.route('/v1/people/<index>/diet-preferences')
def diet_preferences(index):
    """List diet preferences for fruit and vegetables for a person"""
    person = Person.objects(index=index).first()
    if not person:
        raise ValueError('Person not found')
    return mongo_to_json(person.diet_preferences())

@app.errorhandler(500)
def server_error(error=None):
    message = {
        'status': 500,
        'message': 'Server Error, ' + str(error) + ": " + request.url
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

def mongo_to_json(obj):
    try:
        resp = obj.to_json()
    except AttributeError:
        resp = json.dumps(obj)
    return Response(resp, status=200, mimetype='application/json')
