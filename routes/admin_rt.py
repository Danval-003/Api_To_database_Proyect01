from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_admin import *
from extensions.comprobation_funtions import comprobation_admin
from flask_login import current_user, login_required

from extensions.unauthorized import unauthorized

admin_bp = Blueprint('admin', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@admin_bp.route('/bitacora', methods=['GET'])
@login_required
def verify_inventory():
    conn = current_user.get_my_user_conection()

    if comprobation_admin():
        response = obtain_bitacora(conn)
        return make_response(jsonify(response), response['error'])

    return unauthorized()


@admin_bp.route('/editDoctorUnit', methods=['POST'])
@login_required
def change_doctor():
    conn = current_user.get_my_user_conection()

    res = request.get_json()

    data = [res['dpiDoctor'], res['idUnit']]

    if comprobation_admin():
        response = editDoctorUnit(conn, tuple(data))
        return make_response(jsonify(response), response['error'])

    return unauthorized()


@admin_bp.route('/showUnitHealth', methods=['POST'])
@login_required
def verify_doctor_unit_history():
    conn = current_user.get_my_user_conection()

    if comprobation_admin():
        dpiDoctor = request.get_json()['dpiDoctor']
        response = obtain_DoctorUnit(conn, dpiDoctor)
        return make_response(jsonify(response), response['error'])

    return unauthorized()