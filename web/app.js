const inputTemaMateria = document.getElementById('inputTemaMateria');
const resultadoElement = document.getElementById('resultado');

inputTemaMateria.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Evita que el formulario se envíe si está dentro de un formulario

        const temaMateria = inputTemaMateria.value;
        const apiUrl = `http://localhost:8000/profesores/${temaMateria}`;

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('La solicitud de la API no fue exitosa');
                }
                return response.json();
            })
            .then(data => {
                // Limpia el contenido anterior antes de mostrar nuevos resultados
                resultadoElement.innerHTML = '';

                const profesores = data.profesores;

                if (profesores.length === 0) {
                    resultadoElement.textContent = 'No se encontraron profesores para el tema/materia ingresado.';
                } else {
                    // Procesa y muestra los resultados
                    for (const profesor of profesores) {
                        const profesorElement = document.createElement('p');
                        profesorElement.textContent = `Nombre del profesor: ${profesor.nombre}`;
                        const enlaceElement = document.createElement('a');
                        enlaceElement.href = profesor.enlace_perfil;
                        enlaceElement.textContent = 'Ver perfil';
                        profesorElement.appendChild(enlaceElement);
                        resultadoElement.appendChild(profesorElement);
                    }
                }
            })
            .catch(error => {
                resultadoElement.textContent = 'Hubo un error al consumir la API: ' + error.message;
            });
    }
});
