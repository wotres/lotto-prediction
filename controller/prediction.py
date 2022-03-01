from flask import Blueprint, Response
from service import Prediction

bp = Blueprint('prediction', __name__, url_prefix='/prediction')
prediction = Prediction.Prediction(1, 5)


@bp.route('/check', methods=['GET'])
def check():
    return prediction.check()


@bp.route('/expect', methods=['GET'])
def statistic_calculate():
    expect_nums = [1, 2, 3, 4, 5, 6]
    res = prediction.statistic_calculate(expect_nums)
    return Response(res, content_type='application/json; charset=utf-8')
