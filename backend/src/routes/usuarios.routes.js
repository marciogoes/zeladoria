const express = require('express');
const router = express.Router();
const { auth, checkRole } = require('../middlewares/auth.middleware');
const {
    getUsuarios,
    getUsuario
} = require('../controllers/usuarioController');

// Todas as rotas requerem autenticação
router.use(auth);

// Apenas gestor/admin pode listar usuários
router.get('/', checkRole('gestor', 'admin'), getUsuarios);
router.get('/:id', getUsuario);

module.exports = router;
