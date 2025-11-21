console.log("MOVIE DETAIL JS LOADED");

// ============================
// HELPER FUNCTIONS
// ============================

function getMovieId() {
    const parts = window.location.pathname.split("/");
    const id = parts.pop() || parts.pop(); // handles trailing slash
    return id;
}

async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        return await res.json();
    } catch (err) {
        console.error("Fetch Error:", err);
        return {};
    }
}

// NEW — Check subscription via backend API
async function checkSubscription() {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        console.warn("User not logged in, redirecting to login.");
        window.location.href = "/login";
        return false;
    }

    try {
        const res = await fetch(`/subscriptions/status/${userId}`);
        const data = await res.json();

        console.log("Subscription API Response:", data);
        return data.subscribed === true;

    } catch (err) {
        console.error("Subscription check error:", err);
        return false;
    }
}


// ============================
// MAIN LOGIC
// ============================
(async () => {
    const id = getMovieId();
    console.log("Movie ID:", id);

    // Load Movie Detail
    const detail = await fetchJSON(`/movies/${id}`);
    console.log("Movie Detail:", detail);

    if (!detail || detail.error) {
        alert("Failed to load movie details.");
        return;
    }

    // --- SAFE DOM SETTER ---
    const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.innerText = value || "";
    };

    // Fill Movie Data
    setText("detail-title", detail.title);
    setText("detail-genres", (detail.genres || []).join(", "));
    setText("detail-overview", detail.overview);
    setText("detail-release", detail.release_date);
    setText("detail-rating", detail.rating);

    // Poster
    const posterEl = document.getElementById("detail-poster");
    if (posterEl) posterEl.src = detail.poster;

    // Backdrop
    const backdropEl = document.getElementById("detail-backdrop");
    if (backdropEl) {
        backdropEl.style.backgroundImage = `url(${detail.backdrop || detail.poster})`;
    }


    // ============================
    // PLAY TRAILER
    // ============================
    const trailerBtn = document.getElementById("playTrailerBtn");
    if (trailerBtn) {
        trailerBtn.onclick = async () => {
            const trailer = await fetchJSON(`/movies/trailer/${id}`);

            if (!trailer || !trailer.youtube_key) {
                alert("Trailer not available.");
                return;
            }

            window.open(`https://www.youtube.com/watch?v=${trailer.youtube_key}`, "_blank");
        };
    }


    // ============================
    // PLAY MOVIE  (Subscription Check)
    // ============================
    const playMovieBtn = document.getElementById("playMovieBtn");

    if (playMovieBtn) {
        playMovieBtn.onclick = async () => {
            console.log("Checking subscription...");

            const allowed = await checkSubscription();
            console.log("Subscription Allowed:", allowed);

            if (!allowed) {
                alert("Please subscribe to watch full movies.");
                window.location.href = "/subscribe";
                return;
            }

            // SUCCESS → Play movie
            window.location.href = `/movies/stream/${id}`;
        };
    }


    // ============================
    // WATCHLIST FEATURE
    // ============================
    const watchlistBtn = document.getElementById("watchlistBtn");

    if (watchlistBtn) {
        watchlistBtn.onclick = () => {
            let list = JSON.parse(localStorage.getItem("watchlist") || "[]");
            const movieId = String(id);

            if (!list.includes(movieId)) {
                list.push(movieId);
                watchlistBtn.innerText = "Remove from Watchlist";
                alert("Added to watchlist!");
            } else {
                list = list.filter(x => x !== movieId);
                watchlistBtn.innerText = "Add to Watchlist";
                alert("Removed from watchlist.");
            }

            localStorage.setItem("watchlist", JSON.stringify(list));
        };

        // Initialize button text
        const stored = JSON.parse(localStorage.getItem("watchlist") || "[]");
        if (stored.includes(String(id))) {
            watchlistBtn.innerText = "Remove from Watchlist";
        }
    }

})();
