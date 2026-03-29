const express = require('express');
const router = express.Router();
const { auth } = require('../middlewares/auth.middleware');
const {
    register,
    login,
    getMe,
    updateMe
} = require('../controllers/authController');

// Rotas públicas
router.post('/register', register);
router.post('/login', login);

// Rotas protegidas
router.get('/me', auth, getMe);
router.put('/me', auth, updateMe);

module.exports = router;
