import psycopg2


# Funcion que realiza la coneccion a la base de datos
def connect(user='postgres', password='postgres123'):
    # Se le manda la informacion para realizar la coneccion
    conn = psycopg2.connect(
        host="uvg-bd-p2v2.czfikro2hw8h.us-east-2.rds.amazonaws.com",
        database="postgres",
        user=user,
        password=password
    )
    return conn
