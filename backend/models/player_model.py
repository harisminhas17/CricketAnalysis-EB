from datetime import datetime
from .enums import SportType, GenderEnum
from models import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True) 
    is_active = db.Column(db.Boolean, default=True)

    # Personal Info
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.Male)
    country = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)

    # Sports Info
    sport_type = db.Column(db.Enum(SportType), default=SportType.Cricket)
    player_role_id = db.Column(db.Integer, db.ForeignKey('player_roles.id'), nullable=False)
    player_role = db.relationship('PlayerRole', backref='players')
    dominant_hand = db.Column(db.String(10), nullable=True)
    batting_style = db.Column(db.String(50), nullable=True)  # For cricket
    bowling_style = db.Column(db.String(50), nullable=True)  # For cricket

    # Physical Info
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)

    # Team + Coach Info
    team_name = db.Column(db.String(100), nullable=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=True) 
    coach = db.relationship('Coach', backref='players')

    # Social Media
    instagram_link = db.Column(db.String(255), nullable=True)
    facebook_link = db.Column(db.String(255), nullable=True)
    twitter_link = db.Column(db.String(255), nullable=True)
    youtube_link = db.Column(db.String(255), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<Player {self.name} ({self.sport_type.value})>"
