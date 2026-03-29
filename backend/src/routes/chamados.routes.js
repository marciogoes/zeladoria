const express = require('express');
const router = express.Router();
const { auth } = require('../middlewares/auth.middleware');
const upload = require('../middlewares/upload.middleware');
const {
    getChamados,
    getChamado,
    createChamado,
    updateChamado,
    avaliarChamado
} = require('../controllers/chamadoController');

// Todas as rotas requerem autenticação
router.use(auth);

router.get('/', getChamados);
router.get('/:id', getChamado);
router.post('/', upload.single('foto'), createChamado);
router.put('/:id', upload.single('foto'), updateChamado);
router.post('/:id/avaliar', avaliarChamado);

module.exports = router;
