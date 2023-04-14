from extensions.conection import connect


def get_role(dpi, clave):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT rol from usuarios_app where dpi = '"+dpi+"' and clave ='" + clave+"'")
    row = cur.fetchall()
    print(row)
    return row[0][0]


def get_name(dpi, clave):
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT nombre from usuarios_app where dpi = %s and clave = %s', (dpi, clave))
    row = cur.fetchall()
    return row[0][0]
