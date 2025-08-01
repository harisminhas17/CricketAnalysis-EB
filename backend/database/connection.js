const { Sequelize } = require('sequelize');
const config = require('../config/config');

// Create Sequelize instance
const sequelize = new Sequelize(
  config.database.database,
  config.database.username,
  config.database.password,
  {
    host: config.database.host,
    port: config.database.port,
    dialect: config.database.dialect,
    charset: config.database.charset,
    collate: config.database.collation,
    logging: config.database.logging,
    pool: config.database.pool,
    define: {
      timestamps: true,
      underscored: true,
      freezeTableName: true
    }
  }
);

// Test database connection
const testConnection = async () => {
  try {
    await sequelize.authenticate();
    console.log('Database connection has been established successfully.');
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
};

// Initialize database with models
const initializeDatabase = async () => {
  try {
    // Import models and associations
    require('../models/index');
    
    // Sync database (in development)
    if (config.nodeEnv === 'development') {
      await sequelize.sync({ alter: true });
      console.log('Database synced successfully.');
    }
  } catch (error) {
    console.error('Error initializing database:', error);
  }
};

module.exports = {
  sequelize,
  testConnection,
  initializeDatabase
}; 