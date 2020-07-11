import scipy.stats as sp
from scipy.optimize import minimize
from flask import Flask, g, Response
from flask_restful import Resource, Api, reqparse
import numpy as np
import pandas as pd

app = Flask(__name__)

api = Api(app)

STD_DEV = 12.0


def calculate_probability(spread, std_dev):
    return sp.norm.sf(0.5, spread, std_dev)

# def mean_squared_error(expected_probabilities=[19.09,22.15,77.08,23.08]):


spreads = [10.5, 9.5, 10, 8.5]

expected_probabilities = [0.8091, 0.7785, 0.7708, 0.7692]

constraint = 0.00


# def calculate_mse(spreads):
#     spread_inputs = np.array(spreads)
#     model_probabilities= calculate_probability(spread_inputs,12.0)
#     subtracted_vector = np.subtract(model_probabilities,expected_probabilities)
#     vector_powered = np.power(subtracted_vector,2)
#     mse_sum = np.sum(vector_powered)
#     return mse_sum/len(spreads)


def calculate_mse(std_dev):
    spread_inputs = np.array(spreads)
    model_probabilities = calculate_probability(spread_inputs, std_dev)
    subtracted_vector = np.subtract(
        model_probabilities, expected_probabilities)
    vector_powered = np.power(subtracted_vector, 2)
    mse_sum = np.sum(vector_powered)
    return mse_sum / len(spreads)

class WinProbability(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('spread', required=True, type=str)

        args = parser.parse_args()

        favourite_win = calculate_probability(float(args.spread), STD_DEV)
        outsider_win = 1 - favourite_win

        return{'message': 'POST really was excellent', 'favouriteProbability': favourite_win,
               'outsiderProbability': outsider_win}, 200


class Transformation(Resource):

    def get(self):
        return{'data': calculate_mse(11.0).tolist()}, 200

class Minimize(Resource):

    std_dev_guess = 12.0
    result = minimize(calculate_mse, std_dev_guess)
    final_result = pd.Series(result).to_json(orient='values')

    def get(self):
        return {'data': self.final_result}, 200

api.add_resource(Minimize, '/minimize')
api.add_resource(WinProbability, '/winProbability')
api.add_resource(Transformation, '/transformation')
