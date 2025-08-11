import os
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Post, Comment, Like, CommentLike, Share, Follow, Notification
import config
import uuid

# Create Blueprint for social media routes
social_bp = Blueprint('social', __name__)

# JWT Secret Key (in production, use environment variable)
JWT_SECRET_KEY = 'your-secret-key-change-in-production'

def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to save profile pictures
def save_profile_picture(file):
    if file and allowed_file(file.filename):
        # Create a dedicated folder for avatars if it doesn't exist
        avatars_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
        os.makedirs(avatars_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex
        unique_filename = f"{unique_id}_{filename}"
        
        save_path = os.path.join(avatars_folder, unique_filename)
        file.save(save_path)
        
        # Return the public URL
        return f"/uploads/avatars/{unique_filename}"
    return None

def save_post_media(file):
    if file and allowed_file(file.filename):
        media_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'social')
        os.makedirs(media_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex
        unique_filename = f"{unique_id}_{filename}"
        
        save_path = os.path.join(media_folder, unique_filename)
        file.save(save_path)
        
        # Return the public URL and media type
        media_type = 'image' if filename.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'gif'] else 'video'
        return f"/uploads/social/{unique_filename}", media_type
    return None, None

def remove_media(file_path):
    if file_path:
        # Construct the full path from the root of the project
        # file_path is like '/uploads/social/filename.jpg'
        # We need to get to 'backend/uploads/social/filename.jpg'
        full_path = os.path.join(current_app.config['BASE_DIR'], file_path.lstrip('/'))
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                return True
            except Exception as e:
                current_app.logger.error(f"Error removing file {full_path}: {e}")
    return False

