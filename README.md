<h1 align="center">🎬 <strong>OTT Streaming Platform</strong></h1>
<p align="center"><em>A modern, Netflix-inspired OTT system built with Flask, SQLite, and TMDB API.</em></p> <br> <p align="center"> <img src="https://img.shields.io/badge/Framework-Flask-black?style=for-the-badge&logo=flask"> <img src="https://img.shields.io/badge/Database-SQLite-07405E?style=for-the-badge&logo=sqlite"> <img src="https://img.shields.io/badge/CI/CD-GitHub%20Actions-2F80ED?style=for-the-badge&logo=githubactions"> <img src="https://img.shields.io/badge/API-TMDB-01B4E4?style=for-the-badge&logo=themoviedatabase"> </p> <br>
<h2>✨ Overview</h2>

A full-stack OTT platform where users can:
✔ Watch movies
✔ Explore trending films
✔ Add movies to a personal watchlist
✔ Access premium content using a subscription system

Admins get tools to upload movies, manage posters, control subscriptions, and monitor the platform.

<br>
<h2>🚀 Features</h2>
<h3>🎯 User Features</h3>

🔐 Secure Login & Register

🎞 Watch uploaded movies (MP4 streaming)

⭐ Add/remove movies from My Watchlist

🔍 Search movies instantly

🎬 TMDB trending & categories

💳 Subscription-based movie access

<br>
<h3>🛠 Admin Features</h3>

🎥 Upload MP4 movies

🖼 Upload posters

📁 Edit or delete movies

📜 Approve subscription payments

🔄 Automatic refresh on user side

<br>
<h3>🤖 Developer Features</h3>

🧪 PyTest integration

⚙️ GitHub Actions CI

🧹 Clean backend structure

🔐 JWT authentication

<br>
<h2>📁 Project Structure</h2>
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
│   ├── assets/css/
│   ├── assets/js/
│   └── assets/videos/      ← (ignored in git)
│
│── requirements.txt
│── README.md
│── .gitignore
│── .github/workflows/ci.yml

<br>
<h2>⚙️ Installation Guide</h2>
<h3>1️⃣ Clone the Repository</h3>
git clone https://github.com/<username>/SE_Project-OTT_Platform.git
cd SE_Project-OTT_Platform

<br>
<h3>2️⃣ Create Virtual Environment</h3>
python -m venv venv
venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

<br>
<h3>3️⃣ Install Dependencies</h3>
pip install -r requirements.txt

<br>
<h3>4️⃣ Initialize the Database</h3>
python -c "from backend.database.db_connection import init_db; init_db()"

<br>
<h3>5️⃣ Run the Server</h3>
python -m backend.app


👉 App will run at: http://127.0.0.1:5000

<br>
<h2>🧪 Running Tests</h2>
pytest -q


Includes automated tests for:
✔ Authentication
✔ Movies API
✔ TMDB integration
✔ Watchlist
✔ Subscription system

<br>
<h2>⚡ CI/CD Pipeline (GitHub Actions)</h2>

Your pipeline checks:

🧪 PyTest

📦 Dependency installation

✔ Code correctness

🔧 Clean execution

Triggers on:

Push

Pull Request

Manual Run

File:

.github/workflows/ci.yml

<br>
<h2>👨‍💻 Team</h2>
Member
Kushal Kumar - Backend + Integration
Laasya R - Frontend and admin panel
Mohammed Sadatullah - User registration and forgot password
Mohin Nayumsab - Testing & Docs
<br>
<h2>🌟 Future Enhancements</h2>

🎭 Profile-based recommendations

🧪 Automated load testing

📊 Admin analytics dashboard

🎞 Subtitle support

📱 Mobile app

<br>
<h2>📝 License</h2>

MIT License © 2025 — FilmAura OTT
