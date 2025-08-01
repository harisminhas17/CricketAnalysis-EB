# Cricket Analysis EB 🏏

A comprehensive cricket analysis platform that provides player management, coach coordination, and performance tracking for cricket teams and clubs.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🏃‍♂️ Player Management
- Player registration and profile management
- Performance tracking and statistics
- Role-based player categorization (Batsman, Bowler, All-rounder, etc.)
- Social media integration
- Physical attributes tracking (height, weight, dominant hand)

### 👨‍🏫 Coach Management
- Coach registration and profile management
- Specialization tracking (cricket coach, football coach)
- Experience and expertise documentation
- Team assignment capabilities

### 🏢 Club Management
- Club registration and administration
- Player and coach association
- Location-based club management

### 🔐 Authentication & Security
- JWT-based authentication
- Role-based access control (Super Admin, Coach, Player)
- Secure password hashing with bcrypt
- Rate limiting and security headers

### 📊 Data Management
- MySQL database with Prisma ORM
- Comprehensive data validation
- Soft delete functionality
- Audit trails with timestamps

## 🛠 Tech Stack

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Prisma** - Database ORM
- **MySQL** - Database
- **JWT** - Authentication
- **bcryptjs** - Password hashing
- **Helmet** - Security headers
- **CORS** - Cross-origin resource sharing
- **Morgan** - HTTP request logger

### Frontend
- **React.js** - Frontend framework
- **React Scripts** - Development tools
- **Testing Library** - Testing utilities

## 📁 Project Structure

```
Cricket Analysis EB/
├── backend/
│   ├── config/
│   │   └── config.js
│   ├── controllers/
│   │   ├── coachController.js
│   │   ├── playerController.js
│   │   └── superAdminController.js
│   ├── lib/
│   │   └── prisma.js
│   ├── prisma/
│   │   └── schema.prisma
│   ├── routes/
│   │   ├── adminRoutes.js
│   │   ├── coachRoutes.js
│   │   └── playerRoutes.js
│   ├── seeders/
│   │   └── playerRolesSeeder.js
│   ├── utils/
│   ├── server.js
│   └── package.json
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── utils/
    └── package.json
```

## ⚙️ Prerequisites

Before running this project, make sure you have the following installed:

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **MySQL** (v8.0 or higher)
- **Git**

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cricket-analysis-eb.git
cd cricket-analysis-eb
```

### 2. Backend Setup

```bash
cd backend
npm install
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in the backend directory:

```bash
cd backend
cp env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL="mysql://username:password@localhost:3306/cricket_analysis_db"

# Server Configuration
PORT=5000
NODE_ENV=development

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=24h

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# File Upload Configuration
MAX_FILE_SIZE=16777216
UPLOAD_PATH=./uploads
```

### 2. Database Setup

```bash
cd backend

# Generate Prisma client
npm run prisma:generate

# Run database migrations
npm run prisma:migrate

# Seed initial data (optional)
npm run prisma:studio
```

## 🎯 Usage

### Starting the Backend Server

```bash
cd backend

# Development mode
npm run dev

# Production mode
npm start
```

The backend server will start on `http://localhost:5000`

### Starting the Frontend Application

```bash
cd frontend

# Development mode
npm start
```

The frontend application will start on `http://localhost:3000`

## 🔌 API Endpoints

### Authentication
- `POST /api/admin/login` - Super admin login
- `POST /api/coaches/login` - Coach login
- `POST /api/players/login` - Player login

### Player Management
- `GET /api/players` - Get all players
- `POST /api/players` - Create new player
- `GET /api/players/:id` - Get player by ID
- `PUT /api/players/:id` - Update player
- `DELETE /api/players/:id` - Delete player

### Coach Management
- `GET /api/coaches` - Get all coaches
- `POST /api/coaches` - Create new coach
- `GET /api/coaches/:id` - Get coach by ID
- `PUT /api/coaches/:id` - Update coach
- `DELETE /api/coaches/:id` - Delete coach

### Admin Management
- `GET /api/admin` - Get admin profile
- `PUT /api/admin` - Update admin profile

## 🗄️ Database Schema

The application uses the following main entities:

- **SuperAdmin** - System administrators
- **Player** - Cricket players with roles and attributes
- **Coach** - Cricket coaches with specializations
- **Club** - Cricket clubs and teams
- **PlayerRole** - Player role definitions (Batsman, Bowler, etc.)

### Key Features:
- Soft delete functionality
- Comprehensive audit trails
- Role-based relationships
- Social media integration
- Physical attributes tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/cricket-analysis-eb/issues) page
2. Create a new issue with detailed information
3. Contact the development team

---

**Made with ❤️ for Cricket Analysis** 