from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración de Selenium Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

#datos de la cuenta bot
username = "saimonlaplace@gmail.com"  # Reemplaza con tu correo electrónico
password = "perroLaplace456"         # Reemplaza con tu contraseña



##link para aumentar cantidad buscada en superprof
#https://www.superprof.cl/s/python,Chile,,,1.html?n=2
#aumentar el ultimo valor para buscar mas profesores

'''


temaMateria = input("Ingresar tema: ")

url_superProf = 'https://www.superprof.cl/s/'+ temaMateria +',Chile,,,1.html'
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
    profesores.append((nombre, link))

# Imprime los nombres de los profesores y los enlaces a sus perfiles
for nombre, link in profesores:
    print(f"Nombre del profesor: {nombre}")
    print(f"Enlace a perfil del profesor: {link}")
    print()
'''





"""

###Linkedin
# Página de inicio de sesión de LinkedIn
linkedin_url = "https://www.linkedin.com/login"

# Abre LinkedIn en el navegador
driver.get(linkedin_url)

# Localizadores
username_locator = (By.NAME, "session_key")
password_locator = (By.NAME, "session_password")

# Encuentra los elementos y envía las credenciales
username_field = driver.find_element(*username_locator)
password_field = driver.find_element(*password_locator)

username_field.send_keys(username)
password_field.send_keys(password)

#apretar boton inciar sesion
# Encuentra el botón de inicio de sesión por su atributo "aria-label"
login_button = driver.find_element(By.XPATH, "//button[@aria-label='Iniciar sesión']")

# Haz clic en el botón de inicio de sesión
login_button.click()


# Espera a que se cargue la página (puedes ajustar este tiempo según sea necesario)
driver.implicitly_wait(20)

# Encuentra el primer elemento de nompreperfil y rol
nompreMiPerfil = driver.find_element(By.CLASS_NAME, "t-16.t-black.t-bold")
rolMiPerfil = driver.find_element(By.CLASS_NAME, "identity-headline")
# Imprime el texto del elemento
print("Primer resultado:")
print(nompreMiPerfil.text)
print(rolMiPerfil.text)


"""



### INSTAGRAM

# Página de inicio de sesión de Instagram
instagram_url = "https://www.instagram.com/accounts/login/"

# Abre Instagram en el navegador
driver.get(instagram_url)
driver.implicitly_wait(10)
# Localizadores
username_locator = (By.NAME, "username")
password_locator = (By.NAME, "password")

# Encuentra los elementos y envía las credenciales
username_field = driver.find_element(*username_locator)
password_field = driver.find_element(*password_locator)

username_field.send_keys(username)
password_field.send_keys(password)
driver.implicitly_wait(10)

# Apretar botón "Iniciar sesión"
buttons = driver.find_elements(By.CLASS_NAME, '_acan')

# Verifica si hay al menos dos botones con esa clase
if len(buttons) >= 2:
    # Accede al segundo botón y obtén su texto
    second_button = buttons[1]
    print(second_button.text)
    second_button.click()
    

# Espera a que se cargue la página de inicio de tu cuenta (puedes ajustar este tiempo según sea necesario)
WebDriverWait(driver, 10).until(EC.url_contains('tu_pagina_de_inicio'))    

# Espera a que se cargue la página de inicio de tu cuenta (puedes ajustar este tiempo según sea necesario)





# Cierra el navegador al final
driver.quit()


#buscar elemento por tag
#elements = driver.find_elements(By.TAG_NAME, 'h1')
#Para el primer elemento
#print(elements[0].text)

#elements es una lista
#for e in elements:
#    print(e.text)
