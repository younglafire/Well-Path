from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.db import IntegrityError
from .models import User, Category, Unit, Goal, Progress
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass"))


class CategoryUnitModelTest(TestCase):
    # Test if the category and unit are created successfully
    def setUp(self):
        self.unit = Unit.objects.create(name="km")
        self.category = Category.objects.create(cat="Running")
        self.category.units.add(self.unit)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Running")

    def test_unit_str(self):
        self.assertEqual(str(self.unit), "km")

    def test_category_unit_relationship(self):
        self.assertIn(self.unit, self.category.units.all())


class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123")
        self.unit = Unit.objects.create(name="kg")
        self.category = Category.objects.create(cat="Fitness")
        self.goal = Goal.objects.create(
            user=self.user,
            title="Lose Weight",
            description="Lose 5kg in 2 months",
            category=self.category,
            unit=self.unit,
            target_value=5,
            current_value=1,
            deadline=now().date() + timedelta(days=10),
        )

    def test_goal_str_fields(self):
        self.assertEqual(self.goal.title, "Lose Weight")
        self.assertEqual(self.goal.target_value, 5)
        self.assertEqual(self.goal.current_value, 1)
        self.assertEqual(self.goal.deadline, now().date() + timedelta(days=10))

    def test_days_remaining(self):
        self.assertEqual(self.goal.days_remaining(), 10)

    def test_days_remaining_none(self):
        self.goal.deadline = None
        self.goal.save()
        self.assertIsNone(self.goal.days_remaining())


class ProgressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="progressuser", password="123")
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 50km",
            target_value=50,
            deadline=now().date() + timedelta(days=30),
        )

    def test_add_progress(self):
        progress = Progress.objects.create(
            user=self.user, goal=self.goal, value=5
        )
        self.assertEqual(str(progress), f"{self.user.username} - {self.goal.title} - 5 on {progress.date}")
        self.assertEqual(self.goal.progresses.count(), 1)

    def test_unique_daily_progress(self):
        Progress.objects.create(user=self.user, goal=self.goal, value=10)
        with self.assertRaises(IntegrityError):
            Progress.objects.create(user=self.user, goal=self.goal, value=15)

    def test_has_today_progress(self):
        Progress.objects.create(user=self.user, goal=self.goal, value=3)
        self.assertTrue(self.goal.has_today_progress(self.user))


class GoalProgressCalculationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="calcuser", password="123")
        self.goal = Goal.objects.create(
            user=self.user,
            title="Run 10km",
            target_value=10
        )

    def test_current_value(self):
        Progress.objects.create(user=self.user, goal=self.goal, value=2)
        # Progress from yesterday plus today
        Progress.objects.create(user=self.user, goal=self.goal, value=3, date=now().date() - timedelta(days=1))
        # total = 2 + 3
        total = sum(p.value for p in self.goal.progresses.all())
        self.assertEqual(total, 5)


class GoalDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.goal = Goal.objects.create(
            user=self.user,
            title="Test Goal",
            target_value=100,
            current_value=10
        )

    def test_delete_goal(self):
        # send POST to delete the goal
        response = self.client.post(reverse("delete_goal", args=[self.goal.id]))

        # check redirect
        self.assertRedirects(response, reverse("dashboard", args=[self.user.username]))

        # check goal is gone
        goals = Goal.objects.filter(id=self.goal.id)
        self.assertEqual(goals.count(), 0)


# Senlenium test
class TestEditGoalSelenium(StaticLiveServerTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(cat='Health')
        self.unit = Unit.objects.create(name='Steps')
        self.goal = Goal.objects.create(
            user=self.user,
            title='Walk More',
            description='Walk 10,000 steps daily',
            target_value=10000,
            category=self.category,
            unit=self.unit
        )
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_edit_goal(self):
        # Log in
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('testpass')
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Go to edit page
        self.browser.get(f'{self.live_server_url}/edit/{self.goal.id}')


# Testing the logic in models.py:
class GoalLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.goal = Goal.objects.create(user=self.user, title="Run", target_value=10, current_value=8)

    def test_is_completed_false(self):
        self.assertFalse(self.goal.is_completed())

    def test_is_completed_true(self):
        self.goal.current_value = 10
        self.assertTrue(self.goal.is_completed())

    def test_is_overdue_true(self):
        self.goal.deadline = now().date() - timedelta(days=1)
        self.assertTrue(self.goal.is_overdue())

    def test_is_overdue_false_if_completed(self):
        self.goal.deadline = now().date() - timedelta(days=1)
        self.goal.current_value = 12
        self.assertFalse(self.goal.is_overdue())

    def test_progress_percentage(self):
        self.goal.current_value = 5
        self.assertEqual(self.goal.progress_percentage(), 50)


class ProgressLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.goal = Goal.objects.create(user=self.user, title="Run", target_value=10)

    def test_is_today_true(self):
        p = Progress.objects.create(user=self.user, goal=self.goal, value=3, date=now().date())
        self.assertTrue(p.is_today())

    def test_is_today_false(self):
        p = Progress.objects.create(user=self.user, goal=self.goal, value=3, date=now().date() - timedelta(days=1))
        self.assertFalse(p.is_today())
