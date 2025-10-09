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
    <a href="https://github.com/younglafire/cs50w_final"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/younglafire/cs50w_final">View Demo</a>
    ·
    <a href="https://github.com/younglafire/cs50w_final/issues">Report Bug</a>
    ·
    <a href="https://github.com/younglafire/cs50w_final/issues">Request Feature</a>
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
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#dfds">DFDs</a></li>
    <li><a href="#website-flow">Website Flow</a></li>
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
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML"><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS"><img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"></a>
  <a href="https://git-scm.com/"><img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"></a>
  <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>

**Technology Stack:**
- **Backend**: Django (Python web framework)
- **Database**: SQLite for development, easily switchable to PostgreSQL for production
- **Frontend**: HTML, CSS, JavaScript with Django templates
- **Version Control**: Git & GitHub
- **Deployment**: Ready for Heroku, Render, or other platforms

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

✅ **Complete CRUD Operations**
- Create, read, update, and delete personal goals
- Full control over your goal management

🎯 **Progress Tracking**
- Optional progress monitoring for each goal
- Visual feedback on your achievements

🔍 **Smart Organization**
- Sort and filter goals for easy navigation
- Find exactly what you need, when you need it

📄 **Detailed Goal Pages**
- Clean, intuitive layout for each goal
- All information at a glance

🌐 **Social Features**
- Public goals feed to share your journey
- Comment system for community support and motivation
- Connect with others pursuing similar goals

🚀 **Production-Ready**
- Thoroughly tested and polished
- Deployment-ready architecture
- Scalable database design

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get Well Path running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/younglafire/cs50w_final.git
   cd cs50w_final
   ```

2. **Create a virtual environment (recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

7. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000/
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

**Getting Started with Well Path:**

1. **Create an Account**: Register to start tracking your health goals
2. **Set Your First Goal**: Define what you want to achieve (e.g., "Run 5km three times a week")
3. **Track Progress**: Update your progress as you work toward your goal
4. **Share Your Journey**: Make goals public to inspire others and receive support
5. **Engage with the Community**: Comment on other users' goals and celebrate their achievements

**Example Use Cases:**
- Track fitness milestones (running distance, workout frequency)
- Monitor nutrition goals (water intake, meal planning)
- Set and achieve wellness targets (meditation minutes, sleep hours)
- Share transformation journeys with supportive community

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DFDS -->
## DFDs

*Data Flow Diagrams will be added here to illustrate the system architecture and data flow through the application.*

<!-- Context Diagram -->
### Context Diagram
*[Image placeholder - Shows high-level system interactions between users, the Well Path application, and the database]*

<!-- Level 1 DFD -->
### Level 1 DFD
*[Image placeholder - Shows major processes: User Management, Goal Management, Progress Tracking, and Social Features]*

<!-- Level 2 DFD -->
### Level 2 DFD
*[Image placeholder - Detailed breakdown of Goal Management process showing CRUD operations and data flows]*

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- WEBSITE FLOW -->
## Website Flow

*Website flow diagrams will be added here to demonstrate user journeys and navigation paths through the application.*

### User Registration & Authentication Flow
*[Image placeholder - Shows the flow from landing page → registration → login → dashboard]*

### Goal Creation & Management Flow
*[Image placeholder - Shows the flow from dashboard → create goal → view goal → edit/update → track progress]*

### Social Interaction Flow
*[Image placeholder - Shows the flow from feed → view public goals → comment → like/interact]*

### Complete User Journey
*[Image placeholder - Shows end-to-end user experience from first visit to achieving and sharing goals]*

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

### Completed Features ✅
- [x] User authentication and authorization
- [x] Complete CRUD operations for goals
- [x] Progress tracking system
- [x] Goal sorting and filtering
- [x] Detailed goal pages
- [x] Public goals feed
- [x] Comment system
- [x] Responsive design
- [x] Database models and relationships

### Future Enhancements 🚀
- [ ] Goal categories and tags
- [ ] Data visualization (charts and graphs for progress)
- [ ] Achievement badges and milestones
- [ ] User profiles with statistics
- [ ] Follow/friend system
- [ ] Notification system
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations
- [ ] Goal templates and recommendations
- [ ] Export progress reports

See the [open issues](https://github.com/younglafire/cs50w_final/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEVELOPMENT PROCESS -->
## Development Process

Well Path was built following a structured, phase-based approach:

### Phase 1: Core CRUD Operations
- Implemented database models for users, goals, and progress
- Built basic CRUD functionality
- Established project foundation and architecture

### Phase 2: Enhanced User Experience
- Designed and implemented goal detail pages
- Added sorting and filtering capabilities
- Refined UI for better usability

### Phase 3: Social Features
- Created public goals feed
- Implemented commenting system
- Added user interaction capabilities

### Phase 4: Polish & Deployment
- UI/UX refinements and responsive design
- Comprehensive testing and bug fixes
- Deployment preparation and optimization

**Technical Decisions:**
- Chose Django for its robust ORM and built-in admin interface
- Used SQLite for development with easy PostgreSQL migration path
- Implemented AI-assisted frontend development with manual debugging and integration
- Structured code for scalability and maintainability

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

**Project Developer**: [Your Name]

- GitHub: [@younglafire](https://github.com/younglafire)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-linkedin-username)
- Email: your.email@example.com

**Project Link**: [https://github.com/younglafire/cs50w_final](https://github.com/younglafire/cs50w_final)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [CS50W - Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/)
* [CS50x - Introduction to Computer Science](https://cs50.harvard.edu/x/)
* [Django Documentation](https://docs.djangoproject.com/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Shields.io - Badges](https://shields.io/)

---

<p align="center">
  <i>Built with ❤️ as part of my journey to becoming a professional developer</i>
</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/younglafire/cs50w_final.svg?style=for-the-badge
[contributors-url]: https://github.com/younglafire/cs50w_final/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/younglafire/cs50w_final.svg?style=for-the-badge
[forks-url]: https://github.com/younglafire/cs50w_final/network/members
[stars-shield]: https://img.shields.io/github/stars/younglafire/cs50w_final.svg?style=for-the-badge
[stars-url]: https://github.com/younglafire/cs50w_final/stargazers
[issues-shield]: https://img.shields.io/github/issues/younglafire/cs50w_final.svg?style=for-the-badge
[issues-url]: https://github.com/younglafire/cs50w_final/issues
[license-shield]: https://img.shields.io/github/license/younglafire/cs50w_final.svg?style=for-the-badge
[license-url]: https://github.com/younglafire/cs50w_final/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/your-linkedin-username
