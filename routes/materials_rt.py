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


@materials_bp.route('/requestProduct', methods=['POST'])
@login_required
def request_product():
    conn = current_user.get_my_user_conection()

    res = request.get_json()

    data = [res['idProduct'], res['idUnit'], res['count'], res['expiredDate']]

    if comprobation_inventory():
        response = requestedProduct(conn, tuple(data))
        return make_response(jsonify(response), response['error'])

    return unauthorized()


@materials_bp.route('/requestProductExpired', methods=['POST'])
@login_required
def request_product_expired():
    conn = current_user.get_my_user_conection()

    res = request.get_json()

    data = [res['idProduct'], res['idUnit'], res['count'], res['expiredDate'], res['oldExpiredDate']]

    if comprobation_inventory():
        response = requestedProductExpired(conn, tuple(data))
        return make_response(jsonify(response), response['error'])

    return unauthorized()


@materials_bp.route('/solicitar', methods=['POST'])
@login_required
def solicitar():
    conn = current_user.get_my_user_conection()

    res = request.get_json()

    data = [int(res['idUnit']), int(res['idProduct']),  int(res['count'])]

    if comprobation_inventory():
        response = solicitarPro(conn, tuple(data))
        return make_response(jsonify(response), response['error'])

    return unauthorized()