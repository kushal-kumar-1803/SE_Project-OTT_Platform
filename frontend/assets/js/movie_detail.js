console.log("MOVIE DETAIL JS LOADED");

// -------- Helpers --------
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

// -------- Main Logic --------
(async () => {
    const id = getMovieId();
    console.log("Movie ID:", id);

    // Load Movie Details
    const detail = await fetchJSON(`/movies/${id}`);
    console.log("Movie Detail:", detail);

    if (!detail || detail.error) {
        alert("Failed to load movie details.");
        return;
    }

    // Safe-fill DOM elements
    const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.innerText = value || "";
    };

    // Fill Text Data
    setText("detail-title", detail.title);
    setText("detail-genres", (detail.genres || []).join(", "));
    setText("detail-overview", detail.overview);
    setText("detail-release", detail.release_date);
    setText("detail-rating", detail.rating);

    // Poster
    const posterEl = document.getElementById("detail-poster");
    if (posterEl) posterEl.src = detail.poster;

    // Backdrop Fix
    const backdropEl = document.getElementById("detail-backdrop");
    if (backdropEl) {
        backdropEl.style.backgroundImage = `url(${detail.backdrop || detail.poster})`;
    }

    // -------- PLAY TRAILER --------
    const trailerBtn = document.getElementById("playTrailerBtn");
    if (trailerBtn) {
        trailerBtn.onclick = async () => {
            console.log("Trailer button clicked!");

            const trailer = await fetchJSON(`/movies/trailer/${id}`);
            console.log("Trailer response:", trailer);

            if (!trailer || !trailer.youtube_key) {
                alert("Trailer not available for this movie.");
                return;
            }

            const url = `https://www.youtube.com/watch?v=${trailer.youtube_key}`;
            console.log("Opening Trailer URL:", url);

            window.open(url, "_blank");
        };
    }

    // -------- PLAY MOVIE --------
    const playMovieBtn = document.getElementById("playMovieBtn");
    if (playMovieBtn) {
        playMovieBtn.onclick = () => {
            const subscribed = localStorage.getItem("is_subscribed");
            console.log("Subscription Status:", subscribed);

            if (subscribed !== "1") {
                alert("Please subscribe to watch full movies.");
                window.location.href = "/subscribe";
                return;
            }

            window.location.href = `/movies/stream/${id}`;
        };
    }

    // -------- WATCHLIST --------
    const watchlistBtn = document.getElementById("watchlistBtn");
    if (watchlistBtn) {
        watchlistBtn.onclick = () => {
            let list = JSON.parse(localStorage.getItem("watchlist") || "[]");

            // Convert id to string for consistency
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

        // Pre-set watchlist button text
        const userList = JSON.parse(localStorage.getItem("watchlist") || "[]");
        if (userList.includes(String(id))) {
            watchlistBtn.innerText = "Remove from Watchlist";
        }
    }

})();
