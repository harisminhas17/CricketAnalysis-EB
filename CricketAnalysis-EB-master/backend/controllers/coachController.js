const { prisma } = require('../lib/prisma');

// Get all coaches
const getAllCoaches = async (req, res) => {
  try {
    const coaches = await prisma.coach.findMany({
      include: {
        players: true
      },
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
};

// Get coach by ID
const getCoachById = async (req, res) => {
  try {
    const coach = await prisma.coach.findUnique({
      where: { id: BigInt(req.params.id) },
      include: {
        players: true
      }
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
};

// Create new coach
const createCoach = async (req, res) => {
  try {
    // Check if email already exists
    const existingCoach = await prisma.coach.findFirst({
      where: {
        email: req.body.email
      }
    });

    if (existingCoach) {
      return res.status(400).json({
        success: false,
        message: 'Email already exists'
      });
    }

    const coach = await prisma.coach.create({
      data: req.body
    });
    
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
};

// Update coach
const updateCoach = async (req, res) => {
  try {
    const coach = await prisma.coach.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!coach) {
      return res.status(404).json({
        success: false,
        message: 'Coach not found'
      });
    }

    const updatedCoach = await prisma.coach.update({
      where: { id: BigInt(req.params.id) },
      data: req.body
    });
    
    res.json({
      success: true,
      message: 'Coach updated successfully',
      data: updatedCoach
    });
  } catch (error) {
    console.error('Error updating coach:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating coach',
      error: error.message
    });
  }
};

// Delete coach (soft delete)
const deleteCoach = async (req, res) => {
  try {
    const coach = await prisma.coach.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!coach) {
      return res.status(404).json({
        success: false,
        message: 'Coach not found'
      });
    }

    await prisma.coach.update({
      where: { id: BigInt(req.params.id) },
      data: { 
        isActive: false,
        deletedAt: new Date()
      }
    });
    
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
};

module.exports = {
  getAllCoaches,
  getCoachById,
  createCoach,
  updateCoach,
  deleteCoach
};
