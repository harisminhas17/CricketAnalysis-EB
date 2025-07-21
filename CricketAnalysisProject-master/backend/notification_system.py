import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class NotificationSystem:
    def __init__(self, notifications_dir: str = "data/notifications"):
        self.notifications_dir = notifications_dir
        os.makedirs(notifications_dir, exist_ok=True)
        self.notifications_file = os.path.join(notifications_dir, "notifications.json")
        self.notifications = self._load_notifications()
    
    def _load_notifications(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load notifications from JSON file"""
        try:
            if os.path.exists(self.notifications_file):
                with open(self.notifications_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading notifications: {str(e)}")
            return {}
    
    def _save_notifications(self):
        """Save notifications to JSON file"""
        try:
            with open(self.notifications_file, 'w') as f:
                json.dump(self.notifications, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving notifications: {str(e)}")
    
    def create_notification(self, user_id: str, title: str, message: str, 
                           notification_type: str = "info", 
                           action_url: Optional[str] = None) -> Dict[str, Any]:
        """Create a new notification for a user"""
        try:
            if user_id not in self.notifications:
                self.notifications[user_id] = []
            
            notification = {
                "id": len(self.notifications[user_id]) + 1,
                "title": title,
                "message": message,
                "type": notification_type,
                "action_url": action_url,
                "created_at": datetime.now().isoformat(),
                "read": False,
                "dismissed": False
            }
            
            self.notifications[user_id].append(notification)
            self._save_notifications()
            logger.info(f"Created notification for user {user_id}: {title}")
            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")
            return {}
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications for a specific user"""
        user_notifications = self.notifications.get(user_id, [])
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n.get("read", False)]
        
        # Sort by creation date (newest first)
        user_notifications.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return user_notifications
    
    def mark_as_read(self, user_id: str, notification_id: int) -> bool:
        """Mark a notification as read"""
        try:
            notifications = self.notifications.get(user_id, [])
            for notification in notifications:
                if notification.get("id") == notification_id:
                    notification["read"] = True
                    self._save_notifications()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            return False
    
    def mark_all_as_read(self, user_id: str) -> bool:
        """Mark all notifications as read for a user"""
        try:
            if user_id in self.notifications:
                for notification in self.notifications[user_id]:
                    notification["read"] = True
                self._save_notifications()
                return True
            return False
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {str(e)}")
            return False
    
    def dismiss_notification(self, user_id: str, notification_id: int) -> bool:
        """Dismiss a notification"""
        try:
            notifications = self.notifications.get(user_id, [])
            for notification in notifications:
                if notification.get("id") == notification_id:
                    notification["dismissed"] = True
                    self._save_notifications()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error dismissing notification: {str(e)}")
            return False
    
    def delete_notification(self, user_id: str, notification_id: int) -> bool:
        """Delete a notification"""
        try:
            notifications = self.notifications.get(user_id, [])
            for i, notification in enumerate(notifications):
                if notification.get("id") == notification_id:
                    notifications.pop(i)
                    self._save_notifications()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting notification: {str(e)}")
            return False
    
    def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications for a user"""
        notifications = self.notifications.get(user_id, [])
        return len([n for n in notifications if not n.get("read", False)])
    
    def create_analysis_complete_notification(self, user_id: str, analysis_type: str, 
                                            result_url: Optional[str] = None) -> Dict[str, Any]:
        """Create a notification for completed analysis"""
        title = f"Analysis Complete: {analysis_type.title()}"
        message = f"Your {analysis_type} analysis has been completed successfully."
        
        return self.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type="success",
            action_url=result_url
        )
    
    def create_error_notification(self, user_id: str, error_message: str) -> Dict[str, Any]:
        """Create a notification for analysis errors"""
        title = "Analysis Error"
        message = f"An error occurred during analysis: {error_message}"
        
        return self.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type="error"
        )
    
    def create_system_notification(self, user_id: str, title: str, message: str) -> Dict[str, Any]:
        """Create a system notification"""
        return self.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type="system"
        )
    
    def cleanup_old_notifications(self, days_old: int = 30) -> int:
        """Clean up old notifications"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            deleted_count = 0
            
            for user_id, notifications in self.notifications.items():
                original_count = len(notifications)
                notifications[:] = [
                    n for n in notifications
                    if datetime.fromisoformat(n.get("created_at", "1970-01-01")).timestamp() > cutoff_date
                ]
                deleted_count += original_count - len(notifications)
            
            if deleted_count > 0:
                self._save_notifications()
                logger.info(f"Cleaned up {deleted_count} old notifications")
            
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up old notifications: {str(e)}")
            return 0 