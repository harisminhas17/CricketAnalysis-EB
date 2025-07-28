from models.player_roles import PlayerRole
from app import app
from models import db

def run():
    roles = [
        'Batsman',
        'Bowler',
        'All-Rounder',
        'Wicket Keeper',
        'Opening Batsman',
        'Middle Order Batsman',
        'Fast Bowler',
        'Medium Pace Bowler',
        'Off Spin Bowler',
        'Leg Spin Bowler',
        'Left Arm Fast Bowler',
        'Right Arm Fast Bowler',
        'Left Arm Spinner',
        'Right Arm Spinner',
        'Captain',
        'Vice Captain',
        'Wicket Keeper Batsman',
        'Finisher',
        'Night Watchman',
        'Powerplay Specialist',
        'Death Over Specialist',
        'Strike Bowler',
        'Pinch Hitter',
        'Part-time Bowler'
    ]

    for name in roles:
        exists = PlayerRole.query.filter_by(name=name, sport_type='Cricket').first()
        if not exists:
            db.session.add(PlayerRole(name=name, sport_type='Cricket'))
    
    db.session.commit()
    print("✅Player Roles Seed Successfully")

# Run when called directly
if __name__ == '__main__':
    with app.app_context():
        run()
