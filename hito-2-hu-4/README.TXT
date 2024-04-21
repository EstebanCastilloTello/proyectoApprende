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