// frontend/assets/js/movie_detail.js
// This file expects backend endpoint at /movies/<id> and /movies/<id>/similar (optional)

(function () {
  function getMovieIdFromPath() {
    // path like /movie/123
    const parts = window.location.pathname.split("/");
    return parts[parts.length - 1] || parts[parts.length - 2];
  }

  async function fetchJSON(url) {
    const r = await fetch(url);
    return r.json();
  }

  async function loadDetail() {
    const id = getMovieIdFromPath();
    if (!id) {
      console.error("No movie id found in path");
      return;
    }

    const detail = await fetchJSON(`/movies/${id}`);
    if (detail.error) {
      console.error(detail);
      alert("Failed to load movie details.");
      return;
    }

    document.getElementById("detail-title").innerText = detail.title;
    document.getElementById("detail-overview").innerText = detail.overview;
    document.getElementById("detail-genres").innerText = (detail.genres || []).join(", ");
    document.getElementById("detail-release").innerText = detail.release_date || "N/A";
    document.getElementById("detail-rating").innerText = detail.vote_average || "N/A";
    document.getElementById("detail-poster").src = detail.poster || "/assets/images/placeholder.jpg";
    document.getElementById("detail-backdrop").style.backgroundImage = `url(${detail.backdrop || detail.poster})`;

    document.getElementById("playBtn").onclick = () => {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please login to play content.");
        window.location.href = "/login";
        return;
      }
      alert("Play (demo) for movie: " + detail.title);
    };

    document.getElementById("watchlistBtn").onclick = () => {
      const stored = JSON.parse(localStorage.getItem("watchlist") || "[]");
      if (stored.includes(detail.id)) {
        // remove
        const newList = stored.filter(i => i !== detail.id);
        localStorage.setItem("watchlist", JSON.stringify(newList));
        document.getElementById("watchlistBtn").innerText = "Add to Watchlist";
      } else {
        stored.push(detail.id);
        localStorage.setItem("watchlist", JSON.stringify(stored));
        document.getElementById("watchlistBtn").innerText = "Remove from Watchlist";
      }
    };

    // update watchlist button label
    const watchlist = JSON.parse(localStorage.getItem("watchlist") || "[]");
    document.getElementById("watchlistBtn").innerText = watchlist.includes(detail.id) ? "Remove from Watchlist" : "Add to Watchlist";

    // optionally: load similar movies via TMDB raw data, but backend doesn't expose similar by default.
    // For speed, we skip similar; you can call TMDB directly from frontend if desired.
  }

  loadDetail();
})();
