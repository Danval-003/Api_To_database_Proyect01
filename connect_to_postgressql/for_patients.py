import psycopg2


def patients(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute("SELECT dpi, nombre, direccion, genero  from paciente;")
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron pacientes'
        status['error'] = 404
        return status

    status['data'] = [{
        'id': row[0],
        'name_patient': row[1],
        'address': row[2],
        'gender': row[3]
    } for row in rows]
    return status


def patient_now(conn, id_patient):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute("select * from paciente where dpi = '" + str(id_patient) + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontro el paciente'
        status['error'] = 404
        return status

    status['data'] = [{
        'id': row[12],
        'name_patient': row[0],
        'address': row[1],
        'birthdate': row[2],
        'genre': row[3],
        'corporal_mass': row[4],
        'height': row[5],
        'weight': row[6],
        'addiction': row[7],
        'hereditary_disease': row[8],
        'start_date': row[9],
        'status': row[10],
        'numberTel': row[11]
    } for row in rows]
    return status


def instant(conn, query, structure):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontro el '+structure[2]
        status['error'] = 404
        return status

    status['data'] = [{
        structure[0]: row[0],
        structure[1]: row[1]
    } for row in rows]

    status['type'] = structure[2]
    return status


def expedient(conn, id_patient):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute(''' 
            select m.nombre, e.nombre, us.nombre, fecha, consulta.descripcion, consulta.evolucion, consulta.id  from consulta
                 inner join enfermedad e on e.id = consulta.id_enfermedad
                 inner join medico m on m.dpi = consulta.dpi_medico
                 inner join unidad_salud us on us.id = consulta.id_unidad_salud
            where consulta.dpi_paciente =''' + "'" + str(id_patient) + "'")
    rows = cur.fetchall()
    if len(rows) != 0:
        status['data'] = [{
            'nameDoctor': row[0],
            'disease': row[1],
            'healthUnit': row[2],
            'date': row[3],
            'description': row[4],
            'evolution': row[5],
            'id': row[6]
        } for row in rows]
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def tratamient(conn, id_consult):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute(''' 
            select  i.descripcion, it.fecha_final, it.fecha_inicio, it.dosis, i.id
                from insumos_tratamientos it
                inner join insumos i on i.id = it.id_insumo
            where it.id_consulta = ''' + str(id_consult))
    rows = cur.fetchall()
    if len(rows) != 0:
        status['data'] = [{
            'inputDescription': row[0],
            'finalDate': row[1],
            'startDate': row[2],
            'dose': row[3],
            'id': row[4]
        } for row in rows]
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def examens(conn, dpi):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute(""" 
            select id_examen, e.descripcion from examen_paciente
                 inner join examenes e on e.id = examen_paciente.id_examen
                 where dpi_paciente = '""" + str(dpi) +"'")
    rows = cur.fetchall()
    if len(rows) != 0:
        status['data'] = [{
            'idExam': row[0],
            'nameExam': row[1]
        } for row in rows]
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def deleteExamens(conn, dpi, id):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()

    cur.execute(""" 
            delete from examen_paciente where id_examen = """+str(id)+""" and dpi_paciente = '""" + str(dpi) +"'")
    conn.commit()
    return status


def addExamens(conn, dpi, id):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute(""" 
            insert into examen_paciente(id_examen, dpi_paciente) VALUES (%s, %s)""", (int(id), str(dpi)))

    conn.commit()

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def editConsult(conn, id_patient, id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion, id_consult):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        print(''' 
                select * from edit_consult(%s, %s, %s, %s, %s, %s, %s, %s);''',
              (id_patient, id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion, id_consult))
        cur.execute(''' 
                select * from edit_consult(%s, %s, %s, %s, %s, %s, %s, %s);''',
                    (str(id_patient), id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion,
                     id_consult)
                    )

        conn.commit()
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def createConsult(conn, tuplaInfo):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        cur.execute(''' 
                insert into consulta(dpi_paciente, dpi_medico, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion) 
                values(%s, %s, %s, %s, %s, %s, %s); ''',
                    tuplaInfo
                    )
        conn.commit()
        cur.execute("select id from consulta where dpi_paciente = '"+tuplaInfo[0]+"' order by id limit 1")
        rows = cur.fetchall()
        status['idConsult'] = rows[0][0]
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def editPatient(conn, tupleInformation):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        print(''' 
                select * from edit_general(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
              tupleInformation)
        cur.execute(''' 
                select * from edit_general(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    tupleInformation
                    )

        conn.commit()
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def editTratamient(conn, tupleInformation):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        print(''' 
                select * from edit_tratamient(%s,%s,%s,%s,%s)''',
              tupleInformation)
        cur.execute(''' 
                 select * from edit_tratamient(%s,%s,%s,%s,%s)''',
                    tupleInformation
                    )

        conn.commit()
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def createTratamient(conn, tuplaInfo):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()
    print(''' 
                insert into insumos_tratamientos(id_insumo, dosis, fecha_inicio, fecha_final, id_consulta)
                values(%s, %s, %s, %s, %s); ''',
                    tuplaInfo)

    try:
        cur.execute(''' 
                insert into insumos_tratamientos(id_insumo, dosis, fecha_inicio, fecha_final, id_consulta)
                values(%s, %s, %s, %s, %s); ''',
                    tuplaInfo
                    )
        conn.commit()
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def deleteConsult(conn, idConsult):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        cur.execute("delete from consulta where id = '" +idConsult+"'")
        conn.commit()
        status['message'] = 'Bien hecho'
        status['error'] = 202
        return status
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 400
        status['message'] = e.diag.message_primary

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status
