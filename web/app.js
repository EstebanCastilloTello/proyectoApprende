const inputTemaMateria = document.getElementById('inputTemaMateria');
const buscarButton = document.getElementById('buscarButton');
const resultadoElement = document.getElementById('resultado');
const cargandoMensaje = document.getElementById('cargandoMensaje');


buscarButton.addEventListener('click', function() {
    console.log('Botón clicked'); 

    // Limpia el contenido anterior antes de mostrar nuevos resultados
    resultadoElement.innerHTML = '';
    
    // Mostrar el mensaje de carga
    cargandoMensaje.style.display = 'block';

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

                    //para mostrar el tema del taller, las palabras clave
                    if(profesor.tema_taller){
                        const temaTallerElement = document.createElement('p');
                        temaTallerElement.textContent = `Palabras clave: Tema del taller: ${profesor.tema_taller}`;
                        resultadoElement.appendChild(temaTallerElement);
                    }
                }
                


            }
        })
        .catch(error => {
            resultadoElement.textContent = 'Hubo un error al consumir la API: ' + error.message;
        })
        .finally(() => {
            // Ocultar el mensaje de carga una vez que la solicitud se complete (ya sea con éxito o con error)
            cargandoMensaje.style.display = 'none';
        });
});

