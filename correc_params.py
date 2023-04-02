"""
Universidad del Valle de Guatemala
Proyecto 2
Bases de Datos I
Seccion 20
Daniel Armando Valdez Reyes|21240
Diego Alexander Hernandez Silvestre|21270
Kristopher Javier Alvarado Lopez|21188

Descripcion:
Modulo creado para manipular los parametros para adaptarse a las busquedas
"""


# Coloca el nombre en el formato en que esta escrito en postgres con mayusculas en las primeras letras de cada parte
# del nombre
def first_mayus(name):
    # Coloca todo el nombre en minusculas
    name.lower()
    # Se separan los apellidos y nombres
    sep_ = name.split(' ')
    name_with_mayus = ''
    # Se le colocan los nombres con la primera mayuscula
    for name in sep_:
        name_with_mayus = name_with_mayus + name.capitalize() + ' '
    # Se devuelve todo con las mayusculas pero se quita un espacio (" ") que sobró
    return name_with_mayus[:-1]
