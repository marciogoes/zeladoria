const express = require('express');
const router = express.Router();
const { auth, checkRole } = require('../middlewares/auth.middleware');
const { getDashboard } = require('../controllers/relatorioController');

// Todas as rotas requerem autenticação e ser gestor/admin
router.use(auth, checkRole('gestor', 'admin'));

router.get('/dashboard', getDashboard);

module.exports = router;
