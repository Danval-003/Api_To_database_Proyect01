from flask_login import login_required, current_user
from extensions.unauthorized import unauthorized
from flask import jsonify


@login_required
def comprobation_inventory(respon):
    rol = current_user.get_rol()
    if rol == 'Admin' or rol == 'Inventario':
        response = jsonify({'message': respon['message'], 'data': respon['data']})
        response.status_code = respon['error']

    else:
        response = unauthorized()

    return response


@login_required
def comprobation_medic(funtion_medicine):
    def comprobation():
        rol = current_user.get_rol()
        if rol == 'Admin' or rol == 'Medico':
            funtion_medicine()
        else:
            unauthorized()

    return comprobation


@login_required
def comprobation_admin(funtion_admin):
    def comprobation():
        rol = current_user.get_rol()
        if rol == 'Admin':
            funtion_admin()
        else:
            unauthorized()

    return comprobation
