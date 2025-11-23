// Load admin-added movies from local database
const API_BASE = "http://127.0.0.1:5000";
let hasLocalMovies = false;

async function loadLocalMovies() {
    try {
        const res = await fetch(`${API_BASE}/movies/all`);
        const movies = await res.json();
        
        if (!movies || movies.length === 0) {
            hasLocalMovies = false;
            return; // No local movies to show
        }

        hasLocalMovies = true;
        const container = document.getElementById("movieRows");
        
        // Create a section for local movies
        const section = document.createElement("section");
        section.className = "movie-section";
        section.innerHTML = `
            <h2 class="row-title">Platform Movies</h2>
            <div class="row-cards" id="localMoviesRow"></div>
        `;
        
        // Insert at the beginning
        container.insertBefore(section, container.firstChild);
        
        const rowDiv = document.getElementById("localMoviesRow");
        
        movies.forEach(movie => {
            const card = createLocalMovieCard(movie);
            rowDiv.appendChild(card);
        });

        // Update hero banner with first local movie if available
        if (movies.length > 0) {
            const featured = movies[0];
            updateHeroBanner(featured);
        }
    } catch (error) {
        console.error("Error loading local movies:", error);
        hasLocalMovies = false;
    }
}

function createLocalMovieCard(movie) {
    const div = document.createElement("div");
    div.className = "movie-card";

    const posterUrl = movie.poster_url || '';
    
    if (posterUrl) {
        div.innerHTML = `
            <img src="${posterUrl}" alt="${movie.title}" onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'padding:20px;text-align:center;color:#666\\'>No Image</div>';" />
        `;
    } else {
        div.innerHTML = `
            <div style="width:100%;height:260px;background:#333;display:flex;align-items:center;justify-content:center;color:#666;border-radius:6px;">
                No Image
            </div>
        `;
    }

    div.onclick = () => {
        // Navigate to movie detail page
        window.location.href = `/movie/${movie.id}`;
    };
    
    return div;
}

function updateHeroBanner(movie) {
    const hero = document.getElementById("hero");
    const heroTitle = document.getElementById("heroTitle");
    const heroDesc = document.getElementById("heroDesc");
    const playHero = document.getElementById("playHero");
    const moreHero = document.getElementById("moreHero");

    if (hero && movie.poster_url) {
        hero.style.backgroundImage = `url(${movie.poster_url})`;
        hero.style.backgroundSize = "cover";
        hero.style.backgroundPosition = "center";
    }
    
    if (heroTitle) heroTitle.innerText = movie.title || "Featured";
    if (heroDesc) {
        const desc = movie.description || "";
        heroDesc.innerText = desc.length > 150 ? desc.substring(0, 150) + "..." : desc;
    }
    
    if (playHero) {
        playHero.onclick = () => window.location.href = `/movie/${movie.id}`;
    }
    if (moreHero) {
        moreHero.onclick = () => window.location.href = `/movie/${movie.id}`;
    }
}

// Load local movies when page loads
loadLocalMovies();

