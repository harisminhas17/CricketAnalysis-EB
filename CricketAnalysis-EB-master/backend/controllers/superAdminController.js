const { prisma } = require('../lib/prisma');

// Get all admins
const getAllAdmins = async (req, res) => {
  try {
    const admins = await prisma.superAdmin.findMany({
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
};

// Get admin by ID
const getAdminById = async (req, res) => {
  try {
    const admin = await prisma.superAdmin.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
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
};

// Create new admin
const createAdmin = async (req, res) => {
  try {
    // Check if email already exists
    const existingAdmin = await prisma.superAdmin.findFirst({
      where: {
        email: req.body.email
      }
    });

    if (existingAdmin) {
      return res.status(400).json({
        success: false,
        message: 'Email already exists'
      });
    }

    const admin = await prisma.superAdmin.create({
      data: req.body
    });
    
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
};

// Update admin
const updateAdmin = async (req, res) => {
  try {
    const admin = await prisma.superAdmin.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!admin) {
      return res.status(404).json({
        success: false,
        message: 'Admin not found'
      });
    }

    const updatedAdmin = await prisma.superAdmin.update({
      where: { id: BigInt(req.params.id) },
      data: req.body
    });
    
    res.json({
      success: true,
      message: 'Admin updated successfully',
      data: updatedAdmin
    });
  } catch (error) {
    console.error('Error updating admin:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating admin',
      error: error.message
    });
  }
};

// Delete admin (soft delete)
const deleteAdmin = async (req, res) => {
  try {
    const admin = await prisma.superAdmin.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!admin) {
      return res.status(404).json({
        success: false,
        message: 'Admin not found'
      });
    }

    await prisma.superAdmin.update({
      where: { id: BigInt(req.params.id) },
      data: { 
        isActive: false,
        deletedAt: new Date()
      }
    });
    
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
};

module.exports = {
  getAllAdmins,
  getAdminById,
  createAdmin,
  updateAdmin,
  deleteAdmin
};
