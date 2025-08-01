const express = require('express');
const { body, validationResult } = require('express-validator');
const { 
  getAllPlayers, 
  getPlayerById, 
  createPlayer, 
  updatePlayer, 
  deletePlayer 
} = require('../controllers/playerController');

const router = express.Router();

// Validation middleware
const validatePlayer = [
  body('userName').isLength({ min: 3 }).withMessage('Username must be at least 3 characters'),
  body('email').isEmail().withMessage('Must be a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('name').notEmpty().withMessage('Name is required'),
  body('playerRoleId').isInt().withMessage('Player role ID must be a number')
];

// Get all players
router.get('/', getAllPlayers);

// Get player by ID
router.get('/:id', getPlayerById);

// Create new player
router.post('/', validatePlayer, async (req, res) => {
  // Check for validation errors
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      message: 'Validation errors',
      errors: errors.array()
    });
  }
  
  // Call controller function
  await createPlayer(req, res);
});

// Update player
router.put('/:id', updatePlayer);

// Delete player (soft delete)
router.delete('/:id', deletePlayer);

module.exports = router; 