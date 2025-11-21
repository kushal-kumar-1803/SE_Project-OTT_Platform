const TMDB_KEY = "ec726bf0d6157607e751561eb4e9e097";  // keep same key

const categories = [
  { title: "Trending Now", url: `/trending/all/week?api_key=${TMDB_KEY}` },
  { title: "Top Rated", url: `/movie/top_rated?api_key=${TMDB_KEY}` },
  { title: "Action Movies", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=28` },
  { title: "Comedy Movies", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=35` },
  { title: "Horror Movies", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=27` },
  { title: "Romance Movies", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=10749` },
  { title: "Sci-Fi Movies", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=878` },
  { title: "Animation", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=16` },
  { title: "Thriller", url: `/discover/movie?api_key=${TMDB_KEY}&with_genres=53` }
];

async function loadCategoryRows() {
  const container = document.getElementById("movie-sections");

  for (const section of categories) {
    const row = document.createElement("div");
    row.className = "movie-row";
    row.innerHTML = `
      <h2 class="row-title">${section.title}</h2>
      <div class="row-cards" id="${section.title.replace(/ /g, '_')}"></div>
    `;
    container.appendChild(row);

    const data = await fetch(`https://api.themoviedb.org/3${section.url}`);
    const json = await data.json();

    const rowDiv = document.getElementById(section.title.replace(/ /g, '_'));

    json.results.forEach(movie => {
      if (!movie.poster_path) return;

      const img = document.createElement("img");
      img.className = "movie-card";
      img.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
      img.title = movie.title || movie.name;

      img.addEventListener("click", () => {
        window.location.href = `/movie/${movie.id}`;
      });

      rowDiv.appendChild(img);
    });
  }
}

loadCategoryRows();
