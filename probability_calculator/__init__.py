import scipy.stats as sp
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

STD_DEV = 12.0


def calculate_probability(spread, std_dev):
    return sp.norm.sf(0.5, spread, std_dev)


class WinProbability(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('spread', required=True, type=str)

        args = parser.parse_args()

        favourite_win = calculate_probability(float(args.spread), STD_DEV)
        outsider_win = 1 - favourite_win

        return{'message': 'POST really was excellent', 'favouriteProbability': favourite_win,
               'outsiderProbability': outsider_win}, 200


api.add_resource(WinProbability, '/winProbability')
