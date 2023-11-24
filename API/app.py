import streamlit as st
import pandas as pd
import requests


def get_insumos_lider_usando_api(descripcion):
    # Endpoint para obtener los insumos disponibles en LIDER
    endpoint = f"http://localhost:8000/insumosLider/{descripcion}"

    # Realizar la solicitud GET
    response = requests.get(endpoint)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Imprimir la respuesta JSON
        return response.json()
    else:
        # Devolver un diccionario con el mensaje de error si la solicitud no fue exitosa
        return {"error": f"Error al obtener insumos de LIDER. Código de estado: {response.status_code}"}


def get_insumos_mercadolibre_usando_api(descripcion):
    # Endpoint para obtener los insumos disponibles en MERCADOLIBRE
    endpoint = f"http://localhost:8000/insumosMercadoLibre/{descripcion}"

    # Realizar la solicitud GET
    response = requests.get(endpoint)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Imprimir la respuesta JSON
        return response.json()
    else:
        # Devolver un diccionario con el mensaje de error si la solicitud no fue exitosa
        return {"error": f"Error al obtener insumos de MERCADOLIBRE. Código de estado: {response.status_code}"}



def guardar_taller_usando_api(nombre_tallerista, descripcion, enlace, tarifa):
    # el endpoint es @app.post("/guardarTaller")
    
    endpoint = "http://localhost:8000/guardarTaller"
    
    # Crear un diccionario con los datos que se enviarán en el cuerpo del POST
    data = {
        "tallerista": nombre_tallerista,
        "descripcion": descripcion,
        "link": enlace,
        "tarifa": tarifa
    }

    try:
        # Enviar la solicitud POST con los datos en el cuerpo
        response = requests.post(endpoint, json=data)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            print("Datos guardados exitosamente en la API.")
        else:
            print(f"Error al guardar datos. Código de estado: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error en la solicitud POST: {e}")

    
def get_profesores_usando_api(descripcion):
    #endpoint
    url_endpoint = f"http://localhost:8000/profesores/{descripcion}"
    
    # Realizar la solicitud GET
    response = requests.get(url_endpoint)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Imprimir la respuesta JSON
        return response.json()
    else:
        # Devolver un diccionario con el mensaje de error si la solicitud no fue exitosa
        return {"error": f"Error al obtener profesores. Código de estado: {response.status_code}"}






def mostrar_profesor(profesor, input, i):
    """Muestra la información de un profesor en Streamlit."""
    if "nombre" in profesor and "enlace_perfil" in profesor :
        st.success(f"**Nombre:** {profesor['nombre']}", icon="🦸")
        st.info(f"**Enlace de Perfil y Contacto:** [Visitar]({profesor['enlace_perfil']})", icon="🔗")
        st.success(f"**Tarifa:** {profesor['tarifa']}", icon="💸")
                       
        # Crear un botón que llame a la función sin recargar la página completa
        checkbox_state = st.checkbox(f"Guardar Tallerista {i+1}")
        
        if f'checkbox{i+1}' not in st.session_state:
            st.session_state[f'checkbox{i+1}'] = False
            
        if checkbox_state and st.session_state[f'checkbox{i+1}'] == False:
            st.write("Guardado")
            # Guardar solo al profesor del checkbox correspondiente
            #input es la descripcion
            guardar_taller_usando_api(profesor['nombre'], input, profesor['enlace_perfil'], profesor['tarifa'])
            
            st.session_state[f'checkbox{i+1}'] = True
        
        elif checkbox_state and st.session_state[f'checkbox{i+1}'] == True:
            st.write("Tallerista ya ha sido guardado")
        st.write("----------------------------------------------------------------")





def mostrar_respuesta_api(respuesta, input):
    """Muestra la respuesta de la API en Streamlit."""
    if "profesores" in respuesta:
        st.title("Lista de Talleristas")
        st.write("----------------------------------------------------------------")
        for i, profesor in enumerate(respuesta["profesores"]):
            mostrar_profesor(profesor, input, i)




def mostrar_informacion_adicional(insumos_lider, insumos_mercadolibre):
    """Muestra información adicional en una sección desplegable."""
    with st.expander("**Compra de Insumos**"):
        st.title("Lista de Insumos")
        st.write("----------------------------------------------------------------")
        # Verificar si hay insumos disponibles LIDER
        if "insumos" in insumos_lider and len(insumos_lider["insumos"]) > 0:
            # Mostrar la información en una tabla con formato Markdown
            for insumo in insumos_lider["insumos"]:
                st.success(f"**{insumo['nombre']}**", icon="👾")
                st.info(f"**Enlace de compra:** [Comprar!]({insumo['link']})", icon="🔗")
                st.write("----")
        else:
            st.write("No se encontraron insumos para mostrar.")

        # Verificar si hay insumos disponibles MERCADOLIBRE
        if "insumos" in insumos_mercadolibre and len(insumos_mercadolibre["insumos"]) > 0:
            # Mostrar la información en una tabla con formato Markdown
            for insumo in insumos_mercadolibre["insumos"]:
                st.success(f"**{insumo['nombre']}**", icon="👾")
                st.info(f"**Enlace de compra:** [Comprar!]({insumo['link']})", icon="🔗")
                st.write("----")
        else:
            st.write("No se encontraron insumos para mostrar.")




