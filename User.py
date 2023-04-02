import psycopg2
from flask_login import UserMixin
from cryptografic import desencrypth


# Funcion que realiza la coneccion a la base de datos
def connect(user_id, pas):
    # Se le manda la informacion para realizar la coneccion
    conn = psycopg2.connect(
        host="uvg-bd-p2v2.czfikro2hw8h.us-east-2.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="postgres123"
    )
    return conn


dict_role = {
    'Admin': ['admin', 'El mejor jefe del mundo'],
    'Medico': ['medico', 'Hello Medicina'],
    'Inventario': ['inventario', 'Organizar es mi vida']
}


class User(UserMixin):

    def __init__(self, id_user):
        self.user_id = id_user
        self.active = False

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.user_id

    def get_rol(self):
        return desencrypth(self.user_id)['role']

    def get_my_user_conection(self):
        return dict_role[desencrypth(self.user_id)['role']]

    def important_data(self):
        return desencrypth(self.user_id)
