from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import pymysql

# Register PyMySQL as the MySQL driver
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    # Configure SQLAlchemy for MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'poolclass': QueuePool,
        'connect_args': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': False
        }
    }
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            print("MySQL Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            print("Please check your MySQL connection settings.")

def get_db_session():
    """Get database session"""
    return db.session

def close_db_session():
    """Close database session"""
    db.session.close()

def test_connection(app):
    """Test MySQL connection"""
    try:
        with app.app_context():
            db.engine.execute("SELECT 1")
            print("MySQL connection test successful!")
            return True
    except Exception as e:
        print(f"MySQL connection test failed: {e}")
        return False
    """Create database if it doesn't exist"""
    try:
        # Get database configuration
        config = app.config
        host = config.get('MYSQL_HOST', 'localhost')
        port = config.get('MYSQL_PORT', 3306)
        user = config.get('MYSQL_USER', 'root')
        password = config.get('MYSQL_PASSWORD', '')
        database = config.get('MYSQL_DATABASE', 'cricket_db')
        
        # Create connection without database
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
        
        with engine.connect() as connection:
            connection.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{database}' created or already exists!")
            
    except Exception as e:
        print(f"Error creating database: {e}")
        print("Please check your MySQL server is running and credentials are correct.") 