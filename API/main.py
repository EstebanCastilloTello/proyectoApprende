from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#api
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import csv
from fastapi.responses import JSONResponse
from pydantic import BaseModel

#openai
import openai

#dotenv
import os
from dotenv import load_dotenv
import datetime
import openpyxl
from openpyxl import Workbook, load_workbook

#cargar dotenv y apikey
load_dotenv()
api_key = os.getenv("API_KEY_OPENAI")
# Establecer la clave de la API de OpenAI
openai.api_key = api_key



# Configuración de Selenium Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#opcion para establecer en segundo plano chrome
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

#funcion para buscar tarifa
def buscar_tarifa(linkPerfilProfesor):
    
    driver.get(linkPerfilProfesor)
    
    # Espera hasta que se carguen los elementos con la clase "value"
    wait = WebDriverWait(driver, 10)
    tarifa = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'value')))

    return tarifa[0].text


#funcion para encontrar palabra clave en descripcion usando openai
def encontrar_palabra_clave_descripcion(descripcion):
    prompt = "reconoce como palabra clave el tema principal del taller de la siguiente descripción:" + descripcion

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=20,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    #para ver la palabra clave:
    print(response.choices[0].text)
    
    return response.choices[0].text

##funcion de los profes
def buscar_profesores(temaMateria):

    url_superProf = 'https://www.superprof.cl/s/' + temaMateria + ',Chile,,,1.html'

    # Pagina a buscar
    driver.get(url_superProf)

    # Espera hasta que se carguen los elementos con la clase "landing-v4-ads-pic-firstname"
    wait = WebDriverWait(driver, 10)
    nombreProfesor = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'landing-v4-ads-pic-firstname')))
    linkPerfilProfesor = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'landing-v4-ads-bloc.tck-announce-link')))

    #crear una lista de diccionarios para guardar los profesores
    profesores = []

    for i in range(len(nombreProfesor)):
        nombre = nombreProfesor[i].text
        link = linkPerfilProfesor[i].get_attribute('href')
        profesores.append({"nombre": nombre, "enlace_perfil": link, "tarifa": ""})

    return profesores


#-------funcion para encontrar insumos en descripcion usando openai----#

def encontrar_insumos_descripcion(descripcion):
    prompt = "de la siguiente descripción de talleres, reconoce productos o materiales que se necesiten para la realización del taller, solamente entrega los posibles productos separado por guiones \"-\", ejemplo: producto1-producto2-producto3, la descripcion es:" + descripcion

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=40,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    # Verificar si la respuesta contiene productos
    productos_encontrados = response.choices[0].text.strip()
    
    if len(productos_encontrados) > 0:
        return productos_encontrados
    else:
        return ""


def buscar_insumos_lider(insumo, cantidad=1, tiempo_espera=5):
    # URL del supermercado
    url_supermercado = "https://www.lider.cl/supermercado/search?query=" + insumo

    # PÃ¡gina a buscar
    driver.get(url_supermercado)
    
    # Espera hasta que se carguen los elementos con la clase "product-card_description-wrapper"
    wait = WebDriverWait(driver, tiempo_espera)
    try:
        descripcionProducto = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card_description-wrapper')))
    except:
        return []
        
    # Obtener nombres de los primeros 'cantidad' productos
    productos = [element.text for element in descripcionProducto[:cantidad]]

    elementos_ais_hits_item = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ais-Hits-item')))
        # Obtener enlaces de los elementos <a> dentro de la clase "ais-Hits-item"
    enlaces = []
    for elemento_ais_hits_item in elementos_ais_hits_item[:cantidad]:
        # Buscar el elemento <a> dentro de cada elemento ais-Hits-item
        enlace = elemento_ais_hits_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        enlaces.append(enlace)
    
    #crear una lista de diccionarios para guardar los productos
    productos_lista = []
    for i in range(len(productos)):
        productos_lista.append({"nombre": productos[i], "link": enlaces[i]})
        
    
    return productos_lista




