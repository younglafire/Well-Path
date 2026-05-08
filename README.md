# Well Path

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1>🌱 Well Path</h1>
  <h3>A Health-Focused Goal Tracking Application</h3>
  <p>
    Set goals. Track progress. Share your journey.
    <br />
    <a href="https://github.com/younglafire/Well-Path"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://wellpath-kgap.onrender.com">View Live Demo</a>
    ·
    <a href="https://github.com/younglafire/Well-Path/issues">Report Bug</a>
    ·
    <a href="https://github.com/younglafire/Well-Path/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#option-1-docker-compose-recommended">Option 1: Docker Compose</a></li>
        <li><a href="#option-2-manual-local-setup">Option 2: Manual Local Setup</a></li>
        <li><a href="#environment-variables">Environment Variables</a></li>
      </ul>
    </li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#dfds">DFDs</a></li>
    <li><a href="#website-flow">Website Flow</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#development-process">Development Process</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Well Path is a health-focused goal tracking application designed to help users set meaningful goals, monitor their progress, and connect with others for motivation. Built as my CS50W Final Project, this application demonstrates full-stack web development capabilities with a focus on clean architecture, user experience, and social interaction.

**The Philosophy Behind Well Path:**

The idea is simple but powerful: achieving health goals becomes easier when you can track your progress and share your journey with others. Whether it's exercise milestones, nutrition targets, or fitness achievements, Well Path provides the tools to stay accountable and motivated.

**My Role & Approach:**

- **Backend & Core Features**: I implemented all functionality, database models, and business logic from scratch
- **Frontend/UI**: Leveraged AI tools to generate initial components and layouts, then debugged and customized them to integrate seamlessly with my backend
- **Focus**: Designed with health goals in mind, but the architecture is flexible enough to extend to other goal categories

This project showcases my ability to:
- Design and implement full-stack web applications
- Work with modern web frameworks and databases
- Debug and integrate AI-generated code with custom backend logic
- Build scalable, deployment-ready applications
- Implement both individual and social features

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML"><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS"><img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"></a>
  <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"></a>
  <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>

**Technology Stack:**

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python) |
| **Database** | PostgreSQL (development & production) |
| **Frontend** | HTML5, CSS3, JavaScript with Django templates |
| **REST API** | Django REST Framework + drf-spectacular |
| **Application Server** | Gunicorn + Uvicorn (ASGI) |
| **Static Files** | WhiteNoise |
| **Containerization** | Docker + Docker Compose |
| **Deployment** | Render |
| **Version Control** | Git & GitHub |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

✅ **Complete CRUD Operations**
- Create, read, update, and delete personal goals
- Full control over your goal management

🏷️ **Goal Taxonomy (Categories & Units)**
- Organize goals into categories (Fitness, Nutrition, Wellness, etc.)
- Assign measurement units (km, kg, ml, minutes, etc.)
- Dynamic unit loading based on selected category

🎯 **Progress Tracking**
- Log daily progress values (one entry per goal per day)
- Attach progress photos (up to 5 MB per image)
- Visual charts that adapt to goal timespan (daily / weekly / monthly)
- Automatic goal completion detection

📊 **Dashboard & Analytics**
- Personal dashboard with live goal status (active / completed / overdue)
- Category-level statistics (active vs. completed goals per category)
- Filterable goal list by status via AJAX

🌐 **Social Features**
- Public goals feed visible to all visitors
- Like / unlike other users' goals (AJAX-powered, no page reload)

🚀 **Production-Ready**
- 66 comprehensive unit tests covering models, views, services, and forms
- Environment-variable-driven configuration
- Deployed on Render with PostgreSQL and Gunicorn

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Project Structure

