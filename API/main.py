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
#openai
import openai
#dotenv
import os
from dotenv import load_dotenv

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

    # Página a buscar
    driver.get(url_superProf)

    # Espera hasta que se carguen los elementos con la clase "landing-v4-ads-pic-firstname"
    wait = WebDriverWait(driver, 10)
    nombreProfesor = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'landing-v4-ads-pic-firstname')))
    linkPerfilProfesor = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'landing-v4-ads-bloc.tck-announce-link')))

    # Crea una lista de tuplas (nombreProfesor, linkPerfilProfesor)
    profesores = []

    for i in range(len(nombreProfesor)):
        nombre = nombreProfesor[i].text
        link = linkPerfilProfesor[i].get_attribute('href')
        profesores.append({"nombre": nombre, "enlace_perfil": link})

    

    return profesores




##link para aumentar cantidad buscada en superprof
#https://www.superprof.cl/s/python,Chile,,,1.html?n=2
#aumentar el ultimo valor para buscar mas profesores





#------------codigo api-----------------

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Configurar los orígenes permitidos (puede ajustarlos según sus necesidades)
origins = ["http://localhost", "http://localhost:3000", "http://localhost:8080"]

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

# endpoint de prueba
@app.get("/multiplicar/{numero}")
def multiplicar_numero(numero: int):
    resultado = numero * 2
    return {"resultado": resultado}


@app.get("/profesores/{descripcion_taller}")
def get_profesores(descripcion_taller: str):
    
    #llamar a la funcion de encontrar palabra clave usando openai
    temaTaller = encontrar_palabra_clave_descripcion(descripcion_taller) 
   
    #llamar a la funcion de buscar profesores en superprof
    resultado = buscar_profesores(temaTaller)
    

    #para test, no usa openai, solo llama a superprof
    #resultado = buscar_profesores(descripcion_taller)
    
    resultado.append({"tema_taller": temaTaller})
        
    return {"profesores": resultado}


#-----------------------------------------------------


# Cerrar el controlador de Selenium, eventualmente
#por mientras no cerrarlo
#creo que no se debería cerrar nunca mientras la api este corriendo
#driver.quit()
