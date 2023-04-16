from flask_login import login_required, current_user


@login_required
def comprobation_inventory():
    rol = current_user.get_rol()
    return rol == 'Admin' or rol == 'Inventario'


@login_required
def comprobation_medic():
    rol = current_user.get_rol()
    return rol == 'Admin' or rol == 'Medico'


@login_required
def comprobation_admin():
    rol = current_user.get_rol()
    return rol == 'Admin'
