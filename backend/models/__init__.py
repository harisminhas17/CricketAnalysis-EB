# Models package for Cricket Analysis Backend 

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .player_roles import PlayerRole
from .player_model import Player
from .super_admin_model import SuperAdmin
from .coach_model import Coach
