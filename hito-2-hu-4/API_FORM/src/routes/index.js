const express = require('express');
const router = new express.Router();

const FormController = require('../controllers/FormController')


//==========================endpoints(Routes)============================//

// Rutas para el CRUD del Form
router.get('/createTableForm', FormController.createTableForm);
router.post('/formularios', FormController.createForm);
router.get('/formularios', FormController.getForms);
router.get('/formularios/:id', FormController.getFormById);
router.put('/formularios/:id', FormController.updateForm);
router.delete('/formularios/:id', FormController.deleteForm);

module.exports = router;