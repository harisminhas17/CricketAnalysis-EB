const express = require('express');
const { body, validationResult } = require('express-validator');
const Coach = require('../models/Coach');
const Player = require('../models/Player');

const router = express.Router();

// Validation middleware
const validateCoach = [
  body('userName').isLength({ min: 3 }).withMessage('Username must be at least 3 characters'),
  body('email').isEmail().withMessage('Must be a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('name').notEmpty().withMessage('Name is required')
];

// Get all coaches
router.get('/', async (req, res) => {
  try {
    const coaches = await Coach.findAll({
      include: [
        { model: Player, as: 'players' }
      ],
      where: { isActive: true }
    });
    
    res.json({
      success: true,
      data: coaches
    });
  } catch (error) {
    console.error('Error fetching coaches:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching coaches',
      error: error.message
    });
  }
});

// Get coach by ID
router.get('/:id', async (req, res) => {
  try {
    const coach = await Coach.findByPk(req.params.id, {
      include: [
        { model: Player, as: 'players' }
      ]
    });
    
    if (!coach) {
      return res.status(404).json({
        success: false,
        message: 'Coach not found'
      });
    }
    
    res.json({
      success: true,
      data: coach
    });
  } catch (error) {
    console.error('Error fetching coach:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching coach',
      error: error.message
    });
  }
});

// Create new coach
router.post('/', validateCoach, async (req, res) => {
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
    const existingCoach = await Coach.findOne({
      where: {
        [Coach.Sequelize.Op.or]: [
          { email: req.body.email },
          { userName: req.body.userName }
        ]
      }
    });

    if (existingCoach) {
      return res.status(400).json({
        success: false,
        message: 'Email or username already exists'
      });
    }

    const coach = await Coach.create(req.body);
    
    res.status(201).json({
      success: true,
      message: 'Coach created successfully',
      data: coach
    });
  } catch (error) {
    console.error('Error creating coach:', error);
    res.status(500).json({
      success: false,
      message: 'Error creating coach',
      error: error.message
    });
  }
});

// Update coach
router.put('/:id', async (req, res) => {
  try {
    const coach = await Coach.findByPk(req.params.id);
    
    if (!coach) {
      return res.status(404).json({
        success: false,
        message: 'Coach not found'
      });
    }

    await coach.update(req.body);
    
    res.json({
      success: true,
      message: 'Coach updated successfully',
      data: coach
    });
  } catch (error) {
    console.error('Error updating coach:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating coach',
      error: error.message
    });
  }
});

// Delete coach (soft delete)
router.delete('/:id', async (req, res) => {
  try {
    const coach = await Coach.findByPk(req.params.id);
    
    if (!coach) {
      return res.status(404).json({
        success: false,
        message: 'Coach not found'
      });
    }

    await coach.destroy(); // This will soft delete due to paranoid: true
    
    res.json({
      success: true,
      message: 'Coach deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting coach:', error);
    res.status(500).json({
      success: false,
      message: 'Error deleting coach',
      error: error.message
    });
  }
});

module.exports = router; 