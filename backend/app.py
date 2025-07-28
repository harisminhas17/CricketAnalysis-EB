from flask import Flask, jsonify
from flask_cors import CORS
from config.config import config
from database.connection import init_db
from dotenv import load_dotenv  
import os
load_dotenv()

app = Flask(__name__)
env = os.getenv('ENV', 'development')
app.config.from_object(config[env])

CORS(app, origins=app.config['CORS_ORIGINS'])
init_db(app)

@app.route('/')
def home():
    return jsonify({"message": "Cricket Analysis Backend Server is running!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)