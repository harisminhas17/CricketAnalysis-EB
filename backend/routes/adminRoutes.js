const express = require('express');
const { body, validationResult } = require('express-validator');
const SuperAdmin = require('../models/SuperAdmin');

const router = express.Router();

// Validation middleware
const validateAdmin = [
  body('userName').isLength({ min: 3 }).withMessage('Username must be at least 3 characters'),
  body('email').isEmail().withMessage('Must be a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('name').notEmpty().withMessage('Name is required')
];

// Get all admins
router.get('/', async (req, res) => {
  try {
    const admins = await SuperAdmin.findAll({
      where: { isActive: true }
    });
    
    res.json({
      success: true,
      data: admins
    });
  } catch (error) {
    console.error('Error fetching admins:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching admins',
      error: error.message
    });
  }
});

// Get admin by ID
router.get('/:id', async (req, res) => {
  try {
    const admin = await SuperAdmin.findByPk(req.params.id);
    
    if (!admin) {
      return res.status(404).json({
        success: false,
        message: 'Admin not found'
      });
    }
    
    res.json({
      success: true,
      data: admin
    });
  } catch (error) {
    console.error('Error fetching admin:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching admin',
      error: error.message
    });
  }
});

// Create new admin
router.post('/', validateAdmin, async (req, res) => {
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
    const existingAdmin = await SuperAdmin.findOne({
      where: {
        [SuperAdmin.Sequelize.Op.or]: [
          { email: req.body.email },
          { userName: req.body.userName }
        ]
      }
    });

    if (existingAdmin) {
      return res.status(400).json({
        success: false,
        message: 'Email or username already exists'
      });
    }

    const admin = await SuperAdmin.create(req.body);
    
    res.status(201).json({
      success: true,
      message: 'Admin created successfully',
      data: admin
    });
  } catch (error) {
    console.error('Error creating admin:', error);
    res.status(500).json({
      success: false,
      message: 'Error creating admin',
      error: error.message
    });
  }
});

// Update admin
router.put('/:id', async (req, res) => {
  try {
    const admin = await SuperAdmin.findByPk(req.params.id);
    
    if (!admin) {
      return res.status(404).json({
        success: false,
        message: 'Admin not found'
      });
    }

    await admin.update(req.body);
    
    res.json({
      success: true,
      message: 'Admin updated successfully',
      data: admin
    });
  } catch (error) {
    console.error('Error updating admin:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating admin',
      error: error.message
    });
  }
});

// Delete admin (soft delete)
router.delete('/:id', async (req, res) => {
  try {
    const admin = await SuperAdmin.findByPk(req.params.id);
    
    if (!admin) {
      return res.status(404).json({
        success: false,
        message: 'Admin not found'
      });
    }

    await admin.destroy(); // This will soft delete due to paranoid: true
    
    res.json({
      success: true,
      message: 'Admin deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting admin:', error);
    res.status(500).json({
      success: false,
      message: 'Error deleting admin',
      error: error.message
    });
  }
});

module.exports = router; 