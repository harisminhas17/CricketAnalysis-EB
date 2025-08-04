require('dotenv').config();

const config = {
  // CORS configuration
  corsOrigins: [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001'
  ]
};

module.exports = config; 