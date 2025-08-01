const { DataTypes } = require('sequelize');
const { sequelize } = require('../database/connection');
const bcrypt = require('bcryptjs');

const Player = sequelize.define('Player', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  userName: {
    type: DataTypes.STRING(50),
    allowNull: false,
    unique: true,
    field: 'user_name'
  },
  email: {
    type: DataTypes.STRING(120),
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  password: {
    type: DataTypes.STRING(255),
    allowNull: false
  },
  phoneNumber: {
    type: DataTypes.STRING(20),
    allowNull: true,
    field: 'phone_number'
  },
  address: {
    type: DataTypes.STRING(255),
    allowNull: true
  },
  location: {
    type: DataTypes.STRING(255),
    allowNull: true
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    field: 'is_active'
  },
  name: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  dateOfBirth: {
    type: DataTypes.DATEONLY,
    allowNull: true,
    field: 'date_of_birth'
  },
  gender: {
    type: DataTypes.ENUM('male', 'female', 'other'),
    defaultValue: 'male'
  },
  country: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  city: {
    type: DataTypes.STRING(50),
    allowNull: true
  },
  profileImage: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'profile_image'
  },
  sportType: {
    type: DataTypes.ENUM('cricket', 'football'),
    defaultValue: 'cricket',
    field: 'sport_type'
  },
  playerRoleId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    field: 'player_role_id',
    references: {
      model: 'player_roles',
      key: 'id'
    }
  },
  dominantHand: {
    type: DataTypes.STRING(10),
    allowNull: true,
    field: 'dominant_hand'
  },
  battingStyle: {
    type: DataTypes.STRING(50),
    allowNull: true,
    field: 'batting_style'
  },
  bowlingStyle: {
    type: DataTypes.STRING(50),
    allowNull: true,
    field: 'bowling_style'
  },
  heightCm: {
    type: DataTypes.FLOAT,
    allowNull: true,
    field: 'height_cm'
  },
  weightKg: {
    type: DataTypes.FLOAT,
    allowNull: true,
    field: 'weight_kg'
  },
  teamName: {
    type: DataTypes.STRING(100),
    allowNull: true,
    field: 'team_name'
  },
  coachId: {
    type: DataTypes.INTEGER,
    allowNull: true,
    field: 'coach_id',
    references: {
      model: 'coaches',
      key: 'id'
    }
  },
  instagramLink: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'instagram_link'
  },
  facebookLink: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'facebook_link'
  },
  twitterLink: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'twitter_link'
  },
  youtubeLink: {
    type: DataTypes.STRING(255),
    allowNull: true,
    field: 'youtube_link'
  },
  deletedAt: {
    type: DataTypes.DATE,
    allowNull: true,
    field: 'deleted_at'
  }
}, {
  tableName: 'players',
  timestamps: true,
  paranoid: true, // This enables soft deletes
  hooks: {
    beforeCreate: async (player) => {
      if (player.password) {
        player.password = await bcrypt.hash(player.password, 12);
      }
    },
    beforeUpdate: async (player) => {
      if (player.changed('password')) {
        player.password = await bcrypt.hash(player.password, 12);
      }
    }
  }
});

// Instance methods
Player.prototype.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Class methods
Player.findByEmail = function(email) {
  return this.findOne({ where: { email } });
};

Player.findByUserName = function(userName) {
  return this.findOne({ where: { userName } });
};

module.exports = Player; 