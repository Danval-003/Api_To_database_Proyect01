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
def verify_inventory():
    conn = current_user.get_my_user_conection()


    if 
    data = []
    keys =

    if comprobation_admin():
        response = obtain_bitacora(conn)
        return make_response(jsonify(response), response['error'])

    return unauthorized()