const express = require('express');
const morgan = require('morgan');
const path = require('path');
const app = express();
require('dotenv').config();

// Middleware para logs y manejo de JSON
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: true })); 
app.use(express.json());

const database = require('./src/db'); 

database.connect((err) => {
    if (err) {
        console.error('Error al conectar a la base de datos:', err);
        return;
    }
    console.log('Conexión exitosa a la base de datos MySQL');
});


app.use(express.static(path.join(__dirname, 'public')));



app.get('/formOnline', (req, res) => {
    console.log('Ingresando a registro de formularios');
    res.sendFile(path.join(__dirname, 'public', 'formOnline.html'));
});

app.get('/form', (req, res) => {
    console.log('Accediendo a ingreso de formularios');
    res.sendFile(path.join(__dirname, 'public', 'form.html'));
});

app.get('/', (req, res) => {
    console.log('Ingresando a inicio');
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

const routes = require('./src/routes/index');
app.use(routes);


// Iniciar el servidor
const PORT = process.env.PORT_API || 8081;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