# Authentication Routes
@social_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Changed from get_json() to handle multipart form
        data = request.form
        
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        profile_picture_url = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            profile_picture_url = save_profile_picture(file)

        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            profile_picture=profile_picture_url, # Save the URL
            bio=data.get('bio', ''),
            location=data.get('location', ''),
            team=data.get('team', ''),
            position=data.get('position', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 500

@social_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/auth/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile"""
    return jsonify(current_user.to_dict()), 200

@social_bp.route('/auth/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    try:
        data = request.get_json()
        # Update allowed fields
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        if 'last_name' in data:
            current_user.last_name = data['last_name']
        if 'bio' in data:
            current_user.bio = data['bio']
        if 'location' in data:
            current_user.location = data['location']
        if 'team' in data:
            current_user.team = data['team']
        if 'position' in data:
            current_user.position = data['position']
        if 'password' in data and data['password']:
            current_user.set_password(data['password'])
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@social_bp.route('/auth/profile-picture', methods=['POST'])
@token_required
def upload_profile_picture(current_user):
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['profile_picture']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        profile_picture_url = save_profile_picture(file)
        if not profile_picture_url:
            return jsonify({'error': 'Invalid file type'}), 400
        current_user.profile_picture = profile_picture_url
        db.session.commit()
        return jsonify({'profile_picture': current_user.profile_picture}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Post Routes
@social_bp.route('/posts', methods=['GET'])
@token_required
def get_posts(current_user):
    """Get posts for current user's feed"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get posts from users that current user follows + public posts
        following_ids = [follow.followed_id for follow in current_user.following]
        following_ids.append(current_user.id)  # Include own posts
        
        posts = Post.query.filter(
            Post.user_id.in_(following_ids),
            Post.privacy.in_(['public', 'friends'])
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    """Create a new post"""
    try:
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        post = Post(
            user_id=current_user.id,
            content=data['content'],
            media_type=data.get('media_type'),
            media_url=data.get('media_url'),
            media_thumbnail=data.get('media_thumbnail'),
            analysis_data=data.get('analysis_data'),
            privacy=data.get('privacy', 'public')
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(current_user, post_id):
    """Get a specific post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check privacy
        if post.privacy == 'private' and post.user_id != current_user.id:
            return jsonify({'error': 'Post not found'}), 404
        
        return jsonify(post.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """Update a post, now with media support"""
    try:
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.form
        
        if 'content' in data:
            post.content = data['content']
        if 'privacy' in data:
            post.privacy = data['privacy']

        # Check for new media upload
        if 'media' in request.files:
            file = request.files['media']
            if file:
                # Remove old media if it exists
                if post.media_url:
                    remove_media(post.media_url)

                # Save new media
                media_url, media_type = save_post_media(file)
                post.media_url = media_url
                post.media_type = media_type

        # Check if client wants to remove media
        elif data.get('remove_media') == 'true':
            if post.media_url:
                remove_media(post.media_url)
                post.media_url = None
                post.media_type = None

        db.session.commit()
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Post update error: {e}")
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    """Delete a post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Comment Routes
@social_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@token_required
def get_comments(current_user, post_id):
    """Get comments for a post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check privacy
        if post.privacy == 'private' and post.user_id != current_user.id:
            return jsonify({'error': 'Post not found'}), 404
        
        comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.desc()).all()
        
        return jsonify([comment.to_dict() for comment in comments]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, post_id):
    """Create a comment on a post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check privacy
        if post.privacy == 'private' and post.user_id != current_user.id:
            return jsonify({'error': 'Post not found'}), 404
        
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            content=data['content'],
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Create notification for post author
        if post.user_id != current_user.id:
            notification = Notification(
                user_id=post.user_id,
                from_user_id=current_user.id,
                notification_type='comment',
                post_id=post_id,
                comment_id=comment.id,
                content=f"{current_user.first_name} commented on your post"
            )
            db.session.add(notification)
            db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Like Routes
@social_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(current_user, post_id):
    """Like or unlike a post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check privacy
        if post.privacy == 'private' and post.user_id != current_user.id:
            return jsonify({'error': 'Post not found'}), 404
        
        existing_like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        
        if existing_like:
            # Unlike
            db.session.delete(existing_like)
            message = 'Post unliked'
        else:
            # Like
            like = Like(post_id=post_id, user_id=current_user.id)
            db.session.add(like)
            message = 'Post liked'
            
            # Create notification for post author
            if post.user_id != current_user.id:
                notification = Notification(
                    user_id=post.user_id,
                    from_user_id=current_user.id,
                    notification_type='like',
                    post_id=post_id,
                    content=f"{current_user.first_name} liked your post"
                )
                db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@social_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
@token_required
def like_comment(current_user, comment_id):
    """Like or unlike a comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        existing_like = CommentLike.query.filter_by(comment_id=comment_id, user_id=current_user.id).first()
        
        if existing_like:
            # Unlike
            db.session.delete(existing_like)
            message = 'Comment unliked'
        else:
            # Like
            like = CommentLike(comment_id=comment_id, user_id=current_user.id)
            db.session.add(like)
            message = 'Comment liked'
        
        db.session.commit()
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Share Routes
@social_bp.route('/posts/<int:post_id>/share', methods=['POST'])
@token_required
def share_post(current_user, post_id):
    """Share a post"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check privacy
        if post.privacy == 'private' and post.user_id != current_user.id:
            return jsonify({'error': 'Post not found'}), 404
        
        data = request.get_json()
        
        share = Share(
            post_id=post_id,
            user_id=current_user.id,
            share_message=data.get('share_message', '')
        )
        
        db.session.add(share)
        db.session.commit()
        
        # Create notification for post author
        if post.user_id != current_user.id:
            notification = Notification(
                user_id=post.user_id,
                from_user_id=current_user.id,
                notification_type='share',
                post_id=post_id,
                content=f"{current_user.first_name} shared your post"
            )
            db.session.add(notification)
            db.session.commit()
        
        return jsonify({'message': 'Post shared successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Follow Routes
@social_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@token_required
def follow_user(current_user, user_id):
    """Follow or unfollow a user"""
    try:
        if current_user.id == user_id:
            return jsonify({'error': 'Cannot follow yourself'}), 400
        
        target_user = User.query.get_or_404(user_id)
        
        existing_follow = Follow.query.filter_by(
            follower_id=current_user.id, 
            followed_id=user_id
        ).first()
        
        if existing_follow:
            # Unfollow
            db.session.delete(existing_follow)
            message = f'Unfollowed {target_user.first_name}'
        else:
            # Follow
            follow = Follow(follower_id=current_user.id, followed_id=user_id)
            db.session.add(follow)
            message = f'Started following {target_user.first_name}'
            
            # Create notification
            notification = Notification(
                user_id=user_id,
                from_user_id=current_user.id,
                notification_type='follow',
                content=f"{current_user.first_name} {current_user.last_name} has started following you, follow back!"
            )
            db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({'message': message}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# User Routes
@social_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_profile(current_user, user_id):
    """Get user profile"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Check if current user is following this user
        is_following = Follow.query.filter_by(
            follower_id=current_user.id, 
            followed_id=user_id
        ).first() is not None
        
        user_data = user.to_dict()
        user_data['is_following'] = is_following
        
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/users/<int:user_id>/posts', methods=['GET'])
@token_required
def get_user_posts(current_user, user_id):
    """Get posts by a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filter posts based on privacy and relationship
        if current_user.id == user_id:
            # Own posts - show all
            posts_query = Post.query.filter_by(user_id=user_id)
        else:
            # Check if following
            is_following = Follow.query.filter_by(
                follower_id=current_user.id, 
                followed_id=user_id
            ).first() is not None
            
            if is_following:
                # Show public and friends posts
                posts_query = Post.query.filter(
                    Post.user_id == user_id,
                    Post.privacy.in_(['public', 'friends'])
                )
            else:
                # Show only public posts
                posts_query = Post.query.filter(
                    Post.user_id == user_id,
                    Post.privacy == 'public'
                )
        
        posts = posts_query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/users/<int:user_id>/following', methods=['GET'])
@token_required
def get_user_following(current_user, user_id):
    """Get the list of users this user is following"""
    try:
        user = User.query.get_or_404(user_id)
        following = [f.followed for f in user.following]
        following_data = [u.to_dict() for u in following]
        return jsonify({'following': following_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Notification Routes
@social_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications(current_user):
    """Get user notifications"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        notifications = Notification.query.filter_by(user_id=current_user.id)\
            .order_by(Notification.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'notifications': [{
                'id': n.id,
                'type': n.notification_type,
                'content': n.content,
                'from_user': n.from_user.to_dict() if n.from_user else None,
                'post_id': n.post_id,
                'comment_id': n.comment_id,
                'is_read': n.is_read,
                'created_at': n.created_at.isoformat() if n.created_at else None
            } for n in notifications.items],
            'total': notifications.total,
            'pages': notifications.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/notifications/mark-read', methods=['POST'])
@token_required
def mark_notifications_read(current_user):
    """Mark notifications as read"""
    try:
        data = request.get_json()
        notification_ids = data.get('notification_ids', [])
        
        if notification_ids:
            Notification.query.filter(
                Notification.id.in_(notification_ids),
                Notification.user_id == current_user.id
            ).update({'is_read': True}, synchronize_session=False)
        else:
            # Mark all as read
            Notification.query.filter_by(user_id=current_user.id).update({'is_read': True})
        
        db.session.commit()
        
        return jsonify({'message': 'Notifications marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Search Routes
@social_bp.route('/search/users', methods=['GET'])
@token_required
def search_users(current_user):
    """Search for users"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'users': []}), 200
        
        users = User.query.filter(
            User.username.contains(query) | 
            User.first_name.contains(query) | 
            User.last_name.contains(query)
        ).limit(10).all()
        
        return jsonify({'users': [user.to_dict() for user in users]}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/users/discover', methods=['GET'])
@token_required
def discover_users(current_user):
    """Get users to discover (not following)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get users that current user is not following
        following_ids = [follow.followed_id for follow in current_user.following]
        following_ids.append(current_user.id)  # Exclude self
        
        users = User.query.filter(
            ~User.id.in_(following_ids),
            User.is_active == True
        ).order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Add follow status to each user
        user_list = []
        for user in users.items:
            user_data = user.to_dict()
            user_data['is_following'] = False
            user_list.append(user_data)
        
        return jsonify({
            'users': user_list,
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/search/posts', methods=['GET'])
@token_required
def search_posts(current_user):
    """Search for posts"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if not query:
            return jsonify({'posts': [], 'total': 0, 'pages': 0, 'current_page': page}), 200
        
        # Search in public posts and posts from followed users
        following_ids = [follow.followed_id for follow in current_user.following]
        following_ids.append(current_user.id)
        
        posts = Post.query.filter(
            Post.content.contains(query),
            Post.user_id.in_(following_ids),
            Post.privacy.in_(['public', 'friends'])
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 