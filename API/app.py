import streamlit as st
from main import get_profesores, guardar_taller, get_insumos_lider, get_insumos_mercadolibre

def mostrar_profesor(profesor, input):
    """Muestra la información de un profesor en Streamlit."""
    if "nombre" in profesor and "enlace_perfil" in profesor:
        guardar_taller(str({profesor['nombre']})[2:-2], str(input), str({profesor['enlace_perfil']})[2:-2])
        st.success(f"**Nombre:** {profesor['nombre']}", icon="🦸")
        st.info(f"**Enlace de Perfil y Contacto:** [Visitar]({profesor['enlace_perfil']})", icon="🔗")
        st.write("----------------------------------------------------------------")

def mostrar_respuesta_api(respuesta, input):
    """Muestra la respuesta de la API en Streamlit."""
    if "profesores" in respuesta:
        st.title("Lista de Talleristas")
        st.write("----------------------------------------------------------------")
        for profesor in respuesta["profesores"]:
            mostrar_profesor(profesor, input)

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
        st.write("Bienvenido a la Página de Inicio.")
        # Configurar formulario para que funcione con la tecla "Enter"
        with st.form("my_form"):
            # Barra de entrada de texto
            user_input = st.text_area("Ingresa tu Descripción:", height=100, key="user_input")

            # Botón integrado en la barra de búsqueda y para realizar la llamada a la API
            submit_button = st.form_submit_button("Obtener Listado")

        # Lógica para realizar la llamada a la API al hacer clic o presionar "Enter"
        if submit_button or st.session_state.enter_pressed:
            # Mostrar información adicional en una sección desplegable
            insumos_result_lider = get_insumos_lider(user_input)
            insumos_result_mercadolibre = get_insumos_mercadolibre(user_input)
            respuesta = get_profesores(user_input)
            mostrar_informacion_adicional(insumos_result_lider, insumos_result_mercadolibre)
            mostrar_respuesta_api(respuesta, user_input)
            
    elif menu_opcion == "Historial de Búsqueda 📝":
        st.write("MUESTRA EL HISTORIAL.")

if __name__ == "__main__":
    main()
