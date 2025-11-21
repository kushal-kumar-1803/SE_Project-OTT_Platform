const TMDB_KEY = "ec726bf0d6157607e751561eb4e9e097";

async function loadFeaturedMovie() {
    try {
        const res = await fetch(
            `https://api.themoviedb.org/3/trending/movie/day?api_key=${TMDB_KEY}`
        );
        const data = await res.json();

        if (!data.results || data.results.length === 0) return;

        const movie = data.results[0];

        // Elements
        const featuredSection = document.getElementById("featured-section");
        const featuredTitle = document.getElementById("featured-title");
        const featuredDesc = document.getElementById("featured-description");

        // Background image
        featuredSection.style.backgroundImage = `
            url(https://image.tmdb.org/t/p/original${movie.backdrop_path})
        `;

        // Title & Description
        featuredTitle.innerText = movie.title || movie.name;
        featuredDesc.innerText = movie.overview?.slice(0, 150) + "...";

    } catch (error) {
        console.error("Featured section error:", error);
    }
}

loadFeaturedMovie();