```
Well-Path/
├── requirements.txt           # Root-level pinned dependencies
├── build.sh                   # Render build script (install → collectstatic → migrate)
├── render.yaml                # Render deployment configuration
├── SECURITY.md                # Security policy & vulnerability reporting
├── TESTING.md                 # In-depth testing guide
└── WellPath/                  # Django project root (manage.py lives here)
    ├── manage.py
    ├── requirements.txt       # App-level pinned dependencies
    ├── Dockerfile             # Multi-stage Docker build (Python 3.13-slim)
    ├── compose.yml            # Docker Compose (PostgreSQL + Django web service)
    ├── WellPath/              # Django settings package
    │   ├── settings.py        # Environment-driven settings, feature flags, logging
    │   ├── urls.py            # Root URL configuration
    │   ├── context_processors.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── goals/                 # Core app — users, goals, progress, photos
    │   ├── models.py          # User, Goal, Progress, ProgressPhoto
    │   ├── views.py           # Auth, CRUD, dashboard, AJAX endpoints
    │   ├── services.py        # Business logic (HackSoft style guide)
    │   ├── forms.py           # Registration, GoalForm, GoalEditForm
    │   ├── urls.py
    │   └── templates/goals/   # All HTML templates
    ├── social/                # Like system
    │   ├── models.py          # Like (unique per user+goal)
    │   ├── views.py           # like_goal AJAX endpoint
    │   └── urls.py
    ├── taxonomy/              # Goal categories & measurement units
    │   ├── models.py          # Category (with auto-slug), Unit
    │   ├── views.py           # Category filter view, AJAX unit loader
    │   └── urls.py
    └── api/                   # REST API app (Django REST Framework — placeholder)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

The Django project lives inside the `WellPath/` subdirectory. All `manage.py` commands must be run from there. Choose either the Docker Compose path (zero dependency setup) or the manual path.

### Option 1: Docker Compose (Recommended)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

1. **Clone the repository**
   ```sh
   git clone https://github.com/younglafire/Well-Path.git
   cd Well-Path/WellPath
   ```

2. **Create your `.env` file** (see [Environment Variables](#environment-variables) below)
   ```sh
   cp .env.example .env   # then edit .env with your values
   ```

3. **Start all services**
   ```sh
   docker compose up --build
   ```
   This starts a PostgreSQL 17 container and the Django web container on port `8000`.

4. **Run migrations** (first time only, in a separate terminal)
   ```sh
   docker compose exec django-web python manage.py migrate
   docker compose exec django-web python manage.py createsuperuser  # optional
   ```

5. **Open your browser**
   ```
   http://localhost:8000/
   ```

6. **Stop the services**
   ```sh
   docker compose down
   ```

### Option 2: Manual Local Setup

**Prerequisites:**
- Python 3.10 or higher
- PostgreSQL 14+ running locally (or use any `DATABASE_URL`)
- pip

1. **Clone the repository**
   ```sh
   git clone https://github.com/younglafire/Well-Path.git
   cd Well-Path
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   # venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```sh
   cd WellPath
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** inside `WellPath/` (see [Environment Variables](#environment-variables) below)

5. **Create the PostgreSQL database** (if not using `DATABASE_URL`)
   ```sh
   # The helper script creates the DB and user for you:
   cd ..
   bash setup-postgres.sh
   cd WellPath
   ```
   Or create it manually:
   ```sql
   CREATE DATABASE wellpath_db;
   CREATE USER wellpath_user WITH PASSWORD 'wellpath_password';
   GRANT ALL PRIVILEGES ON DATABASE wellpath_db TO wellpath_user;
   ```

6. **Apply database migrations**
   ```sh
   python manage.py migrate
   ```

7. **Create a superuser** (optional, for Django admin access)
   ```sh
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```sh
   python manage.py runserver
   ```

9. **Open your browser**
   ```
   http://127.0.0.1:8000/
   ```

### Environment Variables

Create a file named `.env` inside the `WellPath/` directory with the following variables:

```env
# Django core
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (choose one option)

# Option A — individual variables (local PostgreSQL)
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=wellpath_db
POSTGRES_USER=wellpath_user
POSTGRES_PASSWORD=wellpath_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Option B — single URL (Render / other cloud providers)
# DATABASE_URL=postgres://user:password@host:5432/dbname

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Feature flags (optional)
ENABLE_GPT5_FOR_ALL_CLIENTS=true
```

> **Note:** Never commit `.env` to version control. It is already listed in `.gitignore`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TESTING -->
## Testing

Well Path includes a comprehensive test suite to ensure code quality and reliability. Tests cover models, views, services, and forms across all applications.

> All test commands must be run from the `WellPath/` subdirectory (where `manage.py` lives).

### Running Tests

**Run all tests:**
```sh
cd WellPath
python manage.py test
```

**Run tests for a specific app:**
```sh
python manage.py test goals      # Test the goals app
python manage.py test social     # Test the social app
python manage.py test taxonomy   # Test the taxonomy app
```

**Run tests with verbose output:**
```sh
python manage.py test --verbosity=2
```

**Run a specific test class or method:**
```sh
python manage.py test goals.tests.GoalModelTest
python manage.py test goals.tests.GoalModelTest.test_goal_creation
```

### Test Coverage

The project includes **66 comprehensive tests** covering:

📋 **Goals App (40 tests)**
- User model and authentication
- Goal model with status calculations (active / completed / overdue)
- Progress tracking with unique daily constraint
- ProgressPhoto model with file-size and type validation
- Business logic in the service layer (`services.py`)
- User registration and goal forms

👥 **Social App (11 tests)**
- Like model with unique-per-user-per-goal constraint
- Like/unlike toggle via AJAX endpoint
- Authentication enforcement on social endpoints

🏷️ **Taxonomy App (15 tests)**
- Category model with automatic slug generation
- Unit model creation and ordering
- Category-filtered goal views
- AJAX unit-loading endpoint

### Understanding the Tests

Each test file includes detailed comments explaining:
- **What** is being tested
- **Why** it matters
- **How** the test is structured

This makes the tests an excellent learning resource for Django development patterns!

### Example Test Structure

```python
def test_goal_creation(self):
    """
    Test that a goal is created successfully with all fields.

    This checks:
    - The goal exists in the database
    - All fields are stored correctly
    """
    self.assertEqual(self.goal.title, "Run 100km")
    self.assertTrue(self.goal.is_public)
```

### Writing New Tests

When adding new features:
1. Write tests first (Test-Driven Development)
2. Run tests to confirm they fail
3. Implement the feature
4. Run tests to confirm they pass

See [TESTING.md](TESTING.md) for a complete guide including patterns, debugging tips, and further learning resources.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

**Getting Started with Well Path:**

1. **Create an Account**: Register with a username, email, and password
2. **Set Your First Goal**: Pick a category (e.g., Fitness), a unit (e.g., km), and a target value with a deadline
3. **Track Daily Progress**: Log today's progress value and optionally attach a photo
4. **View Your Charts**: The goal detail page shows a progress chart (daily / weekly / monthly based on timespan) with your average pace and what you still need per day
5. **Share Your Journey**: Toggle a goal to **Public** so it appears in the community feed
6. **Engage with the Community**: Like other users' goals from the feed

**Example Use Cases:**
- Track a running goal: *Run 100 km by end of year* → log km each day
- Monitor hydration: *Drink 60 litres of water this month* → log ml each day
- Build a meditation habit: *Meditate 1 800 minutes in 90 days* → log minutes daily

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DFDS -->
## DFDs

<!-- Context Diagram -->
### Context Diagram For All Apps

<img width="663" height="933" alt="Image" src="https://github.com/user-attachments/assets/897453b1-607a-4853-85eb-5fe21c915c05" />

<!-- WEBSITE FLOW -->

## Website Flow

https://github.com/user-attachments/assets/a0ffd798-5d1c-4a90-982a-afdb17e3ab10

### User Registration & Authentication Flow
```mermaid
graph LR
    A[Start] --> B[Landing Page]
    B --> C[Register Form]
    B --> D[Login Form]
    C --> F[Login]
    D --> G[Dashboard]
    F --> G
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style G fill:#e8f5e9
```
### Goal Creation & Management Flow
```mermaid
graph LR
    A[Dashboard] --> B[Click New Goal]
    B --> C[Fill Form]
    C --> D[Submit]
    D --> E[Goal Detail Page]
    E --> F[Back to Dashboard]
    
    style A fill:#e3f2fd
    style E fill:#f3e5f5
    style F fill:#e8f5e9
```
### Social Interaction Flow
```mermaid
graph LR
    A[Dashboard] --> B[Navigate to Feed]
    B --> C[View Public Goals]
    C --> D[Like Goal]
    D --> E[Click Goal]
    E --> F[Read Details]
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style E fill:#e8f5e9
```

### 🎨 System State Diagram

```
                    ┌──────────────┐
                    │  Anonymous   │
                    │    User      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Register/  │
                    │    Login     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
              ┌─────┤ Authenticated├─────┐
              │     │     User     │     │
              │     └──────────────┘     │
              │                          │
       ┌──────▼──────┐          ┌───────▼────────┐
       │   Personal  │          │     Social     │
       │    Goals    │          │     Feed       │
       └──────┬──────┘          └───────┬────────┘
              │                          │
    ┌─────────┼─────────┐               │
    ▼         ▼         ▼               ▼
┌────────┐ ┌──────┐ ┌──────┐    ┌────────────┐
│ Create │ │ Edit │ │Delete│    │    Like    │
└────────┘ └──────┘ └──────┘    └────────────┘
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEPLOYMENT -->
## Deployment

Well Path is configured for one-click deployment on **[Render](https://render.com)** using `render.yaml`.

### Render (Production)

The `render.yaml` at the repository root defines:
- A **PostgreSQL** managed database (`wellpathdb`)
- A **web service** running Gunicorn + Uvicorn (ASGI)

**Steps:**
1. Fork or push this repository to your GitHub account
2. In Render, select **New → Blueprint** and connect your repository
3. Render reads `render.yaml` and provisions the database and web service automatically
4. Set the `DJANGO_SECRET_KEY` (auto-generated) and any other env vars under the service's **Environment** tab
5. The `build.sh` script runs on every deploy:
   ```sh
   pip install -r requirements.txt
   python manage.py collectstatic --no-input
   python manage.py migrate
   ```

**Live URL:** `https://wellpath-kgap.onrender.com`

### Docker (Self-Hosted)

See [Option 1: Docker Compose](#option-1-docker-compose-recommended) in the Getting Started section.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

### Completed Features ✅
- [x] User authentication and authorization (register, login, logout)
- [x] Complete CRUD operations for goals
- [x] Goal taxonomy — categories and measurement units
- [x] Daily progress tracking with unique constraint
- [x] Progress photo uploads with size and type validation
- [x] Goal status engine (active / completed / overdue)
- [x] Adaptive progress charts (daily / weekly / monthly)
- [x] Dashboard with category-level statistics
- [x] AJAX goal filtering by status
- [x] Public goals feed
- [x] Like / unlike system (AJAX)
- [x] Responsive design
- [x] Docker & Docker Compose setup
- [x] Render deployment via `render.yaml`
- [x] Comprehensive test suite (66 tests across all apps)

### Future Enhancements 🚀
- [ ] Comment system on public goals
- [ ] Achievement badges and milestones
- [ ] User profile pages with statistics
- [ ] Follow / friend system
- [ ] Notification system
- [ ] REST API for third-party integrations (api app scaffold already in place)
- [ ] Goal templates and recommendations
- [ ] Export progress reports (PDF / CSV)
- [ ] Mobile app (React Native)

See the [open issues](https://github.com/younglafire/Well-Path/issues) for a full list of proposed features and known bugs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Known Issues
- The progress chart requires at least one logged progress entry to render correctly; an empty goal shows a blank chart.

<!-- DEVELOPMENT PROCESS -->
## Development Process

Well Path was built following a structured, phase-based approach:

### Phase 1: Core CRUD Operations
- Implemented database models for users, goals, and progress
- Built basic CRUD functionality
- Established project foundation and architecture

### Phase 2: Taxonomy & Enhanced UX
- Added Category and Unit models for structured goal organisation
- Designed and implemented goal detail pages with adaptive charts
- Added AJAX-powered filtering and dynamic unit loading
- Refined UI for better usability

### Phase 3: Social Features
- Created the public goals feed
- Implemented the like / unlike system with AJAX

### Phase 4: Polish & Deployment
- UI/UX refinements and responsive design
- Business logic extracted to a service layer (following HackSoft Django Style Guide)
- Comprehensive testing (66 tests) and bug fixes
- Docker, Docker Compose, and Render deployment setup

**Technical Decisions:**
- Chose Django for its robust ORM, built-in admin, and mature ecosystem
- Used PostgreSQL for both development and production to avoid environment-parity issues
- Separated business logic into `services.py` for cleaner views and easier testing
- Used database-level annotations (`annotate`, `Case/When`) for performant goal-status queries instead of Python-side loops
- Implemented AI-assisted frontend development with manual debugging and backend integration
- Structured code for scalability and maintainability

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

**Project Developer**: [Your Name]

- GitHub: [@younglafire](https://github.com/younglafire)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-linkedin-username)
- Email: your.email@example.com

**Project Link**: [https://github.com/younglafire/Well-Path](https://github.com/younglafire/Well-Path)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [CS50W - Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/)
* [CS50x - Introduction to Computer Science](https://cs50.harvard.edu/x/)
* [Django Documentation](https://docs.djangoproject.com/)
* [HackSoft Django Style Guide](https://github.com/HackSoftware/Django-Styleguide)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Shields.io - Badges](https://shields.io/)

---

<p align="center">
  <i>Built with ❤️ as part of my journey to becoming a professional developer</i>
</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/younglafire/Well-Path.svg?style=for-the-badge
[contributors-url]: https://github.com/younglafire/Well-Path/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/younglafire/Well-Path.svg?style=for-the-badge
[forks-url]: https://github.com/younglafire/Well-Path/network/members
[stars-shield]: https://img.shields.io/github/stars/younglafire/Well-Path.svg?style=for-the-badge
[stars-url]: https://github.com/younglafire/Well-Path/stargazers
[issues-shield]: https://img.shields.io/github/issues/younglafire/Well-Path.svg?style=for-the-badge
[issues-url]: https://github.com/younglafire/Well-Path/issues
[license-shield]: https://img.shields.io/github/license/younglafire/Well-Path.svg?style=for-the-badge
[license-url]: https://github.com/younglafire/Well-Path/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/your-linkedin-username
