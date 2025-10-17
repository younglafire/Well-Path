# 🧪 Testing Guide for Well Path

Welcome! This guide will help you understand the test suite for the Well Path project.

## 📚 What is Testing?

Testing is the practice of writing code to verify that your application works correctly. Think of it as a safety net that catches bugs before they reach your users.

### Why Write Tests?

1. **Catch Bugs Early**: Tests help you find problems before users do
2. **Confidence in Changes**: You can modify code knowing tests will catch any breaks
3. **Documentation**: Tests show how your code is supposed to work
4. **Better Design**: Writing testable code often leads to better architecture

## 🎯 What We've Tested

This project has **66 comprehensive tests** covering:

### Goals App (40 tests)
The core of the application - where users create and track their goals.

**Models (18 tests):**
- `User` model - User creation and authentication
- `Goal` model - Goal creation, status calculations, progress tracking
- `Progress` model - Daily progress logging with constraints
- `ProgressPhoto` model - Photo attachments for progress entries

**Services (19 tests):**
- Status checking (active, completed, overdue)
- Progress calculations and percentages
- Goal filtering and listing
- Dashboard statistics

**Forms (3 tests):**
- User registration form validation
- Goal creation form validation
- Goal editing form (with disabled fields)

### Social App (11 tests)
Features for user interaction and engagement.

**Models (5 tests):**
- `Like` model - User likes with unique constraints
- Relationship between users and goals

**Views (6 tests):**
- Like/unlike toggle functionality
- Authentication requirements
- AJAX endpoint responses

### Taxonomy App (15 tests)
Organization system for goals (categories and units).

**Models (9 tests):**
- `Category` model - Slug generation, ordering, relationships
- `Unit` model - Creation, ordering

**Views (6 tests):**
- Category filtering view
- Unit loading AJAX endpoint
- Authentication and permissions

## 🚀 Running Tests

### Run All Tests
```bash
cd WellPath
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test goals      # Test goals app only
python manage.py test social     # Test social app only
python manage.py test taxonomy   # Test taxonomy app only
```

### Run a Specific Test Class
```bash
python manage.py test goals.tests.GoalModelTest
```

### Run a Single Test Method
```bash
python manage.py test goals.tests.GoalModelTest.test_goal_creation
```

### Verbose Output
```bash
python manage.py test --verbosity=2
```

## 📖 Understanding Test Code

Let's break down a simple test:

```python
def test_goal_creation(self):
    """
    Test that a goal is created successfully.
    """
    # Arrange: Set up test data
    goal = Goal.objects.create(
        user=self.user,
        title="Run 100km",
        target_value=100.0
    )
    
    # Assert: Check that it worked
    self.assertEqual(goal.title, "Run 100km")
    self.assertEqual(goal.target_value, 100.0)
```

### Key Concepts:

**1. Test Methods**
- Always start with `test_`
- Have descriptive names
- Include docstrings explaining what they test

**2. setUp() Method**
```python
def setUp(self):
    """Runs before each test method"""
    self.user = User.objects.create_user(username='test')
```
This creates data that multiple tests need.

**3. Assertions**
- `assertEqual(a, b)` - Check if a equals b
- `assertTrue(x)` - Check if x is True
- `assertFalse(x)` - Check if x is False
- `assertIn(a, b)` - Check if a is in b
- `assertRaises(Exception)` - Check if code raises an error

## 🎓 Learning from Tests

Each test file includes detailed comments to help you learn:

### What You'll Find:
- **Module docstrings** - Overview of what's being tested
- **Class docstrings** - Explanation of the component
- **Method docstrings** - What the specific test checks
- **Inline comments** - Why we do certain things

### Example:
```python
class GoalModelTest(TestCase):
    """
    Test the Goal model.
    
    What is a Goal?
    ---------------
    A Goal represents something a user wants to achieve.
    """
    
    def test_goal_creation(self):
        """
        Test that a goal is created successfully.
        
        This checks:
        - The goal exists in the database
        - All fields are stored correctly
        """
        # Create a test goal
        goal = Goal.objects.create(...)
        
        # Verify it was created correctly
        self.assertEqual(goal.title, "Run 100km")
```

## 🔍 Common Testing Patterns

### 1. Testing Models
```python
def test_model_creation(self):
    """Test that model instances are created correctly"""
    obj = MyModel.objects.create(field="value")
    self.assertEqual(obj.field, "value")
```

### 2. Testing Views
```python
def test_view_requires_login(self):
    """Test that view redirects when not logged in"""
    response = self.client.get(reverse('my-view'))
    self.assertEqual(response.status_code, 302)  # Redirect
```

### 3. Testing Forms
```python
def test_valid_form(self):
    """Test that form accepts valid data"""
    form = MyForm(data={'field': 'value'})
    self.assertTrue(form.is_valid())
```

### 4. Testing Database Constraints
```python
def test_unique_constraint(self):
    """Test that duplicate entries are prevented"""
    MyModel.objects.create(field="value")
    
    # This should raise an IntegrityError
    with self.assertRaises(IntegrityError):
        MyModel.objects.create(field="value")
```

## 📝 Writing New Tests

When adding a new feature:

### 1. Write the Test First (TDD)
```python
def test_new_feature(self):
    """Test the new feature I'm about to build"""
    result = my_new_function()
    self.assertEqual(result, "expected value")
```

### 2. Run the Test (It Should Fail)
```bash
python manage.py test goals.tests.MyTestClass.test_new_feature
```

### 3. Implement the Feature
Write the code to make the test pass.

### 4. Run the Test Again (It Should Pass)
```bash
python manage.py test goals.tests.MyTestClass.test_new_feature
```

### 5. Refactor if Needed
Improve the code while keeping tests passing.

## 🎯 Test Checklist

When writing tests, ask yourself:

- [ ] Does it test one specific thing?
- [ ] Is the test name descriptive?
- [ ] Does it include a docstring?
- [ ] Will it fail if the code breaks?
- [ ] Does it clean up after itself?
- [ ] Is it fast to run?

## 🚨 Debugging Failed Tests

If a test fails:

### 1. Read the Error Message
```
FAIL: test_goal_creation (goals.tests.GoalModelTest)
AssertionError: 'Run 50km' != 'Run 100km'
```

### 2. Check the Test
- Is the test correct?
- Are you testing what you think you're testing?

### 3. Check the Code
- Does your code do what you expect?
- Are there edge cases?

### 4. Add Print Statements
```python
def test_something(self):
    result = my_function()
    print(f"Result: {result}")  # Debug output
    self.assertEqual(result, "expected")
```

### 5. Run Just That Test
```bash
python manage.py test goals.tests.GoalModelTest.test_goal_creation --verbosity=2
```

## 📚 Further Learning

### Django Testing Documentation
- [Django Testing Overview](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Testing Tools](https://docs.djangoproject.com/en/stable/topics/testing/tools/)
- [Advanced Testing Topics](https://docs.djangoproject.com/en/stable/topics/testing/advanced/)

### Testing Best Practices
- Write tests for new features before implementing them (TDD)
- Test both success and failure cases
- Keep tests simple and focused
- Use descriptive names and docstrings
- Don't test Django's built-in functionality
- Mock external services (APIs, payments, etc.)

## 🎉 Next Steps

1. **Explore the Tests**: Read through the test files to understand how they work
2. **Run the Tests**: Get comfortable running different test commands
3. **Modify a Test**: Try changing a test to see what happens
4. **Write a Test**: Add a test for a new scenario
5. **Use TDD**: Try writing tests before code for your next feature

Happy Testing! 🚀
