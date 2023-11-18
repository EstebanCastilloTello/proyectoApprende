import streamlit as st
from main import get_profesores

def mostrar_profesor(profesor):
    """Muestra la información de un profesor en Streamlit."""
    if "nombre" in profesor and "enlace_perfil" in profesor:
        st.success(f"**Nombre:** {profesor['nombre']}",icon="🦸")
        st.info(f"**Enlace de Perfil y Contacto:** [Link]({profesor['enlace_perfil']})",icon="🔗")
        st.write("----------------------------------------------------------------")

def mostrar_respuesta_api(respuesta):
    """Muestra la respuesta de la API en Streamlit."""
    if "profesores" in respuesta:
        st.title("Lista de Talleristas")
        st.write("----------------------------------------------------------------")
        for profesor in respuesta["profesores"]:
            mostrar_profesor(profesor)

def main():
    """Función principal de la aplicación Streamlit."""
    # Inicializar la variable de estado enter_pressed
    if "enter_pressed" not in st.session_state:
        st.session_state.enter_pressed = False

    # Título de la aplicación
    st.image("https://blogger.googleusercontent.com/img/a/AVvXsEgI6f40yapqlQkv6dQ1Mv8PXgRA1xiyiaage_HPZqvywAJeVdik_ZaBlZtYgAfkqxEdUPYXGaw57hvTrYEAKZlXKESC2b5-QBVYrlqB4A-foKkBsYKD-fuU00T6AXdwcTRct5tPSdZw4a_VpEXCuPHYZ-vlF0OwJeqOFx5bLk9Fj6qzC_fe_G6e63WadBU", use_column_width=True)
    st.title("Barra de Búsqueda de Tallerista")

    # Configurar formulario para que funcione con la tecla "Enter"
    with st.form("my_form"):
        # Barra de entrada de texto
        user_input = st.text_input("Ingresa tu Descripción:")

        # Botón integrado en la barra de búsqueda y para realizar la llamada a la API
        submit_button = st.form_submit_button("Obtener Listado")

        # Lógica para realizar la llamada a la API al hacer clic o presionar "Enter"
        if submit_button or st.session_state.enter_pressed:
            respuesta = get_profesores(user_input)
            mostrar_respuesta_api(respuesta)

if __name__ == "__main__":
    main()
