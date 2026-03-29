const express = require('express');
const router = express.Router();
const { auth, checkRole } = require('../middlewares/auth.middleware');
const {
    getCategorias,
    createCategoria
} = require('../controllers/categoriaController');

// Listar é público
router.get('/', getCategorias);

// Criar requer autenticação e ser gestor/admin
router.post('/', auth, checkRole('gestor', 'admin'), createCategoria);

module.exports = router;
