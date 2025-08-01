const express = require('express');
const { body, validationResult } = require('express-validator');
const { 
  getAllAdmins, 
  getAdminById, 
  createAdmin, 
  updateAdmin, 
  deleteAdmin 
} = require('../controllers/superAdminController');

const router = express.Router();

// Validation middleware
const validateAdmin = [
  body('email').isEmail().withMessage('Must be a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('name').notEmpty().withMessage('Name is required')
];

// Get all admins
router.get('/', getAllAdmins);

// Get admin by ID
router.get('/:id', getAdminById);

// Create new admin
router.post('/', validateAdmin, async (req, res) => {
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
  await createAdmin(req, res);
});

// Update admin
router.put('/:id', updateAdmin);

// Delete admin (soft delete)
router.delete('/:id', deleteAdmin);

module.exports = router; 