from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_material_inventory import material_inventory
from extensions.comprobation_funtions import comprobation_inventory
from flask_login import current_user, login_required

from extensions.unauthorized import unauthorized

materials_bp = Blueprint('materials', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@materials_bp.route('/verify_inventory', methods=['GET', 'POST'])
@login_required
def verify_inventory():
    conn = current_user.get_my_user_conection()

    if comprobation_inventory():
        return material_inventory(conn)

    return unauthorized()

