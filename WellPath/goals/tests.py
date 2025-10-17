"""
Unit Tests for Goals App - Part 1: Models, Services, and Forms

This module contains comprehensive tests for the goals application, which is
the core of the Well Path project. It handles goal creation, tracking, and management.

What are we testing?
--------------------
1. Models - User, Goal, Progress, ProgressPhoto
2. Services - Business logic for goal calculations and filtering
3. Forms - User registration, goal creation and editing

Why comprehensive testing is important?
---------------------------------------
The goals app is the heart of this application. Testing it thoroughly ensures
that users can reliably create goals, track progress, and manage their data
without encountering bugs or data loss.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from decimal import Decimal
from .models import Goal, Progress, ProgressPhoto
from .services import (
    goal_is_completed, goal_is_overdue, goal_get_status,
    goal_progress_percentage, progress_create_or_update,
    progress_check_goal_completion, goal_list_for_user,
    goal_list_public, dashboard_get_category_stats
)
from .forms import CustomUserCreationForm, GoalForm, GoalEditForm
from taxonomy.models import Category, Unit

# Get the User model
User = get_user_model()


# =============================================================================
# MODEL TESTS
# =============================================================================

class UserModelTest(TestCase):
    """
    Test the custom User model.
    
    What is the User model?
    -----------------------
    The User model extends Django's AbstractUser. It represents a person
    who uses the application.
    """
    
    def test_user_creation(self):
        """
        Test that a user can be created successfully.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        # Password should be hashed, not stored as plain text
        self.assertNotEqual(user.password, 'testpass123')
        # User should be active by default
        self.assertTrue(user.is_active)
    
    def test_user_string_representation(self):
        """
        Test that the user's username is returned as the string representation.
        """
        user = User.objects.create_user(username='testuser', password='pass')
        # The default __str__ for AbstractUser returns the username
        self.assertEqual(str(user), 'testuser')


