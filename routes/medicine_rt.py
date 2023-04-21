from flask import request, jsonify, make_response, Blueprint
from connect_to_postgressql.for_patients import *
from extensions.comprobation_funtions import comprobation_medic
from extensions.unauthorized import unauthorized
from flask_login import current_user, login_required

medicine_bp = Blueprint('medicine', __name__)


# Creacion de la ruta para el acceso a la Api mediante los metodos GET y POST
@medicine_bp.route('/patients', methods=['GET', 'POST'])
@login_required
def obtain_patients_list():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    if request.method == 'GET':
        response = patients(conn)
        return make_response(jsonify(response), response['error'])

    if request.method == 'POST':
        response = patient_now(conn, request.get_json()['id_patient'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/patientInstant', methods=['GET', 'POST'])
@login_required
def obtain_patient_instant():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()

    if request.method == 'POST':
        id_patient = request.get_json()['key']
        query = "select dpi, nombre from paciente where dpi like '" + str(id_patient) + "%'"
        response = instant(conn, query, ['dpi', 'namePatient', 'Patient'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/unitInstant', methods=['GET', 'POST'])
@login_required
def obtain_unit_instant():
    conn = current_user.get_my_user_conection()

    if request.method == 'POST':
        id_unit = request.get_json()['key']
        query = "select id, nombre from unidad_salud where to_char(id, 'FM99999') like '" + str(id_unit) + "%'"
        response = instant(conn, query, ['dpi', 'nameUnit', 'Unit'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/docInstant', methods=['GET', 'POST'])
@login_required
def obtain_doctor_instant():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()

    if request.method == 'POST':
        id_doctor = request.get_json()['key']
        query = "select dpi, nombre from medico where dpi like '" + str(id_doctor) + "%'"
        response = instant(conn, query, ['dpi', 'nameDoctor', 'Doctor'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/diseaseInstant', methods=['GET', 'POST'])
@login_required
def obtain_disease_instant():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()

    if request.method == 'POST':
        id_disease = request.get_json()['key']
        query = "select id, nombre from enfermedad where to_char(id, 'FM99999') like '" + str(id_disease) + "%'"
        response = instant(conn, query, ['dpi', 'nameDisease', 'Disease'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/productInstant', methods=['GET', 'POST'])
@login_required
def obtain_product_instant():
    conn = current_user.get_my_user_conection()

    if request.method == 'POST':
        id_product = request.get_json()['key']
        query = "select id, descripcion from insumos where to_char(id, 'FM99999') like '" + str(id_product) + "%'"
        response = instant(conn, query, ['dpi', 'nameProduct', 'Product'])
        return make_response(jsonify(response), response['error'])


@medicine_bp.route('/expedient', methods=['POST'])
@login_required
def obtain_expedient():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = expedient(conn, request.get_json()['id_patient'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/tratamient', methods=['POST'])
@login_required
def obtain_consult():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = tratamient(conn, request.get_json()['id_consult'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/exam', methods=['POST'])
@login_required
def obtain_exams():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = examens(conn, request.get_json()['dpi'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/deleteExam', methods=['POST'])
@login_required
def delete_exams():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = deleteExamens(conn, request.get_json()['dpi'], request.get_json()['idExam'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/addExam', methods=['POST'])
@login_required
def add_exams():
    if not comprobation_medic():
        return unauthorized()

    conn = current_user.get_my_user_conection()
    response = addExamens(conn, request.get_json()['dpi'], request.get_json()['idExam'])
    return make_response(jsonify(response), response['error'])


@medicine_bp.route('/editConsult', methods=['POST'])
@login_required
def edit_Consult():
    if not comprobation_medic():
        return unauthorized()

    keys = 'id_patient,nameDoctor,disease,healthUnit,date,description,evolution,id_consult'

    res = request.get_json()
    print(res)
    dataList = []

    try:
        for i in keys.split(','):
            dataList.append(res[i])

        conn = current_user.get_my_user_conection()
        response = editConsult(conn, dataList[0], dataList[1], dataList[2], dataList[3], dataList[4], dataList[5],
                               dataList[6], dataList[7])
        return make_response(jsonify(response), response['error'])

    except psycopg2.IntegrityError as expceptionMsg:
        ex = expceptionMsg + ""
        return make_response(jsonify(ex), 404)


@medicine_bp.route('/editPatient', methods=['POST'])
@login_required
def edit_Patient():
    if not comprobation_medic():
        return unauthorized()

    keys = 'nombre, direccion, fecha_nacimiento, genero, indice_masa_corporal, altura, peso, adicciones, ' \
           'enfermedad_hereditaria, fecha_inicio, status, telefono, dpi'

    res = request.get_json()
    print(res)
    dataList = []

    try:
        for i in keys.split(', '):
            dataList.append(res[i])

        conn = current_user.get_my_user_conection()
        print(dataList)
        response = editPatient(conn, tuple(dataList))
        return make_response(jsonify(response), response['error'])

    except psycopg2.IntegrityError as expceptionMsg:
        ex = expceptionMsg + ""
        return make_response(jsonify(ex), 404)


@medicine_bp.route('/editTratamient', methods=['POST'])
@login_required
def edit_Tratamient():
    if not comprobation_medic():
        return unauthorized()

    keys = 'idInsumo, dosis, fechaInicio, fechaFinal, consulta'

    res = request.get_json()
    print(res)
    dataList = []

    try:
        for i in keys.split(', '):
            dataList.append(res[i])

        conn = current_user.get_my_user_conection()
        print(dataList)
        response = editTratamient(conn, tuple(dataList))
        return make_response(jsonify(response), response['error'])

    except psycopg2.IntegrityError as expceptionMsg:
        ex = expceptionMsg + ""
        return make_response(jsonify(ex), 404)


@medicine_bp.route('/createConsult', methods=['POST'])
@login_required
def create_Consult():
    if not comprobation_medic():
        return unauthorized()

    keys = 'dpi_paciente,id_medico,id_enfermedad,id_unidad_salud,fecha,descripcion,evolucion'

    res = request.get_json()
    print(res)
    dataList = []

    try:
        for i in keys.split(','):
            dataList.append(res[i])

        conn = current_user.get_my_user_conection()
        response = createConsult(conn, tuple(dataList))
        return make_response(jsonify(response), response['error'])

    except psycopg2.IntegrityError as expceptionMsg:
        ex = expceptionMsg + ""
        return make_response(jsonify(ex), 404)
