const express = require('express');
const { body, validationResult } = require('express-validator');
const Player = require('../models/Player');
const PlayerRole = require('../models/PlayerRole');
const Coach = require('../models/Coach');

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
router.get('/', async (req, res) => {
  try {
    const players = await Player.findAll({
      include: [
        { model: PlayerRole, as: 'playerRole' },
        { model: Coach, as: 'coach' }
      ],
      where: { isActive: true }
    });
    
    res.json({
      success: true,
      data: players
    });
  } catch (error) {
    console.error('Error fetching players:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching players',
      error: error.message
    });
  }
});

// Get player by ID
router.get('/:id', async (req, res) => {
  try {
    const player = await Player.findByPk(req.params.id, {
      include: [
        { model: PlayerRole, as: 'playerRole' },
        { model: Coach, as: 'coach' }
      ]
    });
    
    if (!player) {
      return res.status(404).json({
        success: false,
        message: 'Player not found'
      });
    }
    
    res.json({
      success: true,
      data: player
    });
  } catch (error) {
    console.error('Error fetching player:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching player',
      error: error.message
    });
  }
});

// Create new player
router.post('/', validatePlayer, async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation errors',
        errors: errors.array()
      });
    }

    // Check if email or username already exists
    const existingPlayer = await Player.findOne({
      where: {
        [Player.Sequelize.Op.or]: [
          { email: req.body.email },
          { userName: req.body.userName }
        ]
      }
    });

    if (existingPlayer) {
      return res.status(400).json({
        success: false,
        message: 'Email or username already exists'
      });
    }

    const player = await Player.create(req.body);
    
    res.status(201).json({
      success: true,
      message: 'Player created successfully',
      data: player
    });
  } catch (error) {
    console.error('Error creating player:', error);
    res.status(500).json({
      success: false,
      message: 'Error creating player',
      error: error.message
    });
  }
});

// Update player
router.put('/:id', async (req, res) => {
  try {
    const player = await Player.findByPk(req.params.id);
    
    if (!player) {
      return res.status(404).json({
        success: false,
        message: 'Player not found'
      });
    }

    await player.update(req.body);
    
    res.json({
      success: true,
      message: 'Player updated successfully',
      data: player
    });
  } catch (error) {
    console.error('Error updating player:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating player',
      error: error.message
    });
  }
});

// Delete player (soft delete)
router.delete('/:id', async (req, res) => {
  try {
    const player = await Player.findByPk(req.params.id);
    
    if (!player) {
      return res.status(404).json({
        success: false,
        message: 'Player not found'
      });
    }

    await player.destroy(); // This will soft delete due to paranoid: true
    
    res.json({
      success: true,
      message: 'Player deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting player:', error);
    res.status(500).json({
      success: false,
      message: 'Error deleting player',
      error: error.message
    });
  }
});

module.exports = router; 