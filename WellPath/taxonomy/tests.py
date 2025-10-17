"""
Unit Tests for Taxonomy App

This module contains tests for the taxonomy application, which handles
categories and units for goals in the Well Path project.

What are we testing?
--------------------
1. Category Model - Ensures categories are created correctly with unique slugs
2. Unit Model - Tests the basic unit creation
3. Views - Tests the category view and AJAX endpoints

Why do we test?
---------------
Testing ensures that our code works as expected and helps catch bugs
before they reach production. It also makes it easier to make changes
in the future without breaking existing functionality.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Unit
from goals.models import Goal

# Get the User model (could be custom or default Django User)
User = get_user_model()


class CategoryModelTest(TestCase):
    """
    Test the Category model.
    
    What is a Category?
    -------------------
    A Category represents a type of goal (e.g., Fitness, Nutrition, Wellness).
    Each category can have multiple units associated with it.
    """
    
    def setUp(self):
        """
        Set up test data.
        
        setUp() runs before each test method. It's used to create
        data that multiple tests need. This keeps tests DRY (Don't Repeat Yourself).
        """
        # Create a test category
        self.category = Category.objects.create(
            cat="Fitness",
            order=1
        )
    
    def test_category_creation(self):
        """
        Test that a category is created successfully.
        
        This checks:
        - The category exists in the database
        - The category name is stored correctly
        """
        self.assertEqual(self.category.cat, "Fitness")
        self.assertEqual(self.category.order, 1)
    
    def test_category_slug_generation(self):
        """
        Test that slugs are automatically generated from category names.
        
        What is a slug?
        ---------------
        A slug is a URL-friendly version of a string (e.g., "Fitness" -> "fitness").
        It's used in URLs instead of IDs to make them more readable.
        """
        # The slug should be auto-generated when saving
        self.assertEqual(self.category.slug, "fitness")
    
    def test_category_slug_uniqueness(self):
        """
        Test that slugs are automatically generated and unique.
        
        Even with different category names, each category gets its own unique slug.
        Note: The 'cat' field is unique, so we can't have two categories with
        the same name. This test verifies that different names get different slugs.
        """
        # Create another category with a different name
        category2 = Category.objects.create(cat="Wellness", order=2)
        
        # The slugs should be different
        self.assertNotEqual(self.category.slug, category2.slug)
        # Both slugs should be valid
        self.assertEqual(self.category.slug, "fitness")
        self.assertEqual(category2.slug, "wellness")
    
    def test_category_string_representation(self):
        """
        Test the __str__() method.
        
        The __str__() method determines how a model instance is displayed
        as a string (e.g., in the Django admin or when printing).
        """
        self.assertEqual(str(self.category), "Fitness")
    
    def test_category_ordering(self):
        """
        Test that categories are ordered by their 'order' field.
        
        This ensures categories appear in a specific order in lists.
        """
        # Create categories with different order values
        cat1 = Category.objects.create(cat="Nutrition", order=3)
        cat2 = Category.objects.create(cat="Wellness", order=2)
        
        # Get all categories - they should be ordered by the 'order' field
        categories = list(Category.objects.all())
        
        # The first category should have order=1 (our setUp category)
        self.assertEqual(categories[0].order, 1)
        # The second should have order=2
        self.assertEqual(categories[1].order, 2)
        # The third should have order=3
        self.assertEqual(categories[2].order, 3)
    
    def test_category_units_relationship(self):
        """
        Test the many-to-many relationship between categories and units.
        
        A category can have multiple units (e.g., Fitness could have 'km', 'reps').
        """
        # Create some units
        unit1 = Unit.objects.create(name="km", order=1)
        unit2 = Unit.objects.create(name="reps", order=2)
        
        # Add units to the category
        self.category.units.add(unit1, unit2)
        
        # The category should have 2 units
        self.assertEqual(self.category.units.count(), 2)
        # The units should be in the category's units
        self.assertIn(unit1, self.category.units.all())
        self.assertIn(unit2, self.category.units.all())


class UnitModelTest(TestCase):
    """
    Test the Unit model.
    
    What is a Unit?
    ---------------
    A Unit represents a measurement unit (e.g., 'km' for distance, 'kg' for weight).
    Units are associated with categories through a many-to-many relationship.
    """
    
    def test_unit_creation(self):
        """
        Test that a unit is created successfully.
        """
        unit = Unit.objects.create(name="km", order=1)
        
        self.assertEqual(unit.name, "km")
        self.assertEqual(unit.order, 1)
    
    def test_unit_string_representation(self):
        """
        Test the __str__() method returns the unit name.
        """
        unit = Unit.objects.create(name="kg", order=1)
        self.assertEqual(str(unit), "kg")
    
    def test_unit_ordering(self):
        """
        Test that units are ordered by their 'order' field.
        """
        # Create units with different orders
        unit1 = Unit.objects.create(name="km", order=2)
        unit2 = Unit.objects.create(name="kg", order=1)
        unit3 = Unit.objects.create(name="reps", order=3)
        
        # Get all units - should be ordered by 'order' field
        units = list(Unit.objects.all())
        
        self.assertEqual(units[0].name, "kg")  # order=1
        self.assertEqual(units[1].name, "km")  # order=2
        self.assertEqual(units[2].name, "reps")  # order=3


class TaxonomyViewsTest(TestCase):
    """
    Test the views in the taxonomy app.
    
    What are we testing?
    --------------------
    1. Category view - Shows goals filtered by category
    2. Load units AJAX endpoint - Returns units for a selected category
    
    Why test views?
    ---------------
    Views are the bridge between models and templates. Testing them ensures
    the correct data is passed to templates and that permissions work correctly.
    """
    
    def setUp(self):
        """
        Set up test data for view tests.
        
        We need:
        - A test user (for authentication)
        - A test client (to simulate HTTP requests)
        - Test categories and units
        - Test goals
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test client (used to make requests)
        self.client = Client()
        
        # Create test categories and units
        self.fitness_category = Category.objects.create(cat="Fitness", order=1)
        self.nutrition_category = Category.objects.create(cat="Nutrition", order=2)
        
        self.km_unit = Unit.objects.create(name="km", order=1)
        self.kg_unit = Unit.objects.create(name="kg", order=2)
        
        # Associate units with categories
        self.fitness_category.units.add(self.km_unit)
        self.nutrition_category.units.add(self.kg_unit)
        
        # Create a test goal in the fitness category
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 100km",
            description="Complete 100km of running",
            category=self.fitness_category,
            unit=self.km_unit,
            target_value=100.0
        )
    
    def test_category_view_requires_login(self):
        """
        Test that the category view requires authentication.
        
        Why?
        ----
        The @login_required decorator ensures only logged-in users can
        access this view. If not logged in, users should be redirected to login.
        """
        # Try to access the category view without logging in
        response = self.client.get(
            reverse('category', kwargs={'category_slug': self.fitness_category.slug})
        )
        
        # Should redirect to login page (status code 302)
        self.assertEqual(response.status_code, 302)
        # The redirect URL should contain 'login'
        self.assertIn('login', response.url)
    
    def test_category_view_with_login(self):
        """
        Test that logged-in users can access the category view.
        """
        # Log in the test user
        self.client.login(username='testuser', password='testpass123')
        
        # Access the category view
        response = self.client.get(
            reverse('category', kwargs={'category_slug': self.fitness_category.slug})
        )
        
        # Should return success (status code 200)
        self.assertEqual(response.status_code, 200)
        # Should use the correct template
        self.assertTemplateUsed(response, 'taxonomy/category.html')
        # The category should be in the context
        self.assertEqual(response.context['category'], self.fitness_category)
    
    def test_category_view_filters_goals(self):
        """
        Test that the category view only shows goals for that category.
        """
        # Log in
        self.client.login(username='testuser', password='testpass123')
        
        # Create a goal in a different category
        other_goal = Goal.objects.create(
            user=self.user,
            title="Eat healthy",
            description="Nutrition goal",
            category=self.nutrition_category,
            unit=self.kg_unit,
            target_value=50.0
        )
        
        # Access the fitness category view
        response = self.client.get(
            reverse('category', kwargs={'category_slug': self.fitness_category.slug})
        )
        
        # The fitness goal should be in the goals list
        goals = response.context['goals']
        goal_ids = [g.id for g in goals]
        
        self.assertIn(self.goal.id, goal_ids)
        # The nutrition goal should NOT be in the list
        self.assertNotIn(other_goal.id, goal_ids)
    
    def test_load_units_ajax_endpoint(self):
        """
        Test the AJAX endpoint that loads units for a category.
        
        What is AJAX?
        -------------
        AJAX (Asynchronous JavaScript and XML) allows web pages to update
        parts of the page without reloading. This endpoint returns JSON data
        that JavaScript can use to populate a dropdown.
        """
        # Make a request with a category_id
        response = self.client.get(
            reverse('load_units'),
            {'category_id': self.fitness_category.id}
        )
        
        # Should return JSON (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = response.json()
        
        # Should return a list with 1 unit (km)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'km')
    
    def test_load_units_without_category(self):
        """
        Test the load_units endpoint when no category is provided.
        
        Should return an empty list.
        """
        response = self.client.get(reverse('load_units'))
        
        # Should return empty list
        data = response.json()
        self.assertEqual(len(data), 0)
    
    def test_load_units_with_invalid_category(self):
        """
        Test the load_units endpoint with an invalid category ID.
        
        Should return an empty list (no units found).
        """
        response = self.client.get(
            reverse('load_units'),
            {'category_id': 99999}  # Non-existent category
        )
        
        data = response.json()
        self.assertEqual(len(data), 0)
