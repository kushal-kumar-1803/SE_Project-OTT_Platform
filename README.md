<h1 align="center">🎬 FilmAura — OTT Streaming Platform</h1>
<p align="center"><i>A cinematic OTT platform inspired by Netflix — built with Flask, SQLite, and TMDB API.</i></p> <br> <p align="center"> <img src="https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask"> <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite"> <img src="https://img.shields.io/badge/CI/CD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions"> <img src="https://img.shields.io/badge/API-TMDB-01B4E4?style=for-the-badge&logo=themoviedatabase"> </p>
⭐ Overview

FilmAura is a modern OTT streaming platform that lets users watch movies, manage watchlists, explore trending films through TMDB API, and access premium content using a subscription system.
Admins can upload movies, approve payments, and manage the content library.

The project uses:

✨ Flask (Python)

✨ SQLite database

✨ TMDB API

✨ HTML, CSS, JS (Frontend)

✨ GitHub Actions for CI Pipeline

🚀 Features
🎯 User Features

🔐 Login / Registration

🎞 Movie streaming (local uploaded MP4)

📌 Add to watchlist

❤️ Dedicated My Watchlist page

🔎 Search movies

🎬 TMDB Trending & Genre-based movies

💳 Subscription system for premium movies

🛠 Admin Features

🎥 Upload movies (MP4)

🖼 Upload posters

🗃 Edit / Delete movies

🧾 Approve subscription payments

🧩 Movie list auto-updates on user homepage

🤖 Developer Features

🧪 PyTest suite for automated testing

⚙️ CI/CD pipeline using GitHub Actions

📦 Clean project structure

🔐 JWT Authentication

🗂 Project Structure
SE_Project_OTT_Platform/
│── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── database/
│   └── tests/
│
│── frontend/
│   ├── index.html
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── videos/   ← ignored in git
│
│── requirements.txt
│── README.md
│── .gitignore
│── .github/workflows/ci.yml

⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/<your-username>/SE_Project-OTT_Platform.git
cd SE_Project-OTT_Platform

2️⃣ Create Virtual Environment
python -m venv venv
venv/Scripts/activate   # Windows
# or
source venv/bin/activate  # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Initialize Database
python -c "from backend.database.db_connection import init_db; init_db()"

5️⃣ Run Application
python -m backend.app


➡ Visit http://127.0.0.1:5000

🧪 Running Tests
pytest -q


Includes test cases for:

Auth (login/register)

Movie APIs

TMDB integration

Watchlist system

⚡ CI/CD Pipeline (GitHub Actions)

The file .github/workflows/ci.yml performs:

✔ Install dependencies
✔ Prepare test environment
✔ Run all PyTest tests
✔ Auto-check code quality

Triggers on:

Every push

Every pull request

Manual run from Actions tab

🎥 Screenshots (Add your own)

You can add screenshots like:

![Home Page](screenshots/home.png)
![Movie Detail](screenshots/movie.png)
![Admin Panel](screenshots/admin.png)

👨‍💻 Team
Member	Role
Kushal Kumar	Backend + Integration
Member 2	Frontend
Member 3	TMDB Integration
Member 4	Documentation & Testing
🌟 Future Enhancements

🎭 Multi-user profiles

📊 Analytics dashboard

🧠 AI movie recommendation

🌐 Multi-language subtitles

📶 Resume watching

📝 License

MIT License © 2025
