from .enums import SportType
from models import db

class PlayerRole(db.Model):
    __tablename__ = 'player_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)     
    sport_type = db.Column(db.Enum(SportType), default=SportType.Cricket)

    def __repr__(self):
        return f"<PlayerRole {self.name} ({self.sport_type})>"
