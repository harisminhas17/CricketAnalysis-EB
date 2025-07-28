import enum

class SportType(enum.Enum):
    Cricket = "cricket"
    Football = "football"

class GenderEnum(enum.Enum):
    Male = "male"
    Female = "female"
    Other = "other"

class AdminRoleEnum(enum.Enum):
    SuperAdmin = "super_admin"
    Moderator = "moderator"
    Support = "support"

class CoachRoleEnum(enum.Enum):
    CricketCoach = "cricket_coach"
    FootballCoach = "football_coach"