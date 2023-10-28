# proyectoApprende
Este es un repositorio donde se van a ir almacenando los avances del proyecto.



Para ejecutar código:
ejecutar el archivo init.bat con 
\init.bat

api ejecutandose en puerto 8000
pagina en puerto local 8080

O ejecutar individualmente
ejecutar api con
uvicorn main:app --reload

Si el código esta dentro de la carpeta API
uvicorn API.main:app --reload

para ejecutar web
python -m http.server 8080 --directory web        

Endpoints de la API:
http://localhost:8000/profesores/{tema}