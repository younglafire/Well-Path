"""
Unit Tests for Social App

This module contains tests for the social features in the Well Path project.

What are we testing?
--------------------
1. Like Model - Tests the like functionality and constraints
2. Like/Unlike View - Tests the AJAX endpoint for liking/unliking goals

Why do we test?
---------------
Social features are important for user engagement. Testing ensures that
users can like goals correctly and that the system prevents duplicate likes.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Like
from goals.models import Goal
from taxonomy.models import Category, Unit
import json

# Get the User model
User = get_user_model()


class LikeModelTest(TestCase):
    """
    Test the Like model.
    
    What is a Like?
    ---------------
    A Like represents a user's appreciation for a goal. It's similar to
    liking a post on social media - one user can like one goal only once.
    """
    
    def setUp(self):
        """
        Set up test data.
        
        We need:
        - A test user (who will like the goal)
        - A goal owner (who created the goal)
        - A test goal (to be liked)
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.goal_owner = User.objects.create_user(
            username='goalowner',
            password='testpass123'
        )
        
        # Create test category and unit
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        # Create a test goal
        self.goal = Goal.objects.create(
            user=self.goal_owner,
            title="Run 100km",
            description="Complete 100km of running",
            category=self.category,
            unit=self.unit,
            target_value=100.0,
            is_public=True
        )
    
    def test_like_creation(self):
        """
        Test that a like is created successfully.
        
        This checks that:
        - A user can like a goal
        - The like is associated with the correct user and goal
        """
        # Create a like
        like = Like.objects.create(user=self.user, goal=self.goal)
        
        # Verify the like was created correctly
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.goal, self.goal)
        # The like should have a created_at timestamp
        self.assertIsNotNone(like.created_at)
    
    def test_like_string_representation(self):
        """
        Test the __str__() method.
        
        The string representation helps with debugging and in the Django admin.
        """
        like = Like.objects.create(user=self.user, goal=self.goal)
        
        # Should show "username liked goal_title"
        expected = f"{self.user.username} liked {self.goal.title}"
        self.assertEqual(str(like), expected)
    
    def test_like_unique_constraint(self):
        """
        Test that a user cannot like the same goal twice.
        
        Why is this important?
        ----------------------
        The database has a unique_together constraint on (user, goal).
        This prevents duplicate likes, ensuring data integrity.
        """
        # Create the first like
        Like.objects.create(user=self.user, goal=self.goal)
        
        # Try to create a duplicate like - should raise an error
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, goal=self.goal)
    
    def test_goal_likes_count(self):
        """
        Test that we can count how many likes a goal has.
        
        This uses the reverse relationship from Goal to Like.
        """
        # Create multiple likes from different users
        user2 = User.objects.create_user(username='user2', password='pass')
        user3 = User.objects.create_user(username='user3', password='pass')
        
        Like.objects.create(user=self.user, goal=self.goal)
        Like.objects.create(user=user2, goal=self.goal)
        Like.objects.create(user=user3, goal=self.goal)
        
        # The goal should have 3 likes
        self.assertEqual(self.goal.likes.count(), 3)
    
    def test_user_can_check_if_liked(self):
        """
        Test that we can check if a user has liked a specific goal.
        
        This is useful for showing different UI (filled heart vs empty heart).
        """
        # Initially, user has not liked the goal
        self.assertFalse(self.goal.is_liked_by(self.user))
        
        # After creating a like
        Like.objects.create(user=self.user, goal=self.goal)
        
        # User should have liked the goal
        self.assertTrue(self.goal.is_liked_by(self.user))


class LikeViewTest(TestCase):
    """
    Test the like/unlike view.
    
    What are we testing?
    --------------------
    The like_goal view is an AJAX endpoint that:
    1. Allows logged-in users to like a goal
    2. Allows users to unlike a goal they've already liked
    3. Returns JSON with the updated like count
    """
    
    def setUp(self):
        """
        Set up test data for view tests.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.goal_owner = User.objects.create_user(
            username='goalowner',
            password='testpass123'
        )
        
        # Create test client
        self.client = Client()
        
        # Create test category and unit
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        # Create a test goal
        self.goal = Goal.objects.create(
            user=self.goal_owner,
            title="Run 100km",
            description="Complete 100km of running",
            category=self.category,
            unit=self.unit,
            target_value=100.0,
            is_public=True
        )
    
    def test_like_requires_login(self):
        """
        Test that the like endpoint requires authentication.
        
        Anonymous users should not be able to like goals.
        """
        # Try to like without logging in
        response = self.client.post(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        
        # Should redirect to login (status code 302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_like_requires_post_method(self):
        """
        Test that the like endpoint only accepts POST requests.
        
        Why POST?
        ---------
        Liking changes data on the server, so it should use POST, not GET.
        The @require_POST decorator enforces this.
        """
        # Log in
        self.client.login(username='testuser', password='testpass123')
        
        # Try to use GET instead of POST
        response = self.client.get(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        
        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_like_goal_success(self):
        """
        Test that a user can successfully like a goal.
        """
        # Log in
        self.client.login(username='testuser', password='testpass123')
        
        # Like the goal
        response = self.client.post(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        
        # Should return success (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = response.json()
        
        # Should indicate success and that the goal is now liked
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['liked'])
        # Like count should be 1
        self.assertEqual(data['likes_count'], 1)
        
        # Verify the like was created in the database
        self.assertTrue(Like.objects.filter(user=self.user, goal=self.goal).exists())
    
    def test_unlike_goal_success(self):
        """
        Test that a user can unlike a goal they've previously liked.
        """
        # Log in
        self.client.login(username='testuser', password='testpass123')
        
        # First, create a like
        Like.objects.create(user=self.user, goal=self.goal)
        
        # Now unlike the goal (by posting again)
        response = self.client.post(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        
        # Parse JSON response
        data = response.json()
        
        # Should indicate the goal is now unliked
        self.assertEqual(data['status'], 'success')
        self.assertFalse(data['liked'])
        # Like count should be 0
        self.assertEqual(data['likes_count'], 0)
        
        # Verify the like was deleted from the database
        self.assertFalse(Like.objects.filter(user=self.user, goal=self.goal).exists())
    
    def test_like_nonexistent_goal(self):
        """
        Test that liking a non-existent goal returns a 404 error.
        """
        # Log in
        self.client.login(username='testuser', password='testpass123')
        
        # Try to like a goal that doesn't exist
        response = self.client.post(
            reverse('like_goal', kwargs={'goal_id': 99999})
        )
        
        # Should return 404 Not Found
        self.assertEqual(response.status_code, 404)
    
    def test_multiple_users_can_like_same_goal(self):
        """
        Test that multiple different users can like the same goal.
        """
        # Create another user
        user2 = User.objects.create_user(username='user2', password='pass')
        
        # First user likes the goal
        self.client.login(username='testuser', password='testpass123')
        response1 = self.client.post(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        data1 = response1.json()
        self.assertEqual(data1['likes_count'], 1)
        
        # Second user likes the same goal
        self.client.login(username='user2', password='pass')
        response2 = self.client.post(
            reverse('like_goal', kwargs={'goal_id': self.goal.id})
        )
        data2 = response2.json()
        
        # Like count should now be 2
        self.assertEqual(data2['likes_count'], 2)
