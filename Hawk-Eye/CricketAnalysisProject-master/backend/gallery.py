import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

class GalleryManager:
    def __init__(self, gallery_dir: str = "data/gallery"):
        self.gallery_dir = gallery_dir
        os.makedirs(gallery_dir, exist_ok=True)
        self.items_file = os.path.join(gallery_dir, "items.json")
        self.items = self._load_items()
    
    def _load_items(self) -> List[Dict[str, Any]]:
        """Load gallery items from JSON file"""
        try:
            if os.path.exists(self.items_file):
                with open(self.items_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading gallery items: {str(e)}")
            return []
    
    def _save_items(self):
        """Save gallery items to JSON file"""
        try:
            with open(self.items_file, 'w') as f:
                json.dump(self.items, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving gallery items: {str(e)}")
    
    def add_item(self, user_id: str, title: str, description: str, 
                 file_path: str, item_type: str = "video") -> Dict[str, Any]:
        """Add a new item to the gallery"""
        try:
            item = {
                "id": len(self.items) + 1,
                "user_id": user_id,
                "title": title,
                "description": description,
                "file_path": file_path,
                "type": item_type,
                "created_at": datetime.now().isoformat(),
                "likes": 0,
                "comments": []
            }
            
            self.items.append(item)
            self._save_items()
            logger.info(f"Added gallery item: {title}")
            return item
        except Exception as e:
            logger.error(f"Error adding gallery item: {str(e)}")
            return {}
    
    def get_items(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get gallery items, optionally filtered by user"""
        if user_id:
            return [item for item in self.items if item.get("user_id") == user_id]
        return self.items
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific gallery item by ID"""
        for item in self.items:
            if item.get("id") == item_id:
                return item
        return None
    
    def update_item(self, item_id: int, updates: Dict[str, Any]) -> bool:
        """Update a gallery item"""
        try:
            for item in self.items:
                if item.get("id") == item_id:
                    item.update(updates)
                    item["updated_at"] = datetime.now().isoformat()
                    self._save_items()
                    logger.info(f"Updated gallery item: {item_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating gallery item: {str(e)}")
            return False
    
    def delete_item(self, item_id: int) -> bool:
        """Delete a gallery item"""
        try:
            for i, item in enumerate(self.items):
                if item.get("id") == item_id:
                    # Remove the item
                    deleted_item = self.items.pop(i)
                    
                    # Delete the associated file
                    file_path = deleted_item.get("file_path")
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                    
                    self._save_items()
                    logger.info(f"Deleted gallery item: {item_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting gallery item: {str(e)}")
            return False
    
    def like_item(self, item_id: int) -> bool:
        """Like a gallery item"""
        try:
            for item in self.items:
                if item.get("id") == item_id:
                    item["likes"] = item.get("likes", 0) + 1
                    self._save_items()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error liking gallery item: {str(e)}")
            return False
    
    def add_comment(self, item_id: int, user_id: str, comment: str) -> bool:
        """Add a comment to a gallery item"""
        try:
            for item in self.items:
                if item.get("id") == item_id:
                    if "comments" not in item:
                        item["comments"] = []
                    
                    comment_obj = {
                        "id": len(item["comments"]) + 1,
                        "user_id": user_id,
                        "comment": comment,
                        "created_at": datetime.now().isoformat()
                    }
                    item["comments"].append(comment_obj)
                    self._save_items()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error adding comment: {str(e)}")
            return False 