#!/usr/bin/python
from healthcode import app
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, fields, marshal_with, marshal
from flask.ext.restful.utils import cors

"""
More information about Flask RESTful:
http://flask-restful.readthedocs.org/en/latest/installation.html

More documentation on cors (cross origin resource sharing):
https://github.com/twilio/flask-restful/pull/131
"""

app = Flask(__name__)
api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*’)]

DRUGS = [
	{ 'name': 'drug a', 'drug a side effects': {'side effect': 'side effect a1', 'side effect': 'side effect a2' }},
	{ 'name': 'drug b', 'drug b side effects': {'side effect': 'side effect b1', 'side effect': 'side effect b2' }},
	{ 'name': 'drug c', 'drug c side effects': {'side effect': 'side effect c1', 'side effect': 'side effect c2' }}
]

#only output the .task. field
fields = {
	'drug': fields.String
}

# Drug
#   show a single drug item and lets you delete them
class Drug(restful.Resource):

	# Note: There seems to be a way to you implement decorators
	# on all of the classes, but I'm not sure how to do this. More information
	# here: http://flask-restful.readthedocs.org/en/latest/extending.html#resource-method-decorators	
	@marshal_with(fields)
	def get(self, drug_id):
		if not(len(DRUGS) > drug_id >= 0) or DRUGS[drug_id] is None:
			abort(404, message="Drug {} doesn't exist".format(drug_id))
		return DRUGS[drug_id]

	def delete(self, drug_id):
		if not(len(DRUGS) > drug_id >= 0):
			abort(404, message="Drug {} doesn't exist".format(drug_id))
		DRUGS[drug_id] = None
		return "", 204

# DrugList
#   shows a list of all drugs, and lets you POST to add new drugs
parser = reqparse.RequestParser()
parser.add_argument('drug', type=str)

class DrugList(restful.Resource):

	@marshal_with(fields)
	def get(self):
		return DRUGS

	def post(self):
		args = parser.parse_args()
		task = {'drug': args['drug']}
		DRUGS.append(task)
		return marshal(task, fields), 201


## Actually setup the Api resource routing here
api.add_resource(DrugList, '/drug')
api.add_resource(Drug, '/drug/<int:drug_id>')

if __name__ == '__main__':
	app.run(debug=True)