def main():
    # Agregar un menú de navegación en la barra lateral
    st.sidebar.title("Menú de Navegación")
    menu_opcion = st.sidebar.radio("", ("Barra de Búsqueda 🔍", "Historial de Búsqueda 📝"))

    if menu_opcion == "Barra de Búsqueda 🔍":
        # Inicializar la variable de estado enter_pressed
        if "enter_pressed" not in st.session_state:
            st.session_state.enter_pressed = False

        # Título de la aplicación
        st.image("https://blogger.googleusercontent.com/img/a/AVvXsEgI6f40yapqlQkv6dQ1Mv8PXgRA1xiyiaage_HPZqvywAJeVdik_ZaBlZtYgAfkqxEdUPYXGaw57hvTrYEAKZlXKESC2b5-QBVYrlqB4A-foKkBsYKD-fuU00T6AXdwcTRct5tPSdZw4a_VpEXCuPHYZ-vlF0OwJeqOFx5bLk9Fj6qzC_fe_G6e63WadBU", use_column_width=True)
        st.title("Barra de Búsqueda de Tallerista")
        # Configurar formulario para que funcione con la tecla "Enter"

        # Barra de entrada de texto
        user_input = st.text_area("Ingresa tu Descripción:", height=100, key="user_input")


        if "load_state" not in st.session_state:
            st.session_state.load_state = False

        if 'buttonOnClick' not in st.session_state:
            st.session_state['buttonOnClick'] = False
        
        # Botón integrado en la barra de búsqueda y para realizar la llamada a la API
        submit_button = st.button("Obtener Listado")
        
        
        # Variable para controlar la visibilidad del botón
        #boton_visible = False

        # Botón que será visible o invisible según el valor de la variable
        #if submit_button:
        #    boton_visible = not boton_visible

        # Mostrar el botón solo si la variable es True
        #if boton_visible:
        #    st.button("Este es el botón visible")
        #    st.write("¡Excelente! ¡Funcionó!")
            
                
        # Lógica para realizar la llamada a la API al hacer clic o presionar "Enter"
        if submit_button or st.session_state.load_state:
            #boton_visible = not boton_visible
                        
            st.session_state.load_state = True

            #codigo para que se actualice la pagina al cambiar la descripcion
            #if 'description' in st.session_state:
            #    if st.session_state['description'] != user_input:
            #        st.session_state['buttonOnClick'] = False
            #        if 'insumos_result_lider' in st.session_state:
            #            del st.session_state['insumos_result_lider'] 
            #            
            #        if 'insumos_result_mercadolibre' in st.session_state:
            #            del st.session_state['insumos_result_mercadolibre']
            #        
            #        if 'respuesta_prof' in st.session_state:
            #            del st.session_state['respuesta_prof']
            #            
            #        #establecer la descripcion
            #        del st.session_state['description']
            #
            
            
            if (st.session_state['buttonOnClick'] == False):
                if 'respuesta_prof' not in st.session_state:
                    st.session_state['respuesta_prof'] = get_profesores_usando_api(user_input)
                
                if 'insumos_result_lider' not in st.session_state:
                    st.session_state['insumos_result_lider'] = get_insumos_lider_usando_api(user_input)
                
                if 'insumos_result_mercadolibre' not in st.session_state:
                    st.session_state['insumos_result_mercadolibre'] = get_insumos_mercadolibre_usando_api(user_input)
                
                st.session_state['buttonOnClick'] = True
                
                if "description" not in st.session_state:
                    st.session_state['description'] = user_input
        

            mostrar_informacion_adicional(st.session_state['insumos_result_lider'], st.session_state['insumos_result_mercadolibre'])
            mostrar_respuesta_api(st.session_state['respuesta_prof'], user_input)

            
    elif menu_opcion == "Historial de Búsqueda 📝":
        # Endpoint para obtener datos de la base de datos
        endpoint = "http://localhost:8000/historialGuardados" 

        # Obtener datos desde el endpoint
        response = requests.get(endpoint)
        data = response.json()
        talleres = data["talleres"]

        #establecer el titulo
        st.title("Historial de Búsqueda")
        
        #verificar si hay talleres guardados
        if len(talleres) > 0:
            # Crear un DataFrame de Pandas con los datos
            df = pd.DataFrame(talleres)

            # Renombrar las columnas según tus preferencias
            nombres_columnas = {
                'id': 'ID',
                'nombre_tallerista': 'Nombre del Tallerista',
                'tarifa': 'Tarifa por hora',
                'descripcion': 'Descripción',
                'link': 'Enlace',
                'fecha': 'Fecha',
            }

            # Renombrar las columnas del DataFrame
            df.rename(columns=nombres_columnas, inplace=True)

            # Mostrar el DataFrame en Streamlit con la opción de ordenar
            st.dataframe(df.sort_values(by="Nombre del Tallerista"))
            
        else:
            #si no hay talleres guardados solo escirbir un mensaje
            st.write("No hay talleres guardados")


if __name__ == "__main__":
    main()
