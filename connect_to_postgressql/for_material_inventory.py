def material_inventory(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute("SELECT * FROM materiales_escazos()")
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron materiales escazos'
        return status

    