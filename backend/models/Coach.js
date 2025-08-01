const { DataTypes } = require('sequelize');
const { sequelize } = require('../database/connection');
const bcrypt = require('bcryptjs');

const Coach = sequelize.define('Coach', {
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
  sportType: {
    type: DataTypes.ENUM('cricket', 'football'),
    defaultValue: 'cricket',
    field: 'sport_type'
  },
  phoneNumber: {
    type: DataTypes.STRING(20),
    allowNull: true,
    field: 'phone_number'
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
  coachRole: {
    type: DataTypes.ENUM('cricket_coach', 'football_coach'),
    defaultValue: 'cricket_coach',
    field: 'coach_role'
  },
  coachSpeciality: {
    type: DataTypes.STRING(100),
    allowNull: true,
    field: 'coach_speciality'
  },
  assignedTeam: {
    type: DataTypes.STRING(100),
    allowNull: true,
    field: 'assigned_team'
  },
  experienceYears: {
    type: DataTypes.INTEGER,
    allowNull: true,
    field: 'experience_years'
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    field: 'is_active'
  },
  deletedAt: {
    type: DataTypes.DATE,
    allowNull: true,
    field: 'deleted_at'
  }
}, {
  tableName: 'coaches',
  timestamps: true,
  paranoid: true, // This enables soft deletes
  hooks: {
    beforeCreate: async (coach) => {
      if (coach.password) {
        coach.password = await bcrypt.hash(coach.password, 12);
      }
    },
    beforeUpdate: async (coach) => {
      if (coach.changed('password')) {
        coach.password = await bcrypt.hash(coach.password, 12);
      }
    }
  }
});

// Instance methods
Coach.prototype.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Class methods
Coach.findByEmail = function(email) {
  return this.findOne({ where: { email } });
};

Coach.findByUserName = function(userName) {
  return this.findOne({ where: { userName } });
};

module.exports = Coach; 