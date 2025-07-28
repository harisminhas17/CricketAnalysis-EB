from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .enums import GenderEnum, SportType, CoachRoleEnum

db = SQLAlchemy()

class Coach(db.Model):
    __tablename__ = 'coaches'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.Male)
    sport_type = db.Column(db.Enum(SportType), default=SportType.Cricket)
    phone_number = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    coach_role = db.Column(db.Enum(CoachRoleEnum), default=CoachRoleEnum.CricketCoach)
    coach_speciality = db.Column(db.String(100), nullable=True)
    assigned_team = db.Column(db.String(100), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<Coach {self.name} ({self.sport_type.value})>"