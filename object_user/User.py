import psycopg2
from flask_login import UserMixin
from to_complement.cryptografic import desencrypth
from extensions.conection import connect


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
        user_info = dict_role[desencrypth(self.user_id)['role']]
        conn = connect(user_info[0], user_info[1])
        return conn

    def important_data(self):
        return desencrypth(self.user_id)
