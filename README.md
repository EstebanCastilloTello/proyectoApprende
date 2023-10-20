# proyectoApprende
Este es un repositorio donde se van a ir almacenando los avances del proyecto.


ejecutar api con
uvicorn main:app --reload

Si el código esta dentro de la carpeta API
uvicorn API.main:app --reload

ejecutar web
python -m http.server 8080 --directory web        

endpoints de la API:
http://localhost:8000/profesores/{tema}