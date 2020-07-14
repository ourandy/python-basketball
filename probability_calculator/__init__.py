from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from http import HTTPStatus
from scipy import stats, optimize
import numpy as np

app = Flask(__name__)
api = Api(app)

class WinProbability(Resource):

    @staticmethod
    def calculate_probability(spread):

        STD_DEV = 12.0
        favourite_win = stats.norm.sf(0.5,spread,STD_DEV)
        outsider_win = 1 - favourite_win

        return np.array([favourite_win,outsider_win])

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('spread', required=True, type=float)
        args = parser.parse_args()
        result = self.calculate_probability(args.spread)

        return{'message': 'POST really was excellent', 'favouriteProbability': result[0],
               'outsiderProbability': result[1]}, HTTPStatus.OK

class MinimizeEndPoint(Resource):

    def solve(self, spread, expected, stddev):
        spread = np.array(spread)
        expected = np.array(expected)

        def mse(s):
            estimated = stats.norm.sf(0.5, spread, scale=s)
            mse = np.sum(np.power((estimated - expected), 2)) / spread.size
            return mse
        optimal_solution = optimize.minimize(mse, stddev)
        print(optimal_solution)

        return optimal_solution

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('spread', action='append',
                            type=float, required=True)
        parser.add_argument('expected', action='append',
                            type=float, required=True)
        parser.add_argument('stddev', type=float, required=True)
        args = parser.parse_args()
        res = self.solve(**args)
        print(res)

        return {
            "optimum": res.x[0],
            "fun": res.fun
        }, HTTPStatus.OK


api.add_resource(MinimizeEndPoint, '/minimize')
api.add_resource(WinProbability, '/winprobability')
