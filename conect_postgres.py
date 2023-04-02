"""
Universidad del Valle de Guatemala
Proyecto 2
Bases de Datos I
Seccion 20
Daniel Armando Valdez Reyes|21240
Diego Alexander Hernandez Silvestre|21270
Kristopher Javier Alvarado Lopez|21188

Descripcion:
Modulo para las conexiones a la base de datos en postgres
"""

# Se importa la libreria para realizar la conexion y los querys a la base de datos
import psycopg2
import secrets
import string
# Se importa el modulo extra que se asegura de que los parametros que se obtengan de la base de datos o que se
# registren sean correctos
from correc_params import *


# Funcion que realiza la coneccion a la base de datos
def connect(user='postgres', password='postgres123'):
    # Se le manda la informacion para realizar la coneccion
    conn = psycopg2.connect(
        host="uvg-bd-p2v2.czfikro2hw8h.us-east-2.rds.amazonaws.com",
        database="postgres",
        user=user,
        password=password
    )
    return conn


# Funcion que agrega los datos obtenidos a la base de datos
def do_sing_in(data):
    # Se crea una variable para almacenar el estado del mensaje que se manda
    status = {
        "error": 202,
        "message": "Datos agregados exitosamente"
    }
    if not ('dpi' in data) or not ('nombre' in data) or not ('codigo_acceso' in data) or not ('clave' in data):
        status['error'] = 400
        status['message'] = '''Esta intentando hacer post con un objeto incorrecto, el formato real es:
        {
            dpi: NUMERO DPI,
            nombre: NOMBRE PERSONA,
            access_code: VARCHAR Codigo
        }
        '''
        return status

    # Se realiza un Try para que intente la conexion a la base de datos y ejecute el query para agregar datos a la
    # tabla login
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM code_permition where codigo_acceso = '" + data['codigo_acceso'] + "'")
        rows = cur.fetchall()
        if len(rows) == 0:
            status['error'] = 400
            status['message'] = 'No existe el codigo de acceso con el que intento acceder'
            return status

        rol = rows[0][1]

        cur.execute("INSERT INTO usuarios_app (dpi,nombre, clave, rol) VALUES (%s, %s, %s, %s)",
                    (data['dpi'], first_mayus(data['nombre']), data['clave'], rol))
        cur.execute(
            "DELETE FROM public.code_permition WHERE codigo_acceso LIKE '" + data['codigo_acceso'] + "' ESCAPE '#'")
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary

    # Se retorna el estatus de la operacion
    return status


# Regresa los datos de la tabla login en formato JSON
def get_sing_in_code(role):
    alphabet = string.digits + string.ascii_letters + string.punctuation

    access_code = ''
    rols = {
        'Admin': 15,
        'Medico': 12,
        'Inventario': 8
    }
    existe = False
    conn = connect()
    cur = conn.cursor()
    while not existe:
        for i in range(rols[role]):
            access_code = access_code + secrets.choice(alphabet)
        cur.execute("SELECT * FROM code_permition where codigo_acceso = '" + access_code + "'")
        rows = cur.fetchall()
        if len(rows) == 0:
            existe = not existe

    cur.execute("INSERT INTO code_permition(codigo_acceso, rol) VALUES ('" + access_code + "','" + role + "')")
    conn.commit()
    cur.close()
    conn.close()
    # Se regresa los datos de la tabla login
    return {'access_code': access_code}


# Regresa los datos de la tabla login en formato JSON
def get_login():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios_app")
    rows = cur.fetchall()  # El cursor obtiene los datos en las filas
    data = []
    for row in rows:
        # Cada fila se trata de colocar en formato JSON
        data.append({
            "dpi": row[0],
            "nombre": row[1],
            "clave": row[2],
            "rol": row[3]
        })
    cur.close()
    conn.close()
    # Se regresa los datos de la tabla login
    return data


# Regresa los datos de la tabla login en formato JSON
def do_login(data_login):
    status = {
        "error": 202,
        'message': ''
    }
    conn = connect()
    cur = conn.cursor()
    if not ('dpi' in data_login) or not ('clave' in data_login):
        status['error'] = 400
        status['message'] = '''Esta intentando hacer post con un objeto incorrecto, el formato real es:
        {
            dpi: NUMERO DPI,
            clave: CLAVE DE LA PERSONA- TEXTO
        }
        '''
        return status

    cur.execute("SELECT * FROM usuarios_app where dpi = %s and clave =%s",
                (data_login["dpi"], first_mayus(data_login["clave"])))
    rows = cur.fetchall()  # El cursor obtiene los datos en las filas

    if len(rows) == 1:
        status['message'] = 'Se encontro un match Login correcto'
        status['dpi'] = rows[0][0]
        status['nombre'] = rows[0][1]
        status['role'] = rows[0][3]
    elif len(rows) > 1:
        status['error'] = 404
        status['message'] = 'Alguien se canto en la base de datos, hay mas de un login encontrado'
    else:
        status['error'] = 404
        status['message'] = 'No se obtuvo nada'

    cur.close()
    conn.close()
    # Se regresa los datos de la tabla login
    return status
