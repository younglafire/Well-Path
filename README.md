# Goal Tracking App

This project is my **CS50x Final Project** and also a personal project that I built to sharpen my skills in web development.  
The idea behind it is simple but powerful: **a health-focused goal tracking application** where users can set goals, track their progress, and interact with others for motivation.

---

## 🚀 About the Project

- **Backend & Core Features:** I implemented all the functionality, database models, and logic myself.  
- **Frontend/UI:** For the user interface, I leveraged AI tools to generate components and layouts, then debugged and adjusted them to integrate smoothly with my backend.  
- **Focus:** The app is designed with a focus on **health goals** (e.g., exercise, nutrition, fitness milestones), but it can be extended to other areas.

---

## ✨ Features

- Create, update, delete, and list personal goals (CRUD).
- Progress tracking (optional).
- Sort and filter goals for easy navigation.
- Goal detail pages with a clean layout.
- Social features: public goals feed and comment system.
- Deployment-ready with testing and polish.

---

## 🛠️ Tech Stack

- **Backend:** Django / Python  
- **Database:** SQLite (development) → easily switchable to PostgreSQL (production)  
- **Frontend:** HTML, CSS, and templates (UI generated with AI assistance, debugged by me)  
- **Version Control:** Git & GitHub  
- **Deployment:** (Heroku, Render, or platform of choice)  

---

## 📅 Development Timeline

The project was structured in four phases:

1. **Core CRUD** – Foundation of the app (goals, progress).  
2. **User Experience** – Detail pages, sorting, filtering.  
3. **Social Features** – Public feed and comments.  
4. **Polish & Deploy** – UI/UX tweaks, final testing, and deployment.  

---

## ⚙️ How to Run

Clone this repository:

   git clone <your-repo-url>
   cd <your-repo-folder>

Install requirements:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Open in your browser:
http://127.0.0.1:8000/

