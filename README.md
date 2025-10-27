# Pokedex
Proyecto Modulo 4 UCAMP
En este repositorio encontraran una Pokedex construida para el modulo 4 del bootcamp en UCAMP 
Anexo encontraran el código de python, asi como una carpeta con un .json de los pokemones guradados
Me gustaría empezar explicando las librerarias necesarias para usar el código "requests" para realizar las peticiones http al API
"json" para manejar los datos que guardemos y "os" para poder crear directorios en el nuestro sistema operativo.
La funcionalidad del código es la siguiente:
Lo que hacemos es consumir un API para consultar datos en este caso algun nombre de un pokemon si el nombre del pokemon no existe manejamos los códigos de estado http not found para mostrarle al usuario que ese pokemon no existe
Si el nombre del pokemon existe procedemos a mostar los datos "Estadisticas,Tipos,Habilidades,Movimientos Principales,Imagen" y la guardaremos dentro de un archivo .json en una carpeta llamada pokedex.
Durante esta practica se usaron los conocimientos previamente adquiridos como crear variables, guardar datos en ellas, imprimir valores y solicitar datos al usuario.
La parte interesante fue la de usar la libreria "request" para hacer solicitudes a una API y el manejo de los estados de http como el 200 y el 404, ademas de usar la libreria os para ejecutar comandos en nuestro sistema operativo como crear carpetas.
