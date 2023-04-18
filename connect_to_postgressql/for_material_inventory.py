import psycopg2


def material_inventory(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM materiales_escazos()")
    except psycopg2.IntegrityError as e:
        # En caso el query falle se obtiene de vuelta el error
        status['error'] = 500
        status['message'] = e.diag.message_primary
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron materiales escazos'
        status['error'] = 404
        return status

    status['data'] = [{
        "healthUnit": row[0],
        "product": row[1],
        "totalQuantity": row[2],
        "availableQuantity": row[3]
    } for row in rows]
    return status
