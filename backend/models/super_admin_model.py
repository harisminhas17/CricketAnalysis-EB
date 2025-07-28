from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .enums import AdminRoleEnum, GenderEnum

db = SQLAlchemy()

class SuperAdmin(db.Model):
    __tablename__ = 'super_admins'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)    
    is_active = db.Column(db.Boolean, default=True)

    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.Male)
    country = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)

    admin_role = db.Column(db.Enum(AdminRoleEnum), default=AdminRoleEnum.SuperAdmin)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<SuperAdmin {self.name} ({self.admin_role.value})>"
