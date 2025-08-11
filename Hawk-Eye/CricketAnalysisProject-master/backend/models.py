from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    analysis_data = db.Column(db.JSON)
    annotations = db.Column(db.JSON)

    def __repr__(self):
        return f'<Video {self.filename}>'

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    drills = db.Column(db.JSON)
    tags = db.Column(db.JSON)
    metrics = db.Column(db.JSON)

class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # video, screenshot, analysis
    file_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255))
    item_metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shared = db.Column(db.Boolean, default=False)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50))
    port = db.Column(db.Integer)
    position = db.Column(db.JSON)  # x, y, z coordinates
    rotation = db.Column(db.JSON)  # rotation angles
    calibration_data = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)

class TrackingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    camera_ids = db.Column(db.JSON)  # List of camera IDs used
    trajectory_data = db.Column(db.JSON)
    metrics = db.Column(db.JSON)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    location = db.Column(db.String(100))
    team = db.Column(db.String(100))
    position = db.Column(db.String(50))  # batsman, bowler, all-rounder, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    shares = db.relationship('Share', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Followers and following
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy=True)
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_picture': self.profile_picture,
            'bio': self.bio,
            'location': self.location,
            'team': self.team,
            'position': self.position,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'follower_count': len(self.followers),
            'following_count': len(self.following)
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_type = db.Column(db.String(20))  # image, video, analysis, highlight
    media_url = db.Column(db.String(255))
    media_thumbnail = db.Column(db.String(255))
    analysis_data = db.Column(db.JSON)  # For cricket analysis posts
    privacy = db.Column(db.String(20), default='public')  # public, friends, private
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    shares = db.relationship('Share', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'media_type': self.media_type,
            'media_url': self.media_url,
            'media_thumbnail': self.media_thumbnail,
            'created_at': self.created_at.isoformat(),
            'analysis_data': self.analysis_data,
            'privacy': self.privacy,
            'author': self.author.to_dict(),
            'likes': [like.to_dict() for like in self.likes],
            'comments': [comment.to_dict() for comment in self.comments if not comment.parent_id],
            'shares': self.shares
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # For nested comments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    likes = db.relationship('CommentLike', backref='comment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': self.author.to_dict(),
            'content': self.content,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'like_count': len(self.likes),
            'reply_count': len(self.replies),
            'likes': [like.to_dict() for like in self.likes]
        }

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id
        }

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('comment_id', 'user_id', name='unique_comment_like'),)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'comment_id': self.comment_.id
        }

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_message = db.Column(db.Text)  # Optional message when sharing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_type = db.Column(db.String(50), nullable=False)  # like, comment, share, follow, mention
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    from_user = db.relationship('User', foreign_keys=[from_user_id])
    post = db.relationship('Post')
    comment = db.relationship('Comment')
