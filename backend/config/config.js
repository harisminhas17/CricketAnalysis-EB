require('dotenv').config();

const config = {
  // Server configuration
  port: process.env.PORT || 5000,
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Database configuration
  database: {
    host: process.env.MYSQL_HOST || 'localhost',
    port: parseInt(process.env.MYSQL_PORT) || 3306,
    username: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || '',
    database: process.env.MYSQL_DATABASE || 'cricket_db',
    dialect: 'mysql',
    charset: 'utf8mb4',
    collation: 'utf8mb4_unicode_ci',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  },
  
  // JWT configuration
  jwt: {
    secret: process.env.JWT_SECRET_KEY || 'jwt-secret-key-change-in-production',
    expiresIn: '1h',
    refreshExpiresIn: '7d'
  },
  
  // CORS configuration
  corsOrigins: [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001'
  ],
  
  // File upload configuration
  upload: {
    folder: 'uploads',
    maxSize: 16 * 1024 * 1024, // 16MB
    allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
  },
  
  // Security configuration
  security: {
    bcryptRounds: 12,
    rateLimitWindowMs: 15 * 60 * 1000, // 15 minutes
    rateLimitMax: 100
  }
};

module.exports = config; 