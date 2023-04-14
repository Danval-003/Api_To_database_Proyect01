"""
Universidad del Valle de Guatemala
Proyecto 2
Bases de Datos I
Seccion 20
Daniel Armando Valdez Reyes|21240
Diego Alexander Hernandez Silvestre|21270
Kristopher Javier Alvarado Lopez|21188

Description:
Rutas de la Api para el manejo de la base de datos
"""

# Imports de las librerias utilizadas para la creación de la Api y el manejo de los datos JSON, Y el permiso para que
# acepte Cors
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from extensions.login_manager import lm
from routes.to_login import auth_bp
from routes.singin import in_bp
# Se importa el modulo para conectar con postgres

# Asignacion de la declaracion del modulo actual
app = Flask(__name__)

# Se instancia para aceptar CORS
CORS(app)

# Crear una instancia de LoginManager:
login_manager = lm

login_manager.init_app(app)

# Se crea una clave secreta para encriptar el login
app.secret_key = 'danta2024'

app.register_blueprint(auth_bp)
app.register_blueprint(in_bp)


@login_manager.unauthorized_handler
def unauthorized():
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response


# Ruta por defecto de la Api
@app.route('/')
def hello_world():
    return '''
    <h1>Se bienvenido a nuestra Api<h1>
    <h2>Version 2.2: Moduled Version<h2>
    '''


# Programa principal para correr el Api Flask
if __name__ == '__main__':
    app.run()
