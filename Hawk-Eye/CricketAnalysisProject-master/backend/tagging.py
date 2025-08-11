import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Player:
    id: str
    name: str
    role: str
    team: str
    jersey_number: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Event:
    id: str
    type: str
    timestamp: float
    description: str
    player_id: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Tag:
    id: str
    type: str
    description: str
    timestamp: float
    player_id: Optional[str] = None
    event_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

class TaggingSystem:
    def __init__(self, data_dir: str = "data/tags"):
        self.data_dir = data_dir
        self._ensure_data_directory()
        self.players: Dict[str, Player] = {}
        self.events: Dict[str, Event] = {}
        self.tags: Dict[str, Tag] = {}
        self._load_data()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_data(self):
        """Load existing data from files."""
        try:
            # Load players
            players_path = os.path.join(self.data_dir, 'players.json')
            if os.path.exists(players_path):
                with open(players_path, 'r') as f:
                    players_data = json.load(f)
                    for player_data in players_data:
                        player = Player(**player_data)
                        self.players[player.id] = player
            
            # Load events
            events_path = os.path.join(self.data_dir, 'events.json')
            if os.path.exists(events_path):
                with open(events_path, 'r') as f:
                    events_data = json.load(f)
                    for event_data in events_data:
                        event = Event(**event_data)
                        self.events[event.id] = event
            
            # Load tags
            tags_path = os.path.join(self.data_dir, 'tags.json')
            if os.path.exists(tags_path):
                with open(tags_path, 'r') as f:
                    tags_data = json.load(f)
                    for tag_data in tags_data:
                        tag = Tag(**tag_data)
                        self.tags[tag.id] = tag
                        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
    
    def _save_data(self):
        """Save data to files."""
        try:
            # Save players
            players_path = os.path.join(self.data_dir, 'players.json')
            with open(players_path, 'w') as f:
                json.dump([player.__dict__ for player in self.players.values()], f, indent=4)
            
            # Save events
            events_path = os.path.join(self.data_dir, 'events.json')
            with open(events_path, 'w') as f:
                json.dump([event.__dict__ for event in self.events.values()], f, indent=4)
            
            # Save tags
            tags_path = os.path.join(self.data_dir, 'tags.json')
            with open(tags_path, 'w') as f:
                json.dump([tag.__dict__ for tag in self.tags.values()], f, indent=4)
                
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def add_player(self, name: str, role: str, team: str, jersey_number: Optional[int] = None) -> Player:
        """Add a new player."""
        player_id = f"player_{len(self.players) + 1}"
        player = Player(
            id=player_id,
            name=name,
            role=role,
            team=team,
            jersey_number=jersey_number
        )
        self.players[player_id] = player
        self._save_data()
        return player
    
    def add_event(self, type: str, timestamp: float, description: str, player_id: str, confidence: float, metadata: Dict[str, Any] = None) -> Event:
        """Add a new event."""
        event_id = f"event_{len(self.events) + 1}"
        event = Event(
            id=event_id,
            type=type,
            timestamp=timestamp,
            description=description,
            player_id=player_id,
            confidence=confidence,
            metadata=metadata or {}
        )
        self.events[event_id] = event
        self._save_data()
        return event
    
    def add_tag(self, type: str, description: str, timestamp: float, player_id: Optional[str] = None, event_id: Optional[str] = None, metadata: Dict[str, Any] = None) -> Tag:
        """Add a new tag."""
        tag_id = f"tag_{len(self.tags) + 1}"
        tag = Tag(
            id=tag_id,
            type=type,
            description=description,
            timestamp=timestamp,
            player_id=player_id,
            event_id=event_id,
            metadata=metadata or {}
        )
        self.tags[tag_id] = tag
        self._save_data()
        return tag
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        return self.players.get(player_id)
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Get an event by ID."""
        return self.events.get(event_id)
    
    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Get a tag by ID."""
        return self.tags.get(tag_id)
    
    def get_players_by_team(self, team: str) -> List[Player]:
        """Get all players in a team."""
        return [player for player in self.players.values() if player.team == team]
    
    def get_events_by_player(self, player_id: str) -> List[Event]:
        """Get all events for a player."""
        return [event for event in self.events.values() if event.player_id == player_id]
    
    def get_tags_by_player(self, player_id: str) -> List[Tag]:
        """Get all tags for a player."""
        return [tag for tag in self.tags.values() if tag.player_id == player_id]
    
    def get_tags_by_event(self, event_id: str) -> List[Tag]:
        """Get all tags for an event."""
        return [tag for tag in self.tags.values() if tag.event_id == event_id]
    
    def get_tags_by_type(self, type: str) -> List[Tag]:
        """Get all tags of a specific type."""
        return [tag for tag in self.tags.values() if tag.type == type]
    
    def get_events_by_type(self, type: str) -> List[Event]:
        """Get all events of a specific type."""
        return [event for event in self.events.values() if event.type == type]
    
    def get_events_in_timerange(self, start_time: float, end_time: float) -> List[Event]:
        """Get all events within a time range."""
        return [event for event in self.events.values() if start_time <= event.timestamp <= end_time]
    
    def get_tags_in_timerange(self, start_time: float, end_time: float) -> List[Tag]:
        """Get all tags within a time range."""
        return [tag for tag in self.tags.values() if start_time <= tag.timestamp <= end_time]
    
    def update_tag(self, video_id: str, tag_id: str, updates: Dict) -> bool:
        """Update an existing tag"""
        try:
            tags = self.tags.get(video_id, [])
            for tag in tags:
                if tag.id == tag_id:
                    for key, value in updates.items():
                        setattr(tag, key, value)
                    self._save_data()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating tag: {str(e)}")
            raise
    
    def delete_tag(self, video_id: str, tag_id: str) -> bool:
        """Delete a tag"""
        try:
            tags = self.tags.get(video_id, [])
            for i, tag in enumerate(tags):
                if tag.id == tag_id:
                    tags.pop(i)
                    self._save_data()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting tag: {str(e)}")
            raise
    
    def get_tags_for_sharing(self, video_id: str, 
                           player_ids: Optional[List[str]] = None,
                           event_types: Optional[List[str]] = None,
                           time_range: Optional[tuple] = None) -> List[Tag]:
        """Get filtered tags for sharing"""
        tags = self.tags.get(video_id, [])
        
        if player_ids:
            tags = [t for t in tags if t.player_id in player_ids]
        
        if event_types:
            event_ids = [e.id for e in self.events.values() 
                        if e.type in event_types]
            tags = [t for t in tags if t.event_id in event_ids]
        
        if time_range:
            start_time, end_time = time_range
            tags = [t for t in tags 
                   if start_time <= t.timestamp <= end_time]
        
        return tags 