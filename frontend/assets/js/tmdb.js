const TMDB_KEY = "ec726bf0d6157607e751561eb4e9e097";
const TMDB_BASE = "https://api.themoviedb.org/3";

// Category endpoints
const CATEGORIES = {
    "Trending Now": `${TMDB_BASE}/trending/movie/day?api_key=${TMDB_KEY}`,
    "Top Rated": `${TMDB_BASE}/movie/top_rated?api_key=${TMDB_KEY}`,
    "Action Movies": `${TMDB_BASE}/discover/movie?api_key=${TMDB_KEY}&with_genres=28`,
    "Comedy Movies": `${TMDB_BASE}/discover/movie?api_key=${TMDB_KEY}&with_genres=35`,
    "Horror Movies": `${TMDB_BASE}/discover/movie?api_key=${TMDB_KEY}&with_genres=27`,
    "Romance Movies": `${TMDB_BASE}/discover/movie?api_key=${TMDB_KEY}&with_genres=10749`,
    "Sci-Fi Movies": `${TMDB_BASE}/discover/movie?api_key=${TMDB_KEY}&with_genres=878`,
};

// Fetch helper
async function tmdbFetch(url) {
    const res = await fetch(url);
    return res.json();
}

// Load Hero Banner (only if no local movies)
async function loadHeroBanner() {
    // Check if local movies have been loaded and if they exist
    // Wait a bit for local movies to load first
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Check if hero was already updated by local movies
    const heroTitle = document.getElementById("heroTitle");
    if (heroTitle && heroTitle.innerText !== "Featured") {
        // Hero already updated by local movies, skip TMDB
        return;
    }

    try {
        const trending = await tmdbFetch(CATEGORIES["Trending Now"]);
        const movie = trending.results[0];

        const hero = document.getElementById("hero");

        hero.style.backgroundImage =
            `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})`;

        document.getElementById("heroTitle").innerText = movie.title;
        document.getElementById("heroDesc").innerText =
            movie.overview.substring(0, 150) + "...";

        document.getElementById("playHero").onclick =
            () => window.location.href = "/movie/" + movie.id;

        document.getElementById("moreHero").onclick =
            () => window.location.href = "/movie/" + movie.id;
    } catch (error) {
        console.error("Error loading TMDB hero:", error);
    }
}

// Create movie card
function createMovieCard(movie) {
    const div = document.createElement("div");
    div.className = "movie-card";

    div.innerHTML = `
        <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" />
    `;

    div.onclick = () => window.location.href = `/movie/${movie.id}`;
    return div;
}

// Load movie rows
async function loadMovieRows() {
    const container = document.getElementById("movieRows");

    for (const [name, url] of Object.entries(CATEGORIES)) {
        const data = await tmdbFetch(url);

        const section = document.createElement("section");
        section.className = "movie-section";

        section.innerHTML = `
            <h2 class="row-title">${name}</h2>
            <div class="row-cards"></div>
        `;

        const rowDiv = section.querySelector(".row-cards");

        data.results.forEach(movie => {
            if (movie.poster_path) {
                rowDiv.appendChild(createMovieCard(movie));
            }
        });

        container.appendChild(section);
    }
}

// Initialize everything
async function initTMDB() {
    await loadHeroBanner();
    await loadMovieRows();
}

initTMDB();
