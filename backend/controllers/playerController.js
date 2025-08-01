const { prisma } = require('../lib/prisma');

// Get all players
const getAllPlayers = async (req, res) => {
  try {
    const players = await prisma.player.findMany({
      include: {
        playerRole: true,
        coach: true
      },
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
};

// Get player by ID
const getPlayerById = async (req, res) => {
  try {
    const player = await prisma.player.findUnique({
      where: { id: BigInt(req.params.id) },
      include: {
        playerRole: true,
        coach: true
      }
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
};

// Create new player
const createPlayer = async (req, res) => {
  try {
    // Check if email or username already exists
    const existingPlayer = await prisma.player.findFirst({
      where: {
        OR: [
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

    const player = await prisma.player.create({
      data: {
        ...req.body,
        playerRoleId: BigInt(req.body.playerRoleId),
        coachId: req.body.coachId ? BigInt(req.body.coachId) : null,
        clubId: req.body.clubId ? BigInt(req.body.clubId) : null
      }
    });
    
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
};

// Update player
const updatePlayer = async (req, res) => {
  try {
    const player = await prisma.player.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!player) {
      return res.status(404).json({
        success: false,
        message: 'Player not found'
      });
    }

    const updatedPlayer = await prisma.player.update({
      where: { id: BigInt(req.params.id) },
      data: {
        ...req.body,
        playerRoleId: req.body.playerRoleId ? BigInt(req.body.playerRoleId) : undefined,
        coachId: req.body.coachId ? BigInt(req.body.coachId) : undefined,
        clubId: req.body.clubId ? BigInt(req.body.clubId) : undefined
      }
    });
    
    res.json({
      success: true,
      message: 'Player updated successfully',
      data: updatedPlayer
    });
  } catch (error) {
    console.error('Error updating player:', error);
    res.status(500).json({
      success: false,
      message: 'Error updating player',
      error: error.message
    });
  }
};

// Delete player (soft delete)
const deletePlayer = async (req, res) => {
  try {
    const player = await prisma.player.findUnique({
      where: { id: BigInt(req.params.id) }
    });
    
    if (!player) {
      return res.status(404).json({
        success: false,
        message: 'Player not found'
      });
    }

    await prisma.player.update({
      where: { id: BigInt(req.params.id) },
      data: { 
        isActive: false,
        deletedAt: new Date()
      }
    });
    
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
};

module.exports = {
  getAllPlayers,
  getPlayerById,
  createPlayer,
  updatePlayer,
  deletePlayer
};
