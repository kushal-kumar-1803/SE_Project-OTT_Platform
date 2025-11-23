🎬 FilmAura — Smart OTT Streaming Platform

A modern Netflix-style OTT platform built with Flask, SQLite, and TMDB API.

<p align="center"> <img src="https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask"> <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite"> <img src="https://img.shields.io/badge/Frontend-HTML/CSS/JS-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/CI/CD-GitHub Actions-2088FF?style=for-the-badge&logo=githubactions"> </p>
🌟 Overview

FilmAura is a feature-rich OTT streaming web application inspired by Netflix and Prime Video.
Users can explore movies from TMDB, watch locally uploaded movies, manage their watchlist, subscribe for premium content, and enjoy a clean, cinematic UI.

Built using:

Flask (Python) for backend

SQLite for database

TMDB API for movie info

Vanilla JS for frontend interactions

GitHub Actions (CI/CD) for automated testing

🎥 Features
🔐 Authentication

User Registration & Login

JWT-based authentication

Separate Admin Dashboard

🎞 Streaming & Movie Management

Play local MP4 movie files

Admin can upload movies with poster, genre & description

Movies automatically appear on the user homepage

⭐ Watchlist System

Add/remove movies from watchlist

Dedicated My Watchlist page

Synced with backend (persistent)

🎬 TMDB Movie Integration

Trending movies

Genres (Action, Sci-Fi, Horror etc.)

Movie detail pages with posters, trailers & metadata

💳 Subscription System

Users must subscribe to watch local movies

Admin can approve pending payments

Subscription-based access control

🧪 Automated Testing (PyTest)

Test cases for:

Auth system

Movies API

TMDB API

Watchlist

CI pipeline runs tests on every push or pull request

🚀 CI/CD with GitHub Actions

Auto-install dependencies

Auto-run tests

Fails early on broken code

Supports Python 3.8 → 3.10

📁 Project Structure
SE_Project_OTT_Platform/
│── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── database/
│   └── tests/
│
│── frontend/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── videos/     ← Movie files (ignored by Git)
│   ├── index.html
│   └── pages/
│
│── .github/workflows/
│   └── ci.yml          ← CI/CD pipeline
│
│── .gitignore
│── requirements.txt
│── README.md

🛠 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/SE_Project-OTT_Platform.git
cd SE_Project-OTT_Platform

2️⃣ Create Virtual Environment
python -m venv venv
venv/Scripts/activate        # Windows
# OR
source venv/bin/activate     # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Initialize Database
python -c "from backend.database.db_connection import init_db; init_db()"

5️⃣ Run Server
python -m backend.app


Visit:
➡ http://127.0.0.1:5000

🧪 Running Tests
pytest -q

⚙️ GitHub Actions CI/CD

A workflow file at:
.github/workflows/ci.yml

Automatically:

Installs dependencies

Prepares database

Runs PyTest

Marks run as pass/fail

Runs on:

Every push

Every PR to main

Manual trigger from Actions tab

👨‍💻 Admin Panel

Admin can:

Upload movies (MP4)

Delete & update movies

Approve subscriptions

Manage local video library

🧑‍💼 Team
Name	Role
Kushal Kumar	Backend, Flask, Integration
(Add your teammates)	Frontend, Design
…	…
✨ Screenshots (Add on GitHub)

Just drag and drop images in GitHub’s markdown editor:

![Home Page](screenshots/home.png)
![Movie Page](screenshots/movie.png)
![Admin Panel](screenshots/admin.png)

🚀 Future Enhancements

Multi-user profiles

Continue watching section

Multi-language subtitles

Recommendation engine

Analytics dashboard

❤️ Contributions

Pull Requests are welcome!
Follow our CI pipeline guidelines before submitting.

📜 License

MIT License © 2025  
