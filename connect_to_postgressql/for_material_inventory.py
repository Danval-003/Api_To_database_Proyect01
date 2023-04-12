def material_inventory(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM materiales_escazos()")
