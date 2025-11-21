const TMDB_KEY = "ec726bf0d6157607e751561eb4e9e097";
const TMDB_BASE = "https://api.themoviedb.org/3";

function getMovieIdFromPath() {
    const parts = window.location.pathname.split("/");
    return parts[2];
}

async function loadMovie() {
    const id = getMovieIdFromPath();
    const url = `${TMDB_BASE}/movie/${id}?api_key=${TMDB_KEY}`;
    const m = await fetch(url).then(r => r.json());

    document.getElementById("movieTitle").innerText = m.title;
    document.getElementById("movieGenre").innerText = m.genres.map(g => g.name).join(", ");
    document.getElementById("movieDesc").innerText = m.overview;

    document.querySelector(".detail-card").style.backgroundImage =
        `url(https://image.tmdb.org/t/p/original${m.backdrop_path})`;

    document.getElementById("playBtn").onclick = () =>
        alert("Playing: " + m.title + " (demo)");

    document.getElementById("subscribeBtn").onclick = () =>
        alert("Subscriptions coming soon!");
}

loadMovie();
