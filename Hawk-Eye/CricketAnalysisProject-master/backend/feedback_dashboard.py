import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class FeedbackDashboard:
    def __init__(self, feedback_dir: str = "data/feedback"):
        self.feedback_dir = feedback_dir
        os.makedirs(feedback_dir, exist_ok=True)
        self.feedback_file = os.path.join(feedback_dir, "feedback.json")
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            return {
                "feedback_entries": [],
                "analytics": {
                    "total_feedback": 0,
                    "average_rating": 0.0,
                    "feature_requests": [],
                    "bug_reports": []
                }
            }
        except Exception as e:
            logger.error(f"Error loading feedback: {str(e)}")
            return {
                "feedback_entries": [],
                "analytics": {
                    "total_feedback": 0,
                    "average_rating": 0.0,
                    "feature_requests": [],
                    "bug_reports": []
                }
            }
    
    def _save_feedback(self):
        try:
            with open(self.feedback_file, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving feedback: {str(e)}")
    
    def add_feedback(self, user_id: str, feedback_type: str, content: str, rating: Optional[int] = None, category: str = "general") -> Dict[str, Any]:
        try:
            feedback_entry = {
                "id": len(self.feedback_data["feedback_entries"]) + 1,
                "user_id": user_id,
                "type": feedback_type,
                "content": content,
                "rating": rating,
                "category": category,
                "created_at": datetime.now().isoformat(),
                "status": "pending",
                "response": None
            }
            self.feedback_data["feedback_entries"].append(feedback_entry)
            self._update_analytics()
            self._save_feedback()
            logger.info(f"Added feedback from user {user_id}")
            return feedback_entry
        except Exception as e:
            logger.error(f"Error adding feedback: {str(e)}")
            return {}
    
    def get_feedback(self, feedback_id: Optional[int] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        entries = self.feedback_data["feedback_entries"]
        
        if feedback_id:
            return [entry for entry in entries if entry.get("id") == feedback_id]
        
        if user_id:
            return [entry for entry in entries if entry.get("user_id") == user_id]
        
        return entries
    
    def update_feedback_status(self, feedback_id: int, status: str, response: Optional[str] = None) -> bool:
        try:
            for entry in self.feedback_data["feedback_entries"]:
                if entry.get("id") == feedback_id:
                    entry["status"] = status
                    if response:
                        entry["response"] = response
                        entry["responded_at"] = datetime.now().isoformat()
                    self._save_feedback()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating feedback status: {str(e)}")
            return False
    
    def add_feature_request(self, user_id: str, title: str, description: str, priority: str = "medium") -> Dict[str, Any]:
        try:
            feature_request = {
                "id": len(self.feedback_data["analytics"]["feature_requests"]) + 1,
                "user_id": user_id,
                "title": title,
                "description": description,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "status": "pending",
                "votes": 0
            }
            self.feedback_data["analytics"]["feature_requests"].append(feature_request)
            self._save_feedback()
            logger.info(f"Added feature request: {title}")
            return feature_request
        except Exception as e:
            logger.error(f"Error adding feature request: {str(e)}")
            return {}
    
    def add_bug_report(self, user_id: str, title: str, description: str, severity: str = "medium", steps_to_reproduce: str = "") -> Dict[str, Any]:
        try:
            bug_report = {
                "id": len(self.feedback_data["analytics"]["bug_reports"]) + 1,
                "user_id": user_id,
                "title": title,
                "description": description,
                "severity": severity,
                "steps_to_reproduce": steps_to_reproduce,
                "created_at": datetime.now().isoformat(),
                "status": "open"
            }
            self.feedback_data["analytics"]["bug_reports"].append(bug_report)
            self._save_feedback()
            logger.info(f"Added bug report: {title}")
            return bug_report
        except Exception as e:
            logger.error(f"Error adding bug report: {str(e)}")
            return {}
    
    def vote_feature_request(self, feature_id: int) -> bool:
        try:
            for feature in self.feedback_data["analytics"]["feature_requests"]:
                if feature.get("id") == feature_id:
                    feature["votes"] = feature.get("votes", 0) + 1
                    self._save_feedback()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error voting for feature request: {str(e)}")
            return False
    
    def get_analytics(self) -> Dict[str, Any]:
        return self.feedback_data["analytics"]
    
    def _update_analytics(self):
        try:
            entries = self.feedback_data["feedback_entries"]
            self.feedback_data["analytics"]["total_feedback"] = len(entries)
            
            ratings = [entry.get("rating") for entry in entries if entry.get("rating") is not None]
            if ratings:
                self.feedback_data["analytics"]["average_rating"] = sum(ratings) / len(ratings)
            else:
                self.feedback_data["analytics"]["average_rating"] = 0.0
        except Exception as e:
            logger.error(f"Error updating analytics: {str(e)}")
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        try:
            entries = self.feedback_data["feedback_entries"]
            
            type_counts = {}
            for entry in entries:
                feedback_type = entry.get("type", "unknown")
                type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
            
            status_counts = {}
            for entry in entries:
                status = entry.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            category_counts = {}
            for entry in entries:
                category = entry.get("category", "general")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                "total_entries": len(entries),
                "type_distribution": type_counts,
                "status_distribution": status_counts,
                "category_distribution": category_counts,
                "average_rating": self.feedback_data["analytics"]["average_rating"],
                "feature_requests_count": len(self.feedback_data["analytics"]["feature_requests"]),
                "bug_reports_count": len(self.feedback_data["analytics"]["bug_reports"])
            }
        except Exception as e:
            logger.error(f"Error generating feedback summary: {str(e)}")
            return {}
    
    def search_feedback(self, query: str) -> List[Dict[str, Any]]:
        try:
            query = query.lower()
            results = []
            
            for entry in self.feedback_data["feedback_entries"]:
                if (query in entry.get("content", "").lower() or 
                    query in entry.get("category", "").lower()):
                    results.append(entry)
            
            return results
        except Exception as e:
            logger.error(f"Error searching feedback: {str(e)}")
            return []
 