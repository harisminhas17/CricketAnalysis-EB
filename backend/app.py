from flask import Flask, jsonify
from flask_cors import CORS
from config.config import Config
from database.connection import init_db

app = Flask(__name__)
CORS(app)
init_db(app)

@app.route('/')
def home():
    return jsonify({"message": "Cricket Analysis Backend Server is running!"})

@app.route('/api/test')
def test():
    return jsonify({"status": "success", "message": "Backend API is working!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