def buscar_insumos_mercadoLibre(insumo, cantidad=1, tiempo_espera=5):
    # URL del proveedor de insumos
    url_proveedor_insumos = "https://listado.mercadolibre.cl/" + insumo

    # PÃ¡gina a buscar
    driver.get(url_proveedor_insumos)
    
    # Espera hasta que se carguen los elementos con la clase "product-card_description-wrapper"
    wait = WebDriverWait(driver, tiempo_espera)
    
    try:
        descripcionProducto = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-item__title')))    
    except:
        return []
    

    # Obtener nombres de los primeros 'cantidad' productos
    productos = [element.text for element in descripcionProducto[:cantidad]]

    elementos_ais_hits_item = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-item__group')))
    #Obtener enlaces de los elementos <a> dentro de la clase "ui-search-item__group ui-search-item__group--title"
    enlaces = []
    for elemento_ais_hits_item in elementos_ais_hits_item[:cantidad]:
        # Buscar el elemento <a> dentro de cada elemento 
        enlace = elemento_ais_hits_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        enlaces.append(enlace)
    
    #crear una lista de diccionarios para guardar los productos
    productos_lista = []
    for i in range(len(productos)):
        productos_lista.append({"nombre": productos[i], "link": enlaces[i]})
        
    
    return productos_lista





#------------codigo api-----------------

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Configurar los orígenes permitidos (puede ajustarlos según sus necesidades)
origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:8080", "http://127.0.0.1"]

# Habilitar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# endpoit raiz
@app.get("/")
def get_root():
    return {"message": "¡Bienvenido a la API de prueba de FastAPI!"}

if __name__ == "__main__":
    # Cambia el puerto y el host según tus preferencias.
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/profesores/{descripcion_taller}")
def get_profesores(descripcion_taller: str):
    
    #llamar a la funcion de encontrar palabra clave usando openai
    temaTaller = encontrar_palabra_clave_descripcion(descripcion_taller) 
   
    #llamar a la funcion de buscar profesores en superprof
    resultado = buscar_profesores(temaTaller)
    
    #por cada profesor, buscar su tarifa
    for profesor in resultado:
        tarifa = buscar_tarifa(profesor["enlace_perfil"])
        profesor["tarifa"] = tarifa

    #para test, no usa openai, solo llama a superprof
    #resultado = buscar_profesores(descripcion_taller)
    
    resultado.append({"tema_taller": temaTaller})
        
    return {"profesores": resultado}




#endpoint para encontrar insumos en lider
@app.get("/insumosLider/{descripcion_taller}")
def get_insumos_lider(descripcion_taller: str):
    
    #llamar a la funcion de encontrar insumos usando openai
    productosIdentificados = encontrar_insumos_descripcion(descripcion_taller)
    
    if(productosIdentificados == ""):
        return {"insumos": [{"nombre": "No se encontraron productos", "link": "No se encontraron productos"}]}
    
    
    #de la descripcion, separar los productos identificados por guiones y guardarlos en una lista
    productosIdentificados = productosIdentificados.split("-")
    
    #solo si productosIdentificados tiene mas de un producto eliminamos el ultimo elemento
    #por temas de tokes de openai, probablemente el utlimo producto esté incompleto
    if(len(productosIdentificados) > 1):
        productosIdentificados.pop()
        
    #lista para guardar los productos encontrados 
    insumosLider = [] #lista de diccionarios
    
    #por cada producto identificado, buscarlo en proveedor de insumos
    if len(productosIdentificados) > 0:
        #buscar solo 3 productos si es que hay 3 
        if len(productosIdentificados) > 3:
            for i in range(3):
                insumosLider.append(buscar_insumos_lider(productosIdentificados[i]))
        else:
            for i in range(len(productosIdentificados)):
                insumosLider.append(buscar_insumos_lider(productosIdentificados[i]))
        
    
    else:
        insumosLider.append({"nombre": "No se encontraron productos", "link": "No se encontraron productos"})
    
    #desempaquetar lista de listas de diccionarios
    lista_diccionarios_insumos = [insumo for elementoInsumo in insumosLider for insumo in elementoInsumo]
    
    return {"insumos": lista_diccionarios_insumos}



