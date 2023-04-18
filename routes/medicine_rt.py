from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_patients import *
from extensions.comprobation_funtions import comprobation_medic
from extensions.unauthorized import unauthorized
from flask_login import current_user, login_required

medicine_bp = Blueprint('medicine', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@medicine_bp.route('/patients', methods=['GET', 'POST'])
@login_required
def obtain_patients_list():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    if request.method == 'GET':
        response = patients(conn)
        return make_response(jsonify(response), response['error'])

    if request.method == 'POST':
        response = patient_now(conn, request.get_json()['id_patient'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/expedient', methods=['POST'])
@login_required
def obtain_expedient():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = expedient(conn, request.get_json()['id_patient'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/tratamient', methods=['POST'])
@login_required
def obtain_consult():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = tratamient(conn, request.get_json()['id_consult'])
    return make_response(jsonify(response), response['error'])


