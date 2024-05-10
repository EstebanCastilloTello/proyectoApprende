const database = require('../db');

const createTableForm = (req, res) => {
  const query = `
    CREATE TABLE IF NOT EXISTS forms(
      id INT AUTO_INCREMENT PRIMARY KEY,
      nombre VARCHAR(255),
      apellido VARCHAR(255),
      email VARCHAR(255),
      tipo_clase ENUM('Online', 'Presencial'),
      tipo_pago ENUM('Redcompra', 'Paypal', 'Transferencia Bancaria'),
      disponibilidad DATE,
      hora_aproximada TIME,
      costo_clase INT,
      duracion_clase INT
    )
  `;

  database.query(query, (err) => {
    if (err) throw err;
    res.status(200).send('Tabla de formularios creada');
  });
};

const createForm = (req, res) => {
  const { nombre, apellido, email, tipo_clase, tipo_pago, disponibilidad, hora_aproximada, costo_clase, duracion_clase } = req.body;
  const query = 'INSERT INTO forms (nombre, apellido, email, tipo_clase, tipo_pago, disponibilidad, hora_aproximada, costo_clase, duracion_clase) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)';

  database.query(query, [nombre, apellido, email, tipo_clase, tipo_pago, disponibilidad, hora_aproximada, costo_clase, duracion_clase], (err) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al crear el formulario');
    } else {
      res.status(200).send('Formulario creado');
    }
  });
};

const getForms = (req, res) => {
  const query = 'SELECT * FROM forms';

  database.query(query, (err, results) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al obtener los formularios');
    } else {
      res.status(200).json(results);
    }
  });
};

const getFormById = (req, res) => {
  const formId = req.params.id;
  const query = 'SELECT * FROM forms WHERE id = ?';

  database.query(query, [formId], (err, result) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al obtener el formulario por ID');
    } else {
      if (result.length === 0) {
        res.status(404).send('Formulario no encontrado');
      } else {
        res.status(200).json(result[0]);
        
      }
    }
  });
};

const updateForm = (req, res) => {
  const formId = req.params.id;
  const { nombre, apellido, email, tipo_clase, tipo_pago, disponibilidad, hora_aproximada, costo_clase, duracion_clase } = req.body;
  const query = 'UPDATE forms SET nombre = ?, apellido = ?, email = ?, tipo_clase = ?, tipo_pago = ?, disponibilidad = ?, hora_aproximada = ?, costo_clase = ?, duracion_clase = ? WHERE id = ?';

  database.query(query, [nombre, apellido, email, tipo_clase, tipo_pago, disponibilidad, hora_aproximada, costo_clase, duracion_clase, formId], (err, result) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al actualizar el formulario');
    } else {
      if (result.affectedRows === 0) {
        res.status(404).send('Formulario no encontrado');
      } else {
        res.status(200).send('Formulario actualizado');
      }
    }
  });
};

const deleteForm = (req, res) => {
  const formId = req.params.id;
  const query = 'DELETE FROM forms WHERE id = ?';

  database.query(query, [formId], (err) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al eliminar el formulario');
    } else {
      res.status(200).send('Formulario eliminado');
    }
  });
};

module.exports = {
  createTableForm,
  createForm,
  getForms,
  getFormById,
  updateForm,
  deleteForm,
};
