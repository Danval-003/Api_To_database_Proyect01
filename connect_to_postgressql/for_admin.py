import psycopg2
from connect_to_postgressql.for_patients import instant


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


def obtain_DoctorUnit(conn, doctorDpi):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute("""select us.nombre, fecha_inicio 
                    from medico
                    inner join unidad_salud us on id_unidad_salud = us.id
                                     where dpi = '"""
                +doctorDpi+"'")
    r = cur.fetchall()
    status['actualUnit'] = r[0][0]
    status['dateStart'] = r[0][1]

    cur.execute("""select us.nombre, fecha_inicio, fecha_final 
                        from unidad_salud_medico_historial
                        inner join unidad_salud us on us.id = unidad_salud_medico_historial.id_unidad_salud
                                                  where id_medico ='"""+doctorDpi+"'")

    rows = cur.fetchall()

    if len(rows) != 0:
        status['data'] = [{
            'idUnit': row[0],
            'startDate': row[1],
            'finalDate': row[2]
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


def obtain_UserInfo(conn, dpiUser):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute("""select dpi, nombre, clave, rol from usuarios_app where dpi ='"""+str(dpiUser)+"'")

    rows = cur.fetchall()

    if len(rows) != 0:
        status['data'] = [{
            'dpiUser': row[0],
            'nameUser': row[1],
            'clave': row[2],
            'rol': row[2]
        } for row in rows]
        return status

    status['message'] = 'No se encontraron las consultas del expediente'
    status['error'] = 404
    return status
