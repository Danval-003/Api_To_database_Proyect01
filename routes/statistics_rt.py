from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_statistics import *
from extensions.comprobation_funtions import comprobation_medic
from extensions.unauthorized import unauthorized
from flask_login import current_user, login_required

statistic_bp = Blueprint('statistics', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@statistic_bp.route('/topDis', methods=['GET'])
@login_required
def obtainTopDiseases():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()

    response = topDiseases(conn)
    return make_response(jsonify(response), response['error'])


@statistic_bp.route('/topDoc', methods=['GET'])
@login_required
def obtainTopDiseases():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()

    response = topDoctors(conn)
    return make_response(jsonify(response), response['error'])
