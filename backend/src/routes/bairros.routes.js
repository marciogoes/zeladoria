const express = require('express');
const router = express.Router();
const { getBairros } = require('../controllers/bairroController');

// Listar bairros é público
router.get('/', getBairros);

module.exports = router;
