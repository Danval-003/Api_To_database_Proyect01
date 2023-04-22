# Api_To_database_Proyect02
**_Version 6.0  Definitive Edition Api_**

URL de origen http://52.14.44.33/api/

/login  #Mandas un post con los parametros-_[dpi, clave]_

/singin #Mandas un post con los parametros-_[dpi, nombre, clave, codigo_acceso]_ y te da un mensaje de exito al sing in

/singin #Mandas un get y te devuelve todos los usuarios y su informacion


##RUTAS A LAS QUE PODES ACCEDER SOLO DESPUES DEL LOGIN##

/confirmar _#Solo sirve para confirmar que iniciaste sesion y te devuelve la informacion del usuario actual haciendo un metodo GET_

/logout _#Sirve para deslogear al usuario y cerrar sesión mediante un metodo POST sin usar parametros_

/access_code #Usa un metodo POST con el parametro -_[role]_ y te devuelve un json con un access_code con un codigo para la creacion de otro usuario. Solo es posible usarlo cuando el usuario con el que se hizo log in es un Administrador
