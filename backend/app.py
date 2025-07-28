from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config.config import config
from dotenv import load_dotenv 
from models import db, Player, Coach, SuperAdmin, PlayerRole
import os

# Initialize Flask app
# Load environment variables
load_dotenv()

app = Flask(__name__)

env = os.getenv('ENV', 'development')
app.config.from_object(config[env]) # Load configuration

# Initialize CORS
CORS(app, origins=app.config['CORS_ORIGINS'])

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Cricket Analysis Backend Server is running!"})

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)