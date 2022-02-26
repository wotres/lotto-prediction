from flask import Blueprint
from service import Api

bp = Blueprint('answer', __name__, url_prefix='/api')


@bp.route('/lotto/data', methods=['GET'])
def lotto_data():
    api = Api.Api()

    return api.get_data()
