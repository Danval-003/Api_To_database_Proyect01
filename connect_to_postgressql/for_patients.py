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
    cur.execute("select * from paciente where dpi = " + str(id_patient))
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontro el paciente'
        status['error'] = 404
        return status

    status['data'] = [{
        'id': row[0],
        'name_patient': row[1],
        'address': row[2],
        'birthdate': row[3],
        'genre': row[4],
        'corporal_mass': row[5],
        'height': row[6],
        'weight': row[7],
        'addiction': row[8],
        'hereditary_disease': row[9],
        'start_date': row[10],
        'status': row[11]
    } for row in rows]
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
                    inner join medico m on m.id = consulta.id_medico
                    inner join unidad_salud us on us.id = consulta.id_unidad_salud
                where consulta.id_paciente =''' + str(id_patient))
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
            select  i.descripcion, it.cantidad, it.fecha_final, it.fecha_inicio, it.dosis
                from insumos_tratamientos it
                inner join insumos i on i.id = it.id_insumo
            where it.id_consulta = ''' + str(id_consult))
    rows = cur.fetchall()
    if len(rows) != 0:
        status['data'] = [{
            'inputDescription': row[0],
            'count': row[1],
            'finalDate': row[2],
            'startDate': row[3],
            'dose': row[4],
        } for row in rows]
        return status

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
                    (id_patient, id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion, id_consult)
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


def createConsult(conn, id_patient, id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        cur.execute(''' 
                insert into consulta(id_paciente, id_medico, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion) 
                values(%s, %s, %s, %s, %s, %s, %s, %s); ''',
                    (id_patient, id_doctor, id_enfermedad, id_unidad_salud, fecha, descripcion, evolucion)
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