class GoalModelTest(TestCase):
    """
    Test the Goal model.
    
    What is a Goal?
    ---------------
    A Goal represents something a user wants to achieve (e.g., "Run 100km").
    It has a title, description, target value, optional deadline, and can be
    public or private.
    """
    
    def setUp(self):
        """
        Set up test data.
        
        We need:
        - A test user
        - A category and unit
        - Test goals
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        # Create a goal with a deadline
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 100km",
            description="Complete 100km of running",
            category=self.category,
            unit=self.unit,
            target_value=100.0,
            deadline=date.today() + timedelta(days=30),
            is_public=True
        )
    
    def test_goal_creation(self):
        """
        Test that a goal is created successfully with all fields.
        """
        self.assertEqual(self.goal.title, "Run 100km")
        self.assertEqual(self.goal.user, self.user)
        self.assertEqual(self.goal.target_value, 100.0)
        self.assertTrue(self.goal.is_public)
        self.assertIsNotNone(self.goal.created_at)
    
    def test_goal_string_representation(self):
        """
        Test the __str__() method shows the goal title and username.
        """
        expected = f"Goal: {self.goal.title}, User: {self.user.username}"
        self.assertEqual(str(self.goal), expected)
    
    def test_goal_without_deadline(self):
        """
        Test that a goal can be created without a deadline.
        
        Deadlines are optional - some goals are ongoing.
        """
        goal = Goal.objects.create(
            user=self.user,
            title="Drink more water",
            description="Stay hydrated",
            category=self.category,
            unit=self.unit,
            target_value=2000.0,
            deadline=None
        )
        
        self.assertIsNone(goal.deadline)
    
    def test_days_remaining_with_deadline(self):
        """
        Test the days_remaining() method calculates correctly.
        """
        # Goal has a deadline 30 days from today
        days = self.goal.days_remaining()
        self.assertEqual(days, 30)
    
    def test_days_remaining_without_deadline(self):
        """
        Test that days_remaining() returns None when there's no deadline.
        """
        goal = Goal.objects.create(
            user=self.user,
            title="Test",
            category=self.category,
            unit=self.unit,
            target_value=100.0,
            deadline=None
        )
        
        self.assertIsNone(goal.days_remaining())
    
    def test_get_current_value_no_progress(self):
        """
        Test that get_current_value() returns 0 when there's no progress.
        """
        self.assertEqual(self.goal.get_current_value(), 0)
    
    def test_get_current_value_with_progress(self):
        """
        Test that get_current_value() sums all progress values.
        """
        # Add some progress
        Progress.objects.create(user=self.user, goal=self.goal, value=10.0)
        Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=20.0,
            date=date.today() - timedelta(days=1)
        )
        
        # Total progress should be 30.0
        self.assertEqual(self.goal.get_current_value(), 30.0)
    
    def test_has_today_progress(self):
        """
        Test checking if progress was logged today.
        """
        # Initially, no progress today
        self.assertFalse(self.goal.has_today_progress(self.user))
        
        # Add progress for today
        Progress.objects.create(user=self.user, goal=self.goal, value=5.0)
        
        # Now there should be progress today
        self.assertTrue(self.goal.has_today_progress(self.user))
    
    def test_likes_count(self):
        """
        Test the likes_count property.
        """
        from social.models import Like
        
        # Initially, no likes
        self.assertEqual(self.goal.likes_count, 0)
        
        # Add some likes
        user2 = User.objects.create_user(username='user2', password='pass')
        Like.objects.create(user=self.user, goal=self.goal)
        Like.objects.create(user=user2, goal=self.goal)
        
        # Should have 2 likes
        self.assertEqual(self.goal.likes_count, 2)
    
    def test_is_liked_by(self):
        """
        Test the is_liked_by() method.
        """
        from social.models import Like
        
        # Initially, user hasn't liked the goal
        self.assertFalse(self.goal.is_liked_by(self.user))
        
        # After liking
        Like.objects.create(user=self.user, goal=self.goal)
        
        # Should return True
        self.assertTrue(self.goal.is_liked_by(self.user))


class ProgressModelTest(TestCase):
    """
    Test the Progress model.
    
    What is Progress?
    -----------------
    Progress represents a daily entry of work toward a goal (e.g., "Ran 5km today").
    Users can only log one progress entry per goal per day.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='pass')
        
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 100km",
            category=self.category,
            unit=self.unit,
            target_value=100.0
        )
    
    def test_progress_creation(self):
        """
        Test that a progress entry is created successfully.
        """
        progress = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
        
        self.assertEqual(progress.user, self.user)
        self.assertEqual(progress.goal, self.goal)
        self.assertEqual(progress.value, 10.0)
        # Date should default to today (note: the model uses 'now' which returns datetime)
        # We need to compare just the date part
        if hasattr(progress.date, 'date'):
            # If it's a datetime, get the date part
            self.assertEqual(progress.date.date(), date.today())
        else:
            # If it's already a date
            self.assertEqual(progress.date, date.today())
    
    def test_progress_string_representation(self):
        """
        Test the __str__() method shows user, goal, value, and date.
        """
        progress = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
        
        expected = f"{self.user.username} - {self.goal.title} - 10.0 on {progress.date}"
        self.assertEqual(str(progress), expected)
    
    def test_progress_unique_constraint(self):
        """
        Test that a user can only log one progress per goal per day.
        
        Why is this important?
        ----------------------
        The database has a unique constraint on (user, goal, date).
        This prevents duplicate entries for the same day.
        """
        # Create first progress for today
        Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
        
        # Try to create another progress for today - should fail
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Progress.objects.create(
                user=self.user,
                goal=self.goal,
                value=20.0
            )
    
    def test_progress_different_days(self):
        """
        Test that a user can log progress on different days.
        """
        # Progress for today
        p1 = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
        
        # Progress for yesterday
        p2 = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=15.0,
            date=date.today() - timedelta(days=1)
        )
        
        # Both should exist
        self.assertEqual(Progress.objects.filter(goal=self.goal).count(), 2)
    
    def test_is_today(self):
        """
        Test the is_today() method.
        """
        # Progress for today (use explicit date to avoid datetime confusion)
        today_progress = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0,
            date=date.today()
        )
        
        # Progress for yesterday
        yesterday_progress = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0,
            date=date.today() - timedelta(days=1)
        )
        
        self.assertTrue(today_progress.is_today())
        self.assertFalse(yesterday_progress.is_today())


