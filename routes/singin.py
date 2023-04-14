from flask import request, jsonify, make_response, Blueprint
from flask_login import login_required, current_user
from connect_to_postgressql.for_sessions import get_login, do_sing_in, get_sing_in_code

in_bp = Blueprint('in', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@in_bp.route('/singin', methods=['GET', 'POST'])
def sing_in():
    if request.method == 'GET':
        # Si se confirma que el metodo utilizado es GET se le devuelven los datos de la tabla sing in al usuario
        return jsonify(get_login())
    elif request.method == 'POST':
        # Si se confirma que el metodo utilizado es POST se utiliza lo obtenido para agregar datos a la tabla sing in
        # de la base de datos
        # Realiza el proceso para la confirmacion del sing in y se obtiene una respuesta
        process = do_sing_in(request.get_json())

        # Si el proceso no es exitoso se manda el codigo 404
        if process['error'] != 202:
            return make_response(jsonify({'message': process['message']}), process['error'])

        return jsonify({'message': process['message']})


@in_bp.route('/access_code', methods=['POST'])
@login_required
def access_code():
    if current_user.get_rol() == 'Admin':
        data = request.get_json()
        return jsonify(get_sing_in_code(data['role']))
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response
