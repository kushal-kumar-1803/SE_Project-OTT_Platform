
// ==========================================
// FILE 2: frontend/assets/js/admin.js
// ==========================================
const API_ADMIN = "http://127.0.0.1:5000/admin-api";

// ==========================================
// LOAD ALL MOVIES
// ==========================================
let moviesData = {}; // Store movie data for editing

async function loadMovies() {
    try {
        const res = await fetch(`${API_ADMIN}/movies/all`);
        const movies = await res.json();

        const list = document.getElementById("movieList");
        list.innerHTML = "";

        if (movies.length === 0) {
            list.innerHTML = "<p>No movies found. Add your first movie!</p>";
            return;
        }

        // Store movies data for easy access
        moviesData = {};
        movies.forEach(m => {
            moviesData[m.id] = m;
        });

        movies.forEach(m => {
            const card = document.createElement("div");
            card.className = "movie-card";
            card.innerHTML = `
                ${m.poster_url ? `<img src="${m.poster_url}" alt="${m.title}">` : '<div class="no-poster">No Image</div>'}
                <h3>${m.title}</h3>
                <p class="genre">${m.genre}</p>
                <p class="description">${m.description || 'No description'}</p>
                <div class="movie-actions">
                    <button class="delete-btn" onclick="deleteMovie(${m.id})">Delete</button>
                    <button class="edit-btn" onclick="editMovie(${m.id})">Edit</button>
                </div>
            `;
            list.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading movies:", error);
        alert("Failed to load movies");
    }
}

// ==========================================
// ADD MOVIE
// ==========================================
document.getElementById("addMovieForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const movie = {
        title: document.getElementById("title").value.trim(),
        genre: document.getElementById("genre").value.trim(),
        video_url: document.getElementById("video_url").value.trim(),
        poster_url: document.getElementById("poster_url").value.trim(),
        description: document.getElementById("description").value.trim()
    };

    // Validation
    if (!movie.title || !movie.genre || !movie.video_url) {
        alert("Please fill in all required fields");
        return;
    }

    try {
        const res = await fetch(`${API_ADMIN}/movies/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });

        const data = await res.json();
        
        if (res.ok) {
            alert(data.message || "Movie added successfully!");
            document.getElementById("addMovieForm").reset();
            loadMovies();
        } else {
            alert(data.error || "Failed to add movie");
        }
    } catch (error) {
        console.error("Error adding movie:", error);
        alert("Failed to add movie");
    }
});

// ==========================================
// DELETE MOVIE
// ==========================================
async function deleteMovie(id) {
    if (!confirm("Are you sure you want to delete this movie?")) {
        return;
    }

    try {
        const res = await fetch(`${API_ADMIN}/movies/delete/${id}`, {
            method: "DELETE"
        });

        const data = await res.json();
        
        if (res.ok) {
            alert(data.message || "Movie deleted successfully!");
            loadMovies();
        } else {
            alert(data.error || "Failed to delete movie");
        }
    } catch (error) {
        console.error("Error deleting movie:", error);
        alert("Failed to delete movie");
    }
}

// ==========================================
// EDIT MOVIE
// ==========================================
function editMovie(id) {
    const movie = moviesData[id];
    if (!movie) {
        alert("Movie not found!");
        return;
    }

    // Populate form with movie data
    document.getElementById("edit_movie_id").value = movie.id;
    document.getElementById("edit_title").value = movie.title || "";
    document.getElementById("edit_genre").value = movie.genre || "";
    document.getElementById("edit_video_url").value = movie.video_url || "";
    document.getElementById("edit_poster_url").value = movie.poster_url || "";
    document.getElementById("edit_description").value = movie.description || "";

    // Show modal
    document.getElementById("editMovieModal").style.display = "block";
}

// ==========================================
// CLOSE EDIT MODAL
// ==========================================
function closeEditModal() {
    document.getElementById("editMovieModal").style.display = "none";
    document.getElementById("editMovieForm").reset();
}

// ==========================================
// UPDATE MOVIE
// ==========================================
document.getElementById("editMovieForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const movieId = document.getElementById("edit_movie_id").value;
    const movie = {
        title: document.getElementById("edit_title").value.trim(),
        genre: document.getElementById("edit_genre").value.trim(),
        video_url: document.getElementById("edit_video_url").value.trim(),
        poster_url: document.getElementById("edit_poster_url").value.trim(),
        description: document.getElementById("edit_description").value.trim()
    };

    // Validation
    if (!movie.title || !movie.genre || !movie.video_url) {
        alert("Please fill in all required fields");
        return;
    }

    try {
        const res = await fetch(`${API_ADMIN}/movies/update/${movieId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(movie)
        });

        const data = await res.json();
        
        if (res.ok) {
            alert(data.message || "Movie updated successfully!");
            closeEditModal();
            loadMovies();
        } else {
            alert(data.error || "Failed to update movie");
        }
    } catch (error) {
        console.error("Error updating movie:", error);
        alert("Failed to update movie");
    }
});

// ==========================================
// MODAL EVENT LISTENERS
// ==========================================
// Close modal when clicking the X button
const closeBtn = document.querySelector(".close-modal");
if (closeBtn) {
    closeBtn.addEventListener("click", closeEditModal);
}

// Close modal when clicking outside the modal
window.addEventListener("click", (event) => {
    const modal = document.getElementById("editMovieModal");
    if (event.target === modal) {
        closeEditModal();
    }
});

// Load movies on page load
loadMovies();
