import psycopg2


def obtain_bitacora(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute('select dpi, usuario, tipo_cambio, tabla_modificada, fecha_hora from bitacora order by fecha_hora desc')
    rows = cur.fetchall()
    if len(rows) != 0:
        status['data'] = [{
            'dpi': row[0],
            'usuario': row[1],
            'cambio': row[2],
            'tabla': row[3],
            'fechaHora': row[4]
        } for row in rows]
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status


def editDoctorUnit(conn, tupleInformation):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        print(''' 
                select * from change_doctor_unit(%s, %s)''',
              tupleInformation)
        cur.execute(''' 
                 select * from change_doctor_unit(%s, %s)''',
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