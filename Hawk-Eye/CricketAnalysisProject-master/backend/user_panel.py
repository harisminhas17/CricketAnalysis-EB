import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class UserPanel:
    def __init__(self, users_dir: str = "data/users"):
        self.users_dir = users_dir
        os.makedirs(users_dir, exist_ok=True)
        self.users_file = os.path.join(users_dir, "users.json")
        self.users = self._load_users()
    
    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading users: {str(e)}")
            return {}
    
    def _save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving users: {str(e)}")
    
    def create_user(self, user_id: str, username: str, email: str, profile_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            user = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "profile": profile_data or {},
                "settings": {
                    "notifications_enabled": True,
                    "auto_save": True,
                    "theme": "light",
                    "language": "en"
                },
                "stats": {
                    "total_analyses": 0,
                    "total_videos": 0,
                    "favorite_shots": [],
                    "achievements": []
                }
            }
            self.users[user_id] = user
            self._save_users()
            logger.info(f"Created user profile: {username}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return {}
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                self.users[user_id].update(updates)
                self.users[user_id]["updated_at"] = datetime.now().isoformat()
                self._save_users()
                logger.info(f"Updated user profile: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return False
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                if "profile" not in self.users[user_id]:
                    self.users[user_id]["profile"] = {}
                self.users[user_id]["profile"].update(profile_data)
                self.users[user_id]["updated_at"] = datetime.now().isoformat()
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return False
    
    def update_settings(self, user_id: str, settings: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                if "settings" not in self.users[user_id]:
                    self.users[user_id]["settings"] = {}
                self.users[user_id]["settings"].update(settings)
                self.users[user_id]["updated_at"] = datetime.now().isoformat()
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating settings: {str(e)}")
            return False
    
    def update_stats(self, user_id: str, stats_updates: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                if "stats" not in self.users[user_id]:
                    self.users[user_id]["stats"] = {}
                self.users[user_id]["stats"].update(stats_updates)
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating stats: {str(e)}")
            return False
    
    def increment_analysis_count(self, user_id: str) -> bool:
        try:
            if user_id in self.users:
                if "stats" not in self.users[user_id]:
                    self.users[user_id]["stats"] = {}
                if "total_analyses" not in self.users[user_id]["stats"]:
                    self.users[user_id]["stats"]["total_analyses"] = 0
                self.users[user_id]["stats"]["total_analyses"] += 1
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error incrementing analysis count: {str(e)}")
            return False
    
    def add_favorite_shot(self, user_id: str, shot_data: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                if "stats" not in self.users[user_id]:
                    self.users[user_id]["stats"] = {}
                if "favorite_shots" not in self.users[user_id]["stats"]:
                    self.users[user_id]["stats"]["favorite_shots"] = []
                shot_data["added_at"] = datetime.now().isoformat()
                self.users[user_id]["stats"]["favorite_shots"].append(shot_data)
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding favorite shot: {str(e)}")
            return False
    
    def remove_favorite_shot(self, user_id: str, shot_id: str) -> bool:
        try:
            if user_id in self.users:
                stats = self.users[user_id].get("stats", {})
                favorite_shots = stats.get("favorite_shots", [])
                favorite_shots[:] = [shot for shot in favorite_shots if shot.get("id") != shot_id]
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing favorite shot: {str(e)}")
            return False
    
    def add_achievement(self, user_id: str, achievement: Dict[str, Any]) -> bool:
        try:
            if user_id in self.users:
                if "stats" not in self.users[user_id]:
                    self.users[user_id]["stats"] = {}
                if "achievements" not in self.users[user_id]["stats"]:
                    self.users[user_id]["stats"]["achievements"] = []
                achievement["earned_at"] = datetime.now().isoformat()
                self.users[user_id]["stats"]["achievements"].append(achievement)
                self._save_users()
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding achievement: {str(e)}")
            return False
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        user = self.users.get(user_id)
        if user:
            return user.get("stats", {})
        return {}
    
    def get_user_settings(self, user_id: str) -> Dict[str, Any]:
        user = self.users.get(user_id)
        if user:
            return user.get("settings", {})
        return {}
    
    def delete_user(self, user_id: str) -> bool:
        try:
            if user_id in self.users:
                del self.users[user_id]
                self._save_users()
                logger.info(f"Deleted user profile: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return False
    
    def list_users(self) -> List[str]:
        return list(self.users.keys())
