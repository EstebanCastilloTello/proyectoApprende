import streamlit as st
import pandas as pd
from main import get_profesores, guardar_taller, get_insumos_lider, get_insumos_mercadolibre
import requests



def mostrar_profesor(profesor, input, i):
    """Muestra la información de un profesor en Streamlit."""
    if "nombre" in profesor and "enlace_perfil" in profesor :
        st.success(f"**Nombre:** {profesor['nombre']}", icon="🦸")
        st.info(f"**Enlace de Perfil y Contacto:** [Visitar]({profesor['enlace_perfil']})", icon="🔗")
        st.success(f"**Tarifa:** {profesor['tarifa']}", icon="💸")
                 #guardar_taller(str({profesor['nombre']})[2:-2], str(input), str({profesor['enlace_perfil']})[2:-2], str({profesor['tarifa']})[2:-2])
               
        
        # Crear un botón que llame a la función sin recargar la página completa
        checkbox_state = st.checkbox(f"Guardar Tallerista {i+1}")
        
        
        if f'checkbox{i+1}' not in st.session_state:
            st.session_state[f'checkbox{i+1}'] = False
            
        if checkbox_state and st.session_state[f'checkbox{i+1}'] == False:
            st.write("Guardado")
            # Guardar solo al profesor del checkbox correspondiente
            guardar_taller(profesor['nombre'], input, profesor['enlace_perfil'], profesor['tarifa'])
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

        # Botón integrado en la barra de búsqueda y para realizar la llamada a la API
        submit_button = st.button("Obtener Listado")
        
        if "load_state" not in st.session_state:
            st.session_state.load_state = False

        if 'hola' not in st.session_state:
            st.session_state['hola'] = False
        
        # Lógica para realizar la llamada a la API al hacer clic o presionar "Enter"
        if submit_button or st.session_state.load_state:
            st.session_state.load_state = True
            # Mostrar información adicional en una sección desplegable
            #insumos_result_lider = get_insumos_lider(user_input)
            #insumos_result_mercadolibre = get_insumos_mercadolibre(user_input)
    
            if (st.session_state['hola'] == False):
                if 'respuesta' not in st.session_state:
                    st.session_state['respuesta'] = get_profesores(user_input)
                st.session_state['hola'] = True

            #mostrar_informacion_adicional(insumos_result_lider, insumos_result_mercadolibre)
            mostrar_respuesta_api(st.session_state['respuesta'], user_input)
            
            
            
    elif menu_opcion == "Historial de Búsqueda 📝":
        # Endpoint para obtener datos de la base de datos
        endpoint = "http://localhost:8000/historialGuardados" 

        # Obtener datos desde el endpoint
        response = requests.get(endpoint)
        data = response.json()
        talleres = data["talleres"]

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
        st.title("Historial de Búsqueda")
        st.dataframe(df.sort_values(by="Nombre del Tallerista"))
    


if __name__ == "__main__":
    main()
