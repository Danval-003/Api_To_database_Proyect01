from flask_login import UserMixin
from to_complement.cryptografic import desencrypth
from connect_to_postgressql.for_user import *

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
        dpi_0 = desencrypth(self.user_id)['dpi']
        clave_0 = desencrypth(self.user_id)['password']
        return get_role(dpi_0, clave_0)

    def get_name_u(self):
        dpi_0 = desencrypth(self.user_id)['dpi']
        clave_0 = desencrypth(self.user_id)['password']
        return get_name(dpi_0, clave_0)

    def get_my_user_conection(self):
        user_info = dict_role[self.get_rol()]
        conn = connect(user_info[0], user_info[1])
        name_0 = self.get_name_u()
        conn.cursor().execute("""
        set my.app_user = '"""+name_0+"""';
        select current_setting('my.app_user');
        """)
        return conn

    def important_data(self):
        data = desencrypth(self.user_id)
        data.update(
            {'role': self.get_rol(),
             'name': self.get_name_u()
             }
        )

        return data
