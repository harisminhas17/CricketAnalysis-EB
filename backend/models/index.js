const Player = require('./Player');
const Coach = require('./Coach');
const SuperAdmin = require('./SuperAdmin');
const PlayerRole = require('./PlayerRole');

// Define associations
Player.belongsTo(PlayerRole, {
  foreignKey: 'playerRoleId',
  as: 'playerRole'
});

PlayerRole.hasMany(Player, {
  foreignKey: 'playerRoleId',
  as: 'players'
});

Player.belongsTo(Coach, {
  foreignKey: 'coachId',
  as: 'coach'
});

Coach.hasMany(Player, {
  foreignKey: 'coachId',
  as: 'players'
});

module.exports = {
  Player,
  Coach,
  SuperAdmin,
  PlayerRole
}; 