import numpy as np
import scipy.stats as sp
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

dataset = [2, 6, 8, 12, 18, 24, 28, 32]

variance = np.var(dataset)


def calculate_probability(x, y):
    return sp.norm(x, y).pdf(x)


class WinProbability(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('supremacy', required=True)
        parser.add_argument('total_points', required=True)

        args = parser.parse_args()

        # return {'message': 'POST really was excellent', 'data':args},200

        # return{'message': 'POST really was excellent', 'data': calculate_probability(args.supremacy, args.total_points)}, 200

        return{'message': 'POST really was excellent', 'data': calculate_probability(0, 1)}, 200


api.add_resource(WinProbability, '/probability')

# print(variance)
