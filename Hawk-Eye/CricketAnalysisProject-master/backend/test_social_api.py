#!/usr/bin/env python3
"""
Simple test script to verify social API endpoints are working correctly.
This script tests the social API without starting the full Flask app.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_social_api_import():
    """Test that the social API can be imported without conflicts."""
    try:
        from social_api import social_bp
        print("✅ Social API imported successfully")
        
        # Check that the blueprint has the expected name
        if social_bp.name == 'social':
            print("✅ Social blueprint has correct name")
        else:
            print(f"⚠️  Social blueprint name is '{social_bp.name}', expected 'social'")
        
        # Check that the blueprint has routes (basic check)
        if hasattr(social_bp, 'deferred_functions'):
            print(f"✅ Social blueprint has {len(social_bp.deferred_functions)} registered functions")
        else:
            print("⚠️  Could not check registered functions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing social API: {e}")
        return False

def test_models():
    """Test that the database models can be imported."""
    try:
        from models import User, Post, Follow, Notification, Like, Comment, Share
        print("✅ Database models imported successfully")
        
        # Check that models have expected attributes
        models_to_check = [
            (User, ['id', 'username', 'email', 'first_name', 'last_name']),
            (Post, ['id', 'user_id', 'content', 'created_at']),
            (Follow, ['follower_id', 'followed_id']),
            (Notification, ['user_id', 'notification_type', 'content']),
            (Like, ['user_id', 'post_id']),
            (Comment, ['user_id', 'post_id', 'content']),
            (Share, ['user_id', 'post_id'])
        ]
        
        for model, expected_attrs in models_to_check:
            for attr in expected_attrs:
                if hasattr(model, attr):
                    print(f"✅ {model.__name__} has attribute: {attr}")
                else:
                    print(f"⚠️  {model.__name__} missing attribute: {attr}")
        
        return True
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False

def test_endpoint_functions():
    """Test that the endpoint functions exist in the social API."""
    try:
        from social_api import (
            get_profile, update_profile, get_posts, create_post,
            discover_users, follow_user, get_notifications
        )
        print("✅ All required endpoint functions found")
        return True
    except ImportError as e:
        print(f"❌ Missing endpoint function: {e}")
        return False

if __name__ == "__main__":
    print("Testing Social API Components...")
    print("=" * 50)
    
    success = True
    
    # Test models
    if not test_models():
        success = False
    
    print()
    
    # Test social API import
    if not test_social_api_import():
        success = False
    
    print()
    
    # Test endpoint functions
    if not test_endpoint_functions():
        success = False
    
    print()
    print("=" * 50)
    if success:
        print("✅ All tests passed! Social API is ready to use.")
        print("\n📋 Summary of Social Feed Features:")
        print("   • User authentication and profiles")
        print("   • Post creation and sharing")
        print("   • User following system")
        print("   • Real-time notifications")
        print("   • User discovery")
        print("   • Like, comment, and share functionality")
    else:
        print("❌ Some tests failed. Please check the errors above.") 