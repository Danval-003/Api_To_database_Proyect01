"""
Universidad del Valle de Guatemala
Proyecto 2
Bases de Datos I
Seccion 20
Daniel Armando Valdez Reyes|21240
Diego Alexander Hernandez Silvestre|21270
Kristopher Javier Alvarado Lopez|21188

Descripcion:
Rutas de la Api para el manejo de la base de datos
"""

# Imports de las librerias utilizadas para la creación de la Api y el manejo de los datos JSON, Y el permiso para que
# acepte Cors
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from to_complement.cryptografic import encrypth

from object_user.User import User
# Se importa el modulo para conectar con postgres
from connect_to_postgressql.for_sessions import *

# Asignacion de la declaracion del modulo actual
app = Flask(__name__)

# Se instancia para aceptar CORS
CORS(app)

# Crear una instancia de LoginManager:
login_manager = LoginManager(app)

# Se crea una clave secreta para encriptar el login
app.secret_key = 'danta2024'


# Creacion de la ruta usual para el login, recibe un dpi y un nombre y confirma la existencia de dicha combinacion en
# la base de datos
@app.route('/login', methods=['POST'])
def login():
    # Si se confirma que el metodo utilizado es POST se utiliza lo obtenido para agregar datos a la tabla login de la
    # base de datos

    # Realiza el proceso para la confirmacion del login y se obtiene una respuesta
    reque = request.get_json()
    process = do_login(reque)

    # Si el proceso no es exitoso se manda el codigo 404
    if process['error'] != 202:
        return make_response(jsonify({'message': process['message']}), process['error'])

    reque.update({'role': process['role']})
    reque.update({'nombre': process['nombre']})
    user = User(encrypth(reque))
    process.pop('role')
    login_user(user, remember=True)
    return jsonify({'message': process['message']})


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Cierre de sesión exitoso.'})


@app.route('/confirmar')
@login_required
def procter():
    dp = current_user.important_data()
    return jsonify(dp)


@login_manager.unauthorized_handler
def unauthorized():
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@app.route('/singin', methods=['GET', 'POST'])
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


@app.route('/access_code', methods=['POST'])
@login_required
def access_code():
    if current_user.get_rol() == 'Admin':
        data = request.get_json()
        return jsonify(get_sing_in_code(data['rol']))
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response


# Ruta por defecto de la Api
@app.route('/')
def hello_world():
    return '<h1>Se bienvenido a nuestra Api<h1>'


# Programa principal para correr el Api Flask
if __name__ == '__main__':
    app.run()
