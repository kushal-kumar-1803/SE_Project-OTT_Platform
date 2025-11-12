// Base API URL (change if your backend uses a different host/port)
const API_BASE = "http://127.0.0.1:5000/api";

// ✅ Access Protection for Admin Panel
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// Redirect non-admin users
if (!token || role !== "admin") {
  alert("Access denied! Admins only.");
  window.location.href = "login.html";
}

// ------------------------
// 🟢 Load Movies Function
// ------------------------
async function loadAdminMovies() {
  try {
    const res = await fetch(`${API_BASE}/movies`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error("Failed to fetch movies.");

    const movies = await res.json();
    const container = document.getElementById("adminMovieContainer");
    container.innerHTML = "";

    if (movies.length === 0) {
      container.innerHTML = "<p>No movies found in database.</p>";
      return;
    }

    movies.forEach(movie => {
      const card = document.createElement("div");
      card.className = "movie-card";
      card.innerHTML = `
        <img src="${movie.poster}" alt="${movie.title}">
        <h3>${movie.title}</h3>
        <p>${movie.genre}</p>
        <button onclick="deleteMovie('${movie.id}')">🗑 Delete</button>
      `;
      container.appendChild(card);
    });
  } catch (error) {
    console.error(error);
    alert("Error loading movies.");
  }
}

// ------------------------
// 🟢 Upload Movie Function
// ------------------------
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const movieData = {
    title: document.getElementById("title").value,
    genre: document.getElementById("genre").value,
    description: document.getElementById("description").value,
    poster: document.getElementById("poster").value,
    video_url: document.getElementById("video_url").value
  };

  try {
    const res = await fetch(`${API_BASE}/admin/upload`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(movieData)
    });

    if (res.ok) {
      alert("✅ Movie uploaded successfully!");
      document.getElementById("uploadForm").reset();
      loadAdminMovies();
    } else {
      const errorData = await res.json();
      alert("❌ Upload failed: " + (errorData.message || "Unknown error."));
    }
  } catch (error) {
    console.error(error);
    alert("Error uploading movie.");
  }
});

// ------------------------
// 🗑 Delete Movie Function
// ------------------------
async function deleteMovie(id) {
  if (confirm("Are you sure you want to delete this movie?")) {
    try {
      const res = await fetch(`${API_BASE}/admin/delete/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      if (res.ok) {
        alert("🗑 Movie deleted successfully!");
        loadAdminMovies();
      } else {
        const errData = await res.json();
        alert("❌ Error deleting movie: " + (errData.message || "Unknown error."));
      }
    } catch (error) {
      console.error(error);
      alert("Server error while deleting movie.");
    }
  }
}

// ------------------------
// 🔴 Logout Function
// ------------------------
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("user");
  alert("You have been logged out.");
  window.location.href = "login.html";
}

// ------------------------
// 🟢 Load Movies on Page Load
// ------------------------
window.onload = loadAdminMovies;
