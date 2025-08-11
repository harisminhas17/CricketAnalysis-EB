import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SocialFeed:
    def __init__(self, feed_dir: str = "data/social"):
        self.feed_dir = feed_dir
        os.makedirs(feed_dir, exist_ok=True)
        self.feed_file = os.path.join(feed_dir, "feed.json")
        self.posts = self._load_posts()
    
    def _load_posts(self) -> List[Dict[str, Any]]:
        """Load social feed posts from JSON file"""
        try:
            if os.path.exists(self.feed_file):
                with open(self.feed_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading social feed: {str(e)}")
            return []
    
    def _save_posts(self):
        """Save social feed posts to JSON file"""
        try:
            with open(self.feed_file, 'w') as f:
                json.dump(self.posts, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving social feed: {str(e)}")
    
    def create_post(self, user_id: str, content: str, media_url: Optional[str] = None,
                   post_type: str = "analysis") -> Dict[str, Any]:
        """Create a new social media post"""
        try:
            post = {
                "id": len(self.posts) + 1,
                "user_id": user_id,
                "content": content,
                "media_url": media_url,
                "type": post_type,
                "created_at": datetime.now().isoformat(),
                "likes": 0,
                "shares": 0,
                "comments": [],
                "tags": []
            }
            
            self.posts.append(post)
            self._save_posts()
            logger.info(f"Created social post: {content[:50]}...")
            return post
        except Exception as e:
            logger.error(f"Error creating social post: {str(e)}")
            return {}
    
    def get_feed(self, user_id: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get social feed posts, optionally filtered by user"""
        posts = self.posts.copy()
        
        # Sort by creation date (newest first)
        posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        # Filter by user if specified
        if user_id:
            posts = [post for post in posts if post.get("user_id") == user_id]
        
        # Limit results
        return posts[:limit]
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific post by ID"""
        for post in self.posts:
            if post.get("id") == post_id:
                return post
        return None
    
    def like_post(self, post_id: int) -> bool:
        """Like a social post"""
        try:
            for post in self.posts:
                if post.get("id") == post_id:
                    post["likes"] = post.get("likes", 0) + 1
                    self._save_posts()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error liking post: {str(e)}")
            return False
    
    def share_post(self, post_id: int) -> bool:
        """Share a social post"""
        try:
            for post in self.posts:
                if post.get("id") == post_id:
                    post["shares"] = post.get("shares", 0) + 1
                    self._save_posts()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error sharing post: {str(e)}")
            return False
    
    def add_comment(self, post_id: int, user_id: str, comment: str) -> bool:
        """Add a comment to a social post"""
        try:
            for post in self.posts:
                if post.get("id") == post_id:
                    if "comments" not in post:
                        post["comments"] = []
                    
                    comment_obj = {
                        "id": len(post["comments"]) + 1,
                        "user_id": user_id,
                        "comment": comment,
                        "created_at": datetime.now().isoformat()
                    }
                    post["comments"].append(comment_obj)
                    self._save_posts()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error adding comment: {str(e)}")
            return False
    
    def delete_post(self, post_id: int, user_id: str) -> bool:
        """Delete a social post (only by the author)"""
        try:
            for i, post in enumerate(self.posts):
                if post.get("id") == post_id and post.get("user_id") == user_id:
                    self.posts.pop(i)
                    self._save_posts()
                    logger.info(f"Deleted social post: {post_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting post: {str(e)}")
            return False
    
    def add_tag(self, post_id: int, tag: str) -> bool:
        """Add a tag to a social post"""
        try:
            for post in self.posts:
                if post.get("id") == post_id:
                    if "tags" not in post:
                        post["tags"] = []
                    if tag not in post["tags"]:
                        post["tags"].append(tag)
                        self._save_posts()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error adding tag: {str(e)}")
            return False
    
    def search_posts(self, query: str) -> List[Dict[str, Any]]:
        """Search posts by content or tags"""
        try:
            query = query.lower()
            results = []
            
            for post in self.posts:
                # Search in content
                if query in post.get("content", "").lower():
                    results.append(post)
                    continue
                
                # Search in tags
                tags = post.get("tags", [])
                if any(query in tag.lower() for tag in tags):
                    results.append(post)
                    continue
            
            return results
        except Exception as e:
            logger.error(f"Error searching posts: {str(e)}")
            return [] 