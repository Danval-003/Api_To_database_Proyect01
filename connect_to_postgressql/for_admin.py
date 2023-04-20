
def obtain_bitacora(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute('select dpi, usuario, tipo_cambio, tabla_modificada, fecha_hora from bitacora')
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