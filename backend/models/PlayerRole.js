const { DataTypes } = require('sequelize');
const { sequelize } = require('../database/connection');

const PlayerRole = sequelize.define('PlayerRole', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: DataTypes.STRING(50),
    allowNull: false,
    unique: true
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    field: 'is_active'
  }
}, {
  tableName: 'player_roles',
  timestamps: true
});

module.exports = PlayerRole; 