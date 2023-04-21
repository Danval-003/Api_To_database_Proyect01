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
        "availableQuantity": row[3],
        "unitId": row[4],
        'productId': row[5]
    } for row in rows]
    return status


def material_expired(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    try:
        cur.execute("select * from vencimientos()")
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
        "availableQuantity": row[3],
        "expiredDate": row[4],
        "unitID":row[5],
        "productId": row[6]
    } for row in rows]
    return status


def requestedProduct(conn, tupla):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        cur.execute(''' select * from requested_product(%s, %s, %s, %s) ''',
                    tupla
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


def requestedProductExpired(conn, tupla):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }

    cur = conn.cursor()

    try:
        cur.execute(''' select * from requested_product_expired(%s, %s, %s, %s, %s) ''',
                    tupla
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


