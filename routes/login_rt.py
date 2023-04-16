from flask import Blueprint, make_response, jsonify, request
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.exceptions import Unauthorized

from connect_to_postgressql.for_sessions import do_login
from extensions.login_manager import lm
from object_user.User import User
from to_complement.cryptografic import encrypth

auth_bp = Blueprint('auth', __name__)


# Creacion de la ruta usual para el login, recibe un dpi y un nombre y confirma la existencia de dicha combinacion en
# la base de datos
@auth_bp.route('/login', methods=['POST'])
def login():
    # Si se confirma que el metodo utilizado es POST se utiliza lo obtenido para agregar datos a la tabla login de la
    # base de datos

    # Realiza el proceso para la confirmacion del login y se obtiene una respuesta
    reque = request.get_json()
    process = do_login(reque)

    # Si el proceso no es exitoso se manda el codigo 404
    if process['error'] != 202:
        return make_response(jsonify({'message': process['message']}), process['error'])
    data = dict()

    data.update({'dpi': reque['dpi'], 'password': reque['clave']})

    id = encrypth(data)
    user = User(id)
    resp = make_response(jsonify({'message': process['message'],
                                  'rol': user.get_rol(),
                                  'sessionToken': id}), 200)
    login_user(user, remember=True)
    return resp


@lm.request_loader
def load_user_from_request(request):
    # Obtiene el token de sesión de la cabecera "Authorization" de la solicitud HTTP
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    # Verifica el token de sesión y devuelve el usuario autenticado
    if auth_token:
        user = User(auth_token)
        if user:
            return user

    # Si el token no es válido, lanza una excepción Unauthorized (401)
    raise Unauthorized('Unauthorized')


@lm.user_loader
def load_user(user_id):
    return User(user_id)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Cierre de sesión exitoso.'})


@auth_bp.route('/confirmar')
@login_required
def procter():
    dp = current_user.important_data()
    return jsonify(dp)
