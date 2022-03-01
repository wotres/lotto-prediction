from flask import Blueprint, Response
from service import Prediction
import json

bp = Blueprint('prediction', __name__, url_prefix='/prediction')
prediction = Prediction.Prediction(1, 5)


@bp.route('/check', methods=['GET'])
def check():
    return prediction.check()


@bp.route('/expect', methods=['GET'])
def calculate_statistics():
    expect_nums = [1, 2, 3, 4, 5, 6]
    angle_answer, angle_possibility = prediction.calculate_statistics(expect_nums)
    res = json.dumps({
        'angle_answer': angle_answer,
        'angle_possibility': angle_possibility
    }, ensure_ascii=False).encode('utf8')
    return Response(res, content_type='application/json; charset=utf-8')


@bp.route('/recommend', methods=['GET'])
def recommend():
    max_recommend_numbers = prediction.recommend()
    res = json.dumps([{
        'numbers': max_recommend_number[0],
        'possibility': max_recommend_number[1]
    } for max_recommend_number in max_recommend_numbers], ensure_ascii=False).encode('utf8')

    return Response(res, content_type='application/json; charset=utf-8')