import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
import requests
from dataclasses import dataclass
from PIL import Image
import io
import cv2
import uuid
import tweepy
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging
import base64
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Instagram API, but make it optional
try:
    from instagram_private_api import Client, ClientError
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False
    logger.warning("Instagram API not available. Social sharing to Instagram will be disabled.")

# Handle missing imghdr module in Python 3.13+
try:
    import imghdr
except ImportError:
    # Fallback for Python 3.13+ where imghdr was removed
    def imghdr_what(file, h=None):
        """Simple fallback for imghdr.what()"""
        if h is None:
            if hasattr(file, 'read'):
                h = file.read(32)
                file.seek(0)
            else:
                return None
        
        if h.startswith(b'\xff\xd8'):
            return 'jpeg'
        elif h.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        elif h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
            return 'gif'
        elif h.startswith(b'RIFF') and h[8:12] == b'WEBP':
            return 'webp'
        return None
    
    class imghdr:
        @staticmethod
        def what(file, h=None):
            return imghdr_what(file, h)

@dataclass
class GalleryItem:
    id: str
    type: str
    file_path: str
    title: str
    description: str
    tags: List[str]
    metadata: Dict[str, Any]
    subtype: str = ''
    created_at: datetime = None
    user_id: str = ''

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class SocialSharing:
    def __init__(self, data_dir: str = "data/social"):
        self.data_dir = data_dir
        self._ensure_data_directory()
        self.instagram_client = None
        self._load_config()
        
        # Load API credentials
        self.load_credentials()
        
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_config(self):
        """Load social media configuration."""
        config_path = os.path.join(self.data_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'instagram': {
                    'username': '',
                    'password': '',
                    'enabled': False
                }
            }
            self._save_config()
    
    def _save_config(self):
        """Save social media configuration."""
        config_path = os.path.join(self.data_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def configure_instagram(self, username: str, password: str, enable: bool = True):
        """Configure Instagram credentials."""
        if not INSTAGRAM_AVAILABLE:
            raise ImportError("Instagram API is not available. Please install instagram-private-api package.")
        
        self.config['instagram'].update({
            'username': username,
            'password': password,
            'enabled': enable
        })
        self._save_config()
        
        if enable:
            self._initialize_instagram()
    
    def _initialize_instagram(self):
        """Initialize Instagram client."""
        if not INSTAGRAM_AVAILABLE:
            return
        
        try:
            if self.config['instagram']['enabled']:
                self.instagram_client = Client(
                    self.config['instagram']['username'],
                    self.config['instagram']['password']
                )
        except Exception as e:
            logger.error(f"Failed to initialize Instagram client: {str(e)}")
            self.instagram_client = None
    
    def load_credentials(self):
        """Load API credentials from config files"""
        try:
            # Twitter credentials
            with open(os.path.join(self.data_dir, 'twitter.json'), 'r') as f:
                twitter_config = json.load(f)
                self.twitter_auth = tweepy.OAuthHandler(
                    twitter_config['api_key'],
                    twitter_config['api_secret']
                )
                self.twitter_auth.set_access_token(
                    twitter_config['access_token'],
                    twitter_config['access_token_secret']
                )
                self.twitter_api = tweepy.API(self.twitter_auth)
            
            # YouTube credentials
            self.youtube_credentials = None
            if os.path.exists(os.path.join(self.data_dir, 'youtube_token.json')):
                with open(os.path.join(self.data_dir, 'youtube_token.json'), 'r') as f:
                    self.youtube_credentials = Credentials.from_authorized_user_info(
                        json.load(f)
                    )
            
        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            raise
        
    def generate_thumbnail(self, video_path: str, timestamp: float = 0) -> str:
        """Generate thumbnail from video at specified timestamp"""
        try:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Convert to PIL Image
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
                # Resize for thumbnail
                image.thumbnail((320, 180))
                
                # Save thumbnail
                thumbnail_path = os.path.join(self.data_dir, f"thumbnails/{os.path.basename(video_path)}.jpg")
                image.save(thumbnail_path, format='JPEG')
                
                return thumbnail_path
            return None
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            raise
        
    def save_to_gallery(self, user_id: str, item_type: str, file_path: str, 
                       title: str, description: str, tags: List[str], 
                       metadata: Dict) -> GalleryItem:
        """Save item to user's gallery"""
        try:
            # Generate unique ID
            item_id = str(uuid.uuid4())
            
            # Create user directory if it doesn't exist
            user_dir = os.path.join(self.data_dir, user_id)
            os.makedirs(user_dir, exist_ok=True)
            
            # Generate thumbnail for videos
            thumbnail_path = None
            if item_type == 'video':
                thumbnail_path = self.generate_thumbnail(file_path)
                
            # Copy file to gallery
            gallery_path = os.path.join(user_dir, f"{item_id}_{os.path.basename(file_path)}")
            if os.path.exists(file_path):
                with open(file_path, 'rb') as src, open(gallery_path, 'wb') as dst:
                    dst.write(src.read())
            
            # Create gallery item
            item = GalleryItem(
                id=item_id,
                user_id=user_id,
                type=item_type,
                title=title,
                description=description,
                file_path=gallery_path,
                thumbnail_path=thumbnail_path,
                created_at=datetime.now(),
                tags=tags,
                metadata=metadata
            )
            
            # Save metadata to JSON file
            metadata_path = os.path.join(user_dir, f"{item_id}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump({
                    'id': item.id,
                    'user_id': item.user_id,
                    'type': item.type,
                    'title': item.title,
                    'description': item.description,
                    'file_path': item.file_path.replace('\\', '/'),
                    'thumbnail_path': item.thumbnail_path.replace('\\', '/') if item.thumbnail_path else None,
                    'created_at': item.created_at.isoformat(),
                    'tags': item.tags,
                    'metadata': item.metadata
                }, f, indent=2)
            
            return item
        except Exception as e:
            logger.error(f"Error saving to gallery: {str(e)}")
            raise
        
    def get_gallery_items(self, user_id: str, item_type: Optional[str] = None,
                         tags: Optional[List[str]] = None) -> List[GalleryItem]:
        """Get items from user's gallery with optional filtering"""
        try:
            user_dir = os.path.join(self.data_dir, user_id)
            if not os.path.exists(user_dir):
                return []
                
            items = []
            for filename in os.listdir(user_dir):
                if filename.endswith('_metadata.json'):
                    with open(os.path.join(user_dir, filename), 'r') as f:
                        item_data = json.load(f)
                        
                    # Apply filters
                    if item_type and item_data['type'] != item_type:
                        continue
                    if tags and not all(tag in item_data['tags'] for tag in tags):
                        continue
                        
                    # Convert ISO format string back to datetime
                    item_data['created_at'] = datetime.fromisoformat(item_data['created_at'])
                    
                    # Normalize file paths for web compatibility
                    if 'file_path' in item_data:
                        item_data['file_path'] = item_data['file_path'].replace('\\', '/')
                    if 'thumbnail_path' in item_data and item_data['thumbnail_path']:
                        item_data['thumbnail_path'] = item_data['thumbnail_path'].replace('\\', '/')
                    
                    items.append(GalleryItem(**item_data))
                    
            return sorted(items, key=lambda x: x.created_at, reverse=True)
        except Exception as e:
            logger.error(f"Error getting gallery items: {str(e)}")
            raise
            
    def share_to_twitter(self, item: GalleryItem, message: str) -> bool:
        """Share item to Twitter"""
        try:
            if not self.twitter_api:
                raise Exception("Twitter API not initialized")
                
            # Prepare media
            media_ids = []
            if item.thumbnail_path:
                media = self.twitter_api.media_upload(item.thumbnail_path)
                media_ids.append(media.media_id)
            
            # Post tweet with media
            self.twitter_api.update_status(
                status=message,
                media_ids=media_ids
            )
            
            logger.info(f"Successfully shared to Twitter: {item.id}")
            return True
        except Exception as e:
            logger.error(f"Error sharing to Twitter: {str(e)}")
            raise
            
    def share_to_instagram(self, item: GalleryItem, caption: str) -> bool:
        """Share item to Instagram"""
        try:
            if not self.instagram_client:
                raise Exception("Instagram API not initialized")
                
            if item.type == 'video':
                # Upload video
                self.instagram_client.post_video(
                    item.file_path,
                    caption=caption
                )
            else:
                # Upload photo
                self.instagram_client.post_photo(
                    item.file_path,
                    caption=caption
                )
            
            logger.info(f"Successfully shared to Instagram: {item.id}")
            return True
        except Exception as e:
            logger.error(f"Error sharing to Instagram: {str(e)}")
            raise
            
    def share_to_youtube(self, item: GalleryItem, title: str, description: str,
                        tags: List[str]) -> bool:
        """Share item to YouTube"""
        try:
            if not self.youtube_credentials:
                raise Exception("YouTube credentials not initialized")
                
            youtube = build('youtube', 'v3', credentials=self.youtube_credentials)
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': '17'  # Sports category
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                item.file_path,
                mimetype='video/mp4',
                resumable=True
            )
            
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = request.execute()
            
            logger.info(f"Successfully shared to YouTube: {item.id}")
            return True
        except Exception as e:
            logger.error(f"Error sharing to YouTube: {str(e)}")
            raise

    def share_content(self, content_type: str, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Share content to social media platforms."""
        try:
            # Save content metadata
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            metadata = {
                'type': content_type,
                'timestamp': timestamp,
                'data': content_data
            }
            
            metadata_path = os.path.join(self.data_dir, f'{timestamp}_{content_type}.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            # Handle different content types
            if content_type == 'image':
                return self._handle_image_sharing(content_data)
            elif content_type == 'video':
                return self._handle_video_sharing(content_data)
            elif content_type == 'analysis':
                return self._handle_analysis_sharing(content_data)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported content type: {content_type}'
                }
                
        except Exception as e:
            logger.error(f"Error in share_content: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_image_sharing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle image sharing."""
        try:
            # Save image
            image_data = base64.b64decode(data['image'])
            image = Image.open(io.BytesIO(image_data))
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = os.path.join(self.data_dir, f'{timestamp}_image.jpg')
            image.save(image_path)
            
            # Share to Instagram if enabled
            if self.config['instagram']['enabled']:
                return self.share_to_instagram(item=self.save_to_gallery(user_id='', item_type='', file_path=image_path, title='', description='', tags=[], metadata={}), caption=data.get('caption', ''))
            
            return {
                'success': True,
                'message': 'Image saved successfully',
                'path': image_path
            }
            
        except Exception as e:
            logger.error(f"Error in _handle_image_sharing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_video_sharing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle video sharing."""
        try:
            # Save video
            video_data = base64.b64decode(data['video'])
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_path = os.path.join(self.data_dir, f'{timestamp}_video.mp4')
            
            with open(video_path, 'wb') as f:
                f.write(video_data)
            
            return {
                'success': True,
                'message': 'Video saved successfully',
                'path': video_path
            }
            
        except Exception as e:
            logger.error(f"Error in _handle_video_sharing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_analysis_sharing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analysis sharing."""
        try:
            # Save analysis data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            analysis_path = os.path.join(self.data_dir, f'{timestamp}_analysis.json')
            
            with open(analysis_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return {
                'success': True,
                'message': 'Analysis saved successfully',
                'path': analysis_path
            }
            
        except Exception as e:
            logger.error(f"Error in _handle_analysis_sharing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 

try:
    import tweepy
    TWITTER_AVAILABLE = True
    # Patch tweepy.api.imghdr if missing (Python 3.13+)
    import sys
    if sys.version_info >= (3, 13):
        import types
        def imghdr_what(file, h=None):
            if h is None:
                if hasattr(file, 'read'):
                    h = file.read(32)
                    file.seek(0)
                else:
                    return None
            if h.startswith(b'\xff\xd8'):
                return 'jpeg'
            elif h.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            elif h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
                return 'gif'
            elif h.startswith(b'RIFF') and h[8:12] == b'WEBP':
                return 'webp'
            return None
        tweepy.api.imghdr = types.SimpleNamespace(what=imghdr_what)
except ImportError:
    TWITTER_AVAILABLE = False
    logging.warning("Twitter integration not available - tweepy not installed") 