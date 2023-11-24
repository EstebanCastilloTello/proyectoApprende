import streamlit as st
import pandas as pd
from main import get_profesores, guardar_taller, get_insumos_lider, get_insumos_mercadolibre

def mostrar_profesor(profesor, input, i):
    """Muestra la información de un profesor en Streamlit."""
    if "nombre" in profesor and "enlace_perfil" in profesor :
        guardar_taller(str({profesor['nombre']})[2:-2], str(input), str({profesor['enlace_perfil']})[2:-2], str({profesor['tarifa']})[2:-2])
        st.success(f"**Nombre:** {profesor['nombre']}", icon="🦸")
        st.info(f"**Enlace de Perfil y Contacto:** [Visitar]({profesor['enlace_perfil']})", icon="🔗")
        st.success(f"**Tarifa:** {profesor['tarifa']}", icon="💸")
        # Crear un botón que llame a la función sin recargar la página completa
        if st.checkbox(f"Guardar Tallerista {i+1}"):
            st.write("SIUUUUUUUUUUUUUUU")
            #guardar_taller(str({profesor['nombre']})[2:-2], str(input), str({profesor['enlace_perfil']})[2:-2], str({profesor['tarifa']})[2:-2])
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
        with st.form("my_form"):
            # Barra de entrada de texto
            user_input = st.text_area("Ingresa tu Descripción:", height=100, key="user_input")

            # Botón integrado en la barra de búsqueda y para realizar la llamada a la API
            submit_button = st.form_submit_button("Obtener Listado")
            
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
        st.title("Historial de Busqueda")
        # Ruta al archivo Excel en tu carpeta
        ruta_excel = "DB.xlsx"

        # Cargar el archivo Excel en un DataFrame de Pandas
        df = pd.read_excel(ruta_excel)

        # Renombrar las columnas según tus preferencias
        nombres_columnas = {
            'Unnamed: 1': 'Nombre',
            'Unnamed: 2': 'Tarifa',
            'Unnamed: 3': 'Descripcion',
            'Unnamed: 4': 'Link',
            'Unnamed: 5': 'Fecha',
            # Agrega más columnas según sea necesario
        }

        # Renombrar las columnas del DataFrame
        df.rename(columns=nombres_columnas, inplace=True)
        
        # Seleccionar las columnas que deseas mostrar (en este caso, todas excepto 'Link')
        columnas_mostradas = ['Nombre', 'Tarifa', 'Descripcion','Link', 'Fecha']

        # Crear un nuevo DataFrame con solo las columnas seleccionadas
        df_mostrado = df[columnas_mostradas]

        # Mostrar el DataFrame en Streamlit
        st.table(df_mostrado)

if __name__ == "__main__":
    main()
