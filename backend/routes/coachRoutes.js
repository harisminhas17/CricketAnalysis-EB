const express = require('express');
const { body, validationResult } = require('express-validator');
const { 
  getAllCoaches, 
  getCoachById, 
  createCoach, 
  updateCoach, 
  deleteCoach 
} = require('../controllers/coachController');

const router = express.Router();

// Validation middleware
const validateCoach = [
  body('email').isEmail().withMessage('Must be a valid email'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('name').notEmpty().withMessage('Name is required')
];

// Get all coaches
router.get('/', getAllCoaches);

// Get coach by ID
router.get('/:id', getCoachById);

// Create new coach
router.post('/', validateCoach, async (req, res) => {
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
  await createCoach(req, res);
});

// Update coach
router.put('/:id', updateCoach);

// Delete coach (soft delete)
router.delete('/:id', deleteCoach);

module.exports = router; 