class ProgressPhotoModelTest(TestCase):
    """
    Test the ProgressPhoto model.
    
    What is a ProgressPhoto?
    ------------------------
    Users can attach photos to their progress entries (e.g., a photo of
    their workout or meal). This model represents those photos.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='pass')
        
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        self.goal = Goal.objects.create(
            user=self.user,
            title="Test Goal",
            category=self.category,
            unit=self.unit,
            target_value=100.0
        )
        
        self.progress = Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
    
    def test_progress_photo_creation(self):
        """
        Test that a progress photo can be created.
        """
        # Create a simple test image file
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        photo = ProgressPhoto.objects.create(
            progress=self.progress,
            image=image
        )
        
        self.assertEqual(photo.progress, self.progress)
        self.assertIsNotNone(photo.uploaded_at)
        # Image should be saved
        self.assertTrue(photo.image.name.startswith('progress_photos/'))


# =============================================================================
# SERVICE TESTS
# =============================================================================

class GoalServiceTest(TestCase):
    """
    Test the goal service functions.
    
    What are services?
    ------------------
    Services contain business logic separate from models and views.
    This follows the "fat services, thin views" pattern for clean code.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='pass')
        
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 100km",
            category=self.category,
            unit=self.unit,
            target_value=100.0,
            deadline=date.today() + timedelta(days=30)
        )
    
    def test_goal_is_completed_false(self):
        """
        Test goal_is_completed() returns False when goal is not completed.
        """
        # No progress yet
        self.assertFalse(goal_is_completed(self.goal))
        
        # Add some progress, but not enough
        Progress.objects.create(user=self.user, goal=self.goal, value=50.0)
        self.assertFalse(goal_is_completed(self.goal))
    
    def test_goal_is_completed_true(self):
        """
        Test goal_is_completed() returns True when target is reached.
        """
        # Add enough progress to reach the target
        Progress.objects.create(user=self.user, goal=self.goal, value=100.0)
        
        self.assertTrue(goal_is_completed(self.goal))
    
    def test_goal_is_overdue_false(self):
        """
        Test goal_is_overdue() returns False when deadline hasn't passed.
        """
        # Goal has deadline 30 days from now
        self.assertFalse(goal_is_overdue(self.goal))
    
    def test_goal_is_overdue_true(self):
        """
        Test goal_is_overdue() returns True when deadline has passed and not completed.
        """
        # Set deadline to yesterday
        self.goal.deadline = date.today() - timedelta(days=1)
        self.goal.save()
        
        # Goal should be overdue
        self.assertTrue(goal_is_overdue(self.goal))
    
    def test_goal_is_overdue_false_if_completed(self):
        """
        Test that completed goals are never considered overdue.
        """
        # Set deadline to yesterday
        self.goal.deadline = date.today() - timedelta(days=1)
        self.goal.save()
        
        # Complete the goal
        Progress.objects.create(user=self.user, goal=self.goal, value=100.0)
        
        # Should not be overdue because it's completed
        self.assertFalse(goal_is_overdue(self.goal))
    
    def test_goal_get_status_active(self):
        """
        Test goal_get_status() returns 'active' for ongoing goals.
        """
        self.assertEqual(goal_get_status(self.goal), 'active')
    
    def test_goal_get_status_completed(self):
        """
        Test goal_get_status() returns 'completed' for finished goals.
        """
        Progress.objects.create(user=self.user, goal=self.goal, value=100.0)
        self.assertEqual(goal_get_status(self.goal), 'completed')
    
    def test_goal_get_status_overdue(self):
        """
        Test goal_get_status() returns 'overdue' for past-deadline goals.
        """
        self.goal.deadline = date.today() - timedelta(days=1)
        self.goal.save()
        
        self.assertEqual(goal_get_status(self.goal), 'overdue')
    
    def test_goal_progress_percentage(self):
        """
        Test goal_progress_percentage() calculates correctly.
        """
        # No progress - should be 0%
        self.assertEqual(goal_progress_percentage(self.goal), 0)
        
        # Add 50km of progress - should be 50%
        Progress.objects.create(user=self.user, goal=self.goal, value=50.0)
        self.assertEqual(goal_progress_percentage(self.goal), 50.0)
        
        # Add more progress to exceed target - should cap at 100%
        Progress.objects.create(
            user=self.user,
            goal=self.goal,
            value=75.0,
            date=date.today() - timedelta(days=1)
        )
        self.assertEqual(goal_progress_percentage(self.goal), 100.0)
    
    def test_progress_create_or_update_creates(self):
        """
        Test progress_create_or_update() creates new progress.
        """
        progress, created = progress_create_or_update(
            user=self.user,
            goal=self.goal,
            value=10.0
        )
        
        self.assertTrue(created)
        self.assertEqual(progress.value, 10.0)
    
    def test_progress_create_or_update_updates(self):
        """
        Test progress_create_or_update() updates existing progress.
        """
        # Create initial progress
        progress_create_or_update(user=self.user, goal=self.goal, value=10.0)
        
        # Update it with a new value
        progress, created = progress_create_or_update(
            user=self.user,
            goal=self.goal,
            value=20.0
        )
        
        self.assertFalse(created)
        self.assertEqual(progress.value, 20.0)
        # Should still be only one progress entry
        self.assertEqual(Progress.objects.filter(goal=self.goal).count(), 1)
    
    def test_progress_check_goal_completion(self):
        """
        Test progress_check_goal_completion() marks goal as finished.
        """
        # Add enough progress to complete the goal
        Progress.objects.create(user=self.user, goal=self.goal, value=100.0)
        
        # Check completion
        was_completed = progress_check_goal_completion(self.goal)
        
        self.assertTrue(was_completed)
        # Reload goal from database
        self.goal.refresh_from_db()
        self.assertIsNotNone(self.goal.finished_at)
    
    def test_goal_list_for_user(self):
        """
        Test goal_list_for_user() returns user's goals with annotations.
        """
        # Create multiple goals
        goal2 = Goal.objects.create(
            user=self.user,
            title="Another goal",
            category=self.category,
            unit=self.unit,
            target_value=50.0
        )
        
        goals = goal_list_for_user(user=self.user)
        
        # Should return 2 goals
        self.assertEqual(len(goals), 2)
        # Goals should have current_value annotation
        for goal in goals:
            self.assertTrue(hasattr(goal, 'current_value'))
    
    def test_goal_list_for_user_with_filter(self):
        """
        Test goal_list_for_user() with status filter.
        """
        # Create a completed goal
        completed_goal = Goal.objects.create(
            user=self.user,
            title="Completed",
            category=self.category,
            unit=self.unit,
            target_value=50.0
        )
        Progress.objects.create(user=self.user, goal=completed_goal, value=50.0)
        
        # Get only active goals
        active_goals = goal_list_for_user(user=self.user, status_filter='active')
        
        # Should not include the completed goal
        active_ids = [g.id for g in active_goals]
        self.assertIn(self.goal.id, active_ids)
        self.assertNotIn(completed_goal.id, active_ids)
    
    def test_goal_list_public(self):
        """
        Test goal_list_public() returns only public goals.
        """
        # Make the goal public
        self.goal.is_public = True
        self.goal.save()
        
        # Create a private goal
        private_goal = Goal.objects.create(
            user=self.user,
            title="Private",
            category=self.category,
            unit=self.unit,
            target_value=50.0,
            is_public=False
        )
        
        public_goals = goal_list_public()
        
        # Should only include the public goal
        public_ids = [g.id for g in public_goals]
        self.assertIn(self.goal.id, public_ids)
        self.assertNotIn(private_goal.id, public_ids)
    
    def test_dashboard_get_category_stats(self):
        """
        Test dashboard_get_category_stats() returns statistics per category.
        """
        # Create goals in different categories
        cat2 = Category.objects.create(cat="Nutrition", order=2)
        
        Goal.objects.create(
            user=self.user,
            title="Nutrition goal",
            category=cat2,
            unit=self.unit,
            target_value=50.0
        )
        
        stats = dashboard_get_category_stats(user=self.user)
        
        # Should have stats for both categories
        self.assertIn(self.category.id, stats)
        self.assertIn(cat2.id, stats)
        
        # Each category should have the right counts
        fitness_stats = stats[self.category.id]
        self.assertEqual(fitness_stats['total'], 1)
        self.assertEqual(fitness_stats['active'], 1)


# =============================================================================
# FORM TESTS
# =============================================================================

class CustomUserCreationFormTest(TestCase):
    """
    Test the custom user registration form.
    
    What does this form do?
    -----------------------
    It handles new user registration with username, email, and password fields.
    """
    
    def test_valid_form(self):
        """
        Test that the form is valid with correct data.
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """
        Test that the form is invalid when passwords don't match.
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_missing_email(self):
        """
        Test that the form is invalid without an email.
        """
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class GoalFormTest(TestCase):
    """
    Test the goal creation form.
    
    What does this form do?
    -----------------------
    It handles creating new goals with all required fields including
    title, description, category, unit, target value, and deadline.
    """
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
    
    def test_valid_form(self):
        """
        Test that the form is valid with correct data.
        """
        form_data = {
            'title': 'Run 100km',
            'description': 'Complete 100km of running',
            'category': self.category.id,
            'unit': self.unit.id,
            'target_value': 100.0,
            'deadline': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'is_public': True
        }
        form = GoalForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        """
        Test that the form is invalid without required fields.
        """
        form_data = {}
        form = GoalForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        # Should have errors for required fields
        self.assertIn('title', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('category', form.errors)


class GoalEditFormTest(TestCase):
    """
    Test the goal editing form.
    
    What's different from GoalForm?
    -------------------------------
    The edit form disables the category and unit fields since changing
    them could invalidate existing progress data.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='pass')
        
        self.category = Category.objects.create(cat="Fitness", order=1)
        self.unit = Unit.objects.create(name="km", order=1)
        self.category.units.add(self.unit)
        
        self.goal = Goal.objects.create(
            user=self.user,
            title="Original Title",
            description="Original description",
            category=self.category,
            unit=self.unit,
            target_value=100.0
        )
    
    def test_category_and_unit_disabled(self):
        """
        Test that category and unit fields are disabled in edit form.
        """
        form = GoalEditForm(instance=self.goal)
        
        # These fields should be disabled
        self.assertTrue(form.fields['category'].disabled)
        self.assertTrue(form.fields['unit'].disabled)
