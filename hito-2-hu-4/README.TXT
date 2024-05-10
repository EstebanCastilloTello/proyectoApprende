Hito2-hu-4
Para levantar la api utilizamos docker. Comenzamos levantando la base de datos mediante el siguiente comando. 
docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=password -d mysql 
Esperamos a que se inicie completamente, una vez que se crea la imagen corremos el siguiente comando: 
docker exec -it mysql mysql -uroot -p
En donde la password es password
Luego creamos la base de datos, en este caso llamada BD_FORM
create database BD_FORM;
Luego dentro del directorio api_form, corremos lo siguiente: 
docker-compose up --build -d
Y aqui ya estaria levantada la api. Una vez aqui ingresamos a: 
localhost:8081/createTableForm
y luego a 
localhost:8081/
Una vez aqui, completamos todos los campos y finalmente estos se almacenan en la base de datos.
Cabe destacar que falta manejar el error de los campos obligatorios.
Hito3-hu-5
Revisando el hito 2 nos dimos cuenta que en la carpeta de API_FORM faltaba un archivo .env el cual debe llevar lo siguiente:
PORT_API = 8081
DB_USER = "root"
DB_PASSWORD = "password"
DB_NAME = "BD_FORM"
DB_PORT = 3306
DB_HOST = "host.docker.internal"
De esta manera funcionaria correctamente el codigo. 
Luego en base a la historia de usuario "5" hicimos que se mostraran todos los formularios ingresados a la base de datos
y podamos editarlos haciendo click en un boton mediante el cual hace que salga una ventana emergente en donde se deben reingresar los datos 
y modificar el que se busca.
Adicionalmente anadimos un boton eliminar el cual elimina directamente de la base de datos el formulario.
Cabe destacar que comenzamos realizando esto como un datatable, pero al momento de agregar los botones no pudimos hacer que volvieran las funciones
de estas. 