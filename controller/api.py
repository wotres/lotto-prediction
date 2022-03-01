from flask import Blueprint
from service import Api

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/lotto/data', methods=['GET'])
def lotto_data():
    api = Api.Api()

    return api.get_data()
