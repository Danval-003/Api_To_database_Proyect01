# Api_To_database_Proyect01
**_Version 2.2: Moduled Version_**

URL de origen http://52.14.44.33/api/

/login  #Mandas un post con los parametros-[dpi, clave]

/singin #Mandas un post con los parametros-[dpi, nombre, clave, codigo_acceso] y te da un mensaje de exito al sing in

/singin #Mandas un get y te devuelve todos los usuarios y su informacion


##RUTAS A LAS QUE PODES ACCEDER SOLO DESPUES DEL LOGIN##

/confirmar #Solo sirve para confirmar que iniciaste sesion y te devuelve la informacion del usuario actual haciendo un metodo GET

/logout #Sirve para deslogear al usuario y cerrar sesión mediante un metodo POST sin usar parametros

/access_code #Usa un metodo POST con el parametro -[rol] y te devuelve un json con un access_code con un codigo para la creacion de otro usuario. Solo es posible usarlo cuando el usuario con el que se hizo log in es un Administrador
