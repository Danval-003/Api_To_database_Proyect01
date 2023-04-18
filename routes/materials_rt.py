from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_material_inventory import *
from extensions.comprobation_funtions import comprobation_inventory
from flask_login import current_user, login_required

from extensions.unauthorized import unauthorized

materials_bp = Blueprint('materials', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@materials_bp.route('/verifyInventory', methods=['GET'])
@login_required
def verify_inventory():
    conn = current_user.get_my_user_conection()

    if comprobation_inventory():
        response = material_inventory(conn)
        return make_response(jsonify(response), response['error'])

    return unauthorized()


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@materials_bp.route('/verifyExpired', methods=['GET'])
@login_required
def verify_expired():
    conn = current_user.get_my_user_conection()

    if comprobation_inventory():
        response = material_expired(conn)
        return make_response(jsonify(response), response['error'])

    return unauthorized()