#endpoint para encontrar insumos en mercado libre
@app.get("/insumosMercadoLibre/{descripcion_taller}")
def get_insumos_mercadolibre(descripcion_taller: str):
            
    #llamar a la funcion de encontrar insumos usando openai
    productosIdentificados = encontrar_insumos_descripcion(descripcion_taller)
    
    #de la descripcion, separar los productos identificados por guiones y guardarlos en una lista
    productosIdentificados = productosIdentificados.split("-")
    
    #solo si productosIdentificados tiene mas de un producto eliminamos el ultimo elemento
    #por temas de tokes de openai, probablemente el ultimo producto esté incompleto
    if(len(productosIdentificados) > 1):
        productosIdentificados.pop()
        
    #lista para guardar los productos encontrados 
    insumosMercadoLibre = []
    
    #por cada producto identificado, buscarlo en proveedor de insumos
    if len(productosIdentificados) > 0:
        #buscar solo 3 productos si es que hay 3 
        if len(productosIdentificados) > 3:
            for i in range(3):
                insumosMercadoLibre.append(buscar_insumos_mercadoLibre(productosIdentificados[i]))
        else:
            for i in range(len(productosIdentificados)):
                insumosMercadoLibre.append(buscar_insumos_mercadoLibre(productosIdentificados[i]))
        
    else:
        insumosMercadoLibre.append({"nombre": "No se encontraron productos", "link": "No se encontraron productos"})
    
    #desempaquetar lista de listas de diccionarios
    lista_diccionarios_insumos = [insumo for elementoInsumo in insumosMercadoLibre for insumo in elementoInsumo]
            
    return {"insumos": lista_diccionarios_insumos}
            
            

#-----------------------------------------------------

#clase para guardar datos en la base de datos para usar en el endpoint de guardar taller POST
class TallerData(BaseModel):
    tallerista: str
    descripcion: str
    link: str
    tarifa: str

# endpoint para añadir datos a la base de datos
@app.post("/guardarTaller")
def guardar_taller(taller_data: TallerData):
    # fecha actual
    hoy = datetime.datetime.now()
    fecha_hoy = hoy.strftime("%y-%m-%d/%H:%M:%S")

    # si no existe el archivo, crearlo
    if not os.path.isfile('DB.csv'):
        with open('DB.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nombre_tallerista', 'tarifa', 'descripcion', 'link', 'fecha'])

    # abrir el archivo CSV
    with open('DB.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        # Contador para manejar las id
        if taller_data.tallerista is not None:
            try:
                with open('DB.csv', 'r') as file:
                    lector_csv = csv.reader(file)

                    # Leer las filas del archivo CSV
                    filas = list(lector_csv)
                    
                    if len(filas) == 1:
                        # solo está el header
                        # iniciar id en 0
                        next_id = 0
                    else:
                        # Acceder al valor del ID del último elemento y sumar 1 a next_id
                        ultimo_id = int(filas[-1][0])
                        next_id = ultimo_id + 1

                writer.writerow([next_id, taller_data.tallerista, taller_data.tarifa, taller_data.descripcion, taller_data.link, fecha_hoy])

                print(next_id, taller_data.tallerista)

                return JSONResponse(content={"message": "Datos guardados en CSV"}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"message": f"Error: {e}"}, status_code=500)
        else:
            return JSONResponse(content={"message": "Error en los parámetros"}, status_code=400)
#-----------------------------------------------------

#endpoint para obtener datos de la base de datos
@app.get("/historialGuardados")
def get_historial_guardados():
    # si no existe el archivo, crearlo
    if not os.path.isfile('DB.csv'):
        with open('DB.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nombre_tallerista', 'tarifa', 'descripcion', 'link', 'fecha'])

    # abrir el archivo CSV
    with open('DB.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        # Leer las filas del archivo CSV
        filas = list(reader)
        # Eliminar el header
        filas.pop(0)
        # Crear una lista de diccionarios para guardar los talleres
        talleres = []
        # Por cada fila en el archivo CSV
        for fila in filas:
            # Crear un diccionario para guardar los datos del taller
            taller = {
                'id': fila[0],
                'nombre_tallerista': fila[1],
                'tarifa': fila[2],
                'descripcion': fila[3],
                'link': fila[4],
                'fecha': fila[5]
            }
            # Agregar el diccionario a la lista de talleres
            talleres.append(taller)

        return JSONResponse(content={"talleres": talleres}, status_code=200)


# Cerrar el controlador de Selenium, dejarlo comentado para que no se cierre mientras se ejecuta la API
#driver.quit()
