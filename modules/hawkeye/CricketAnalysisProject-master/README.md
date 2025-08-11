# Cricket Analytics Project

A comprehensive cricket analytics platform that provides real-time analysis, training feedback, and performance metrics for cricket players.

## Features

- Real-time ball tracking and analysis
- Multi-camera support for comprehensive coverage
- Advanced batting analysis
- Training mode with instant feedback
- Match mode for live game analysis
- Historical data analysis and visualization
- Performance metrics and statistics
- Social sharing capabilities
- Data export functionality

## Project Structure

```
CricketAnalyticsProject/
├── frontend/           # React frontend application
├── backend/           # Python Flask backend
├── scripts/           # Utility scripts
└── docs/             # Documentation
```

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8 or higher
- OpenCV
- YOLOv8
- React
- Flask

## Setup Instructions

### Quick Start (Recommended)

1. Run the startup script to check and configure everything:
   ```bash
   python scripts/start_project.py
   ```

2. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```

3. Start the frontend server (in a new terminal):
   ```bash
   cd frontend
   npm install  # Only needed first time
   npm start
   ```

### Manual Setup

#### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Development

- Backend API documentation is available at `/api/docs` when running the server
- Frontend components are located in `frontend/src/components`
- Backend modules are organized by functionality in the `backend` directory

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please open an issue in the repository. 