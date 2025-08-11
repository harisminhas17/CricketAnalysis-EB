import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class CommentSystem:
    def __init__(self, comments_dir: str = "data/comments"):
        self.comments_dir = comments_dir
        os.makedirs(comments_dir, exist_ok=True)
        self.comments_file = os.path.join(comments_dir, "comments.json")
        self.comments = self._load_comments()
    
    def _load_comments(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load comments from JSON file"""
        try:
            if os.path.exists(self.comments_file):
                with open(self.comments_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading comments: {str(e)}")
            return {}
    
    def _save_comments(self):
        """Save comments to JSON file"""
        try:
            with open(self.comments_file, 'w') as f:
                json.dump(self.comments, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving comments: {str(e)}")
    
    def add_comment(self, content_id: str, user_id: str, comment_text: str, 
                   content_type: str = "video") -> Dict[str, Any]:
        """Add a comment to content"""
        try:
            if content_id not in self.comments:
                self.comments[content_id] = []
            
            comment = {
                "id": len(self.comments[content_id]) + 1,
                "user_id": user_id,
                "comment": comment_text,
                "content_type": content_type,
                "created_at": datetime.now().isoformat(),
                "likes": 0,
                "replies": []
            }
            
            self.comments[content_id].append(comment)
            self._save_comments()
            logger.info(f"Added comment to {content_id}")
            return comment
        except Exception as e:
            logger.error(f"Error adding comment: {str(e)}")
            return {}
    
    def get_comments(self, content_id: str) -> List[Dict[str, Any]]:
        """Get all comments for a specific content"""
        return self.comments.get(content_id, [])
    
    def get_comment(self, content_id: str, comment_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific comment"""
        comments = self.comments.get(content_id, [])
        for comment in comments:
            if comment.get("id") == comment_id:
                return comment
        return None
    
    def update_comment(self, content_id: str, comment_id: int, 
                      user_id: str, new_text: str) -> bool:
        """Update a comment (only by the author)"""
        try:
            comments = self.comments.get(content_id, [])
            for comment in comments:
                if comment.get("id") == comment_id and comment.get("user_id") == user_id:
                    comment["comment"] = new_text
                    comment["updated_at"] = datetime.now().isoformat()
                    self._save_comments()
                    logger.info(f"Updated comment {comment_id} on {content_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating comment: {str(e)}")
            return False
    
    def delete_comment(self, content_id: str, comment_id: int, user_id: str) -> bool:
        """Delete a comment (only by the author)"""
        try:
            comments = self.comments.get(content_id, [])
            for i, comment in enumerate(comments):
                if comment.get("id") == comment_id and comment.get("user_id") == user_id:
                    comments.pop(i)
                    self._save_comments()
                    logger.info(f"Deleted comment {comment_id} from {content_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting comment: {str(e)}")
            return False
    
    def like_comment(self, content_id: str, comment_id: int) -> bool:
        """Like a comment"""
        try:
            comments = self.comments.get(content_id, [])
            for comment in comments:
                if comment.get("id") == comment_id:
                    comment["likes"] = comment.get("likes", 0) + 1
                    self._save_comments()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error liking comment: {str(e)}")
            return False
    
    def add_reply(self, content_id: str, comment_id: int, 
                  user_id: str, reply_text: str) -> bool:
        """Add a reply to a comment"""
        try:
            comments = self.comments.get(content_id, [])
            for comment in comments:
                if comment.get("id") == comment_id:
                    if "replies" not in comment:
                        comment["replies"] = []
                    
                    reply = {
                        "id": len(comment["replies"]) + 1,
                        "user_id": user_id,
                        "reply": reply_text,
                        "created_at": datetime.now().isoformat(),
                        "likes": 0
                    }
                    comment["replies"].append(reply)
                    self._save_comments()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error adding reply: {str(e)}")
            return False
    
    def like_reply(self, content_id: str, comment_id: int, reply_id: int) -> bool:
        """Like a reply"""
        try:
            comments = self.comments.get(content_id, [])
            for comment in comments:
                if comment.get("id") == comment_id:
                    replies = comment.get("replies", [])
                    for reply in replies:
                        if reply.get("id") == reply_id:
                            reply["likes"] = reply.get("likes", 0) + 1
                            self._save_comments()
                            return True
            return False
        except Exception as e:
            logger.error(f"Error liking reply: {str(e)}")
            return False
    
    def get_user_comments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all comments by a specific user"""
        user_comments = []
        for content_id, comments in self.comments.items():
            for comment in comments:
                if comment.get("user_id") == user_id:
                    comment_with_content = comment.copy()
                    comment_with_content["content_id"] = content_id
                    user_comments.append(comment_with_content)
        return user_comments
    
    def search_comments(self, query: str) -> List[Dict[str, Any]]:
        """Search comments by text"""
        try:
            query = query.lower()
            results = []
            
            for content_id, comments in self.comments.items():
                for comment in comments:
                    if query in comment.get("comment", "").lower():
                        comment_with_content = comment.copy()
                        comment_with_content["content_id"] = content_id
                        results.append(comment_with_content)
            
            return results
        except Exception as e:
            logger.error(f"Error searching comments: {str(e)}")
            return [] 