const API_BASE = "http://127.0.0.1:5000";

async function fetchMovies() {
  try {
    const r = await fetch(`${API_BASE}/movies/all`);
    const movies = await r.json();
    return movies;
  } catch (e) {
    console.error("Failed to load movies", e);
    return [];
  }
}

function makeCard(movie) {
  const div = document.createElement("div");
  div.className = "card";
  div.innerHTML = `
    <img src="${movie.poster || 'assets/images/placeholder.jpg'}" alt="${movie.title}" />
    <div class="meta">
      <div class="title">${movie.title}</div>
      <div class="genre">${movie.genre || ''}</div>
    </div>
  `;
  div.addEventListener("click", () => {
    window.location.href = `/movie/${movie.id}`;
  });
  return div;
}

async function renderHome() {
  const movies = await fetchMovies();
  const row = document.getElementById("moviesRow");
  row.innerHTML = "";
  if (!movies || movies.length === 0) {
    row.innerHTML = "<div style='color:#bbb'>No movies yet.</div>";
    return;
  }

  // hero pick
  const featured = movies[0];
  if (featured) {
    document.getElementById("heroTitle").innerText = featured.title;
    document.getElementById("heroDesc").innerText = featured.description || "";
    const heroEl = document.getElementById("hero");
    heroEl.style.backgroundImage = `url(${featured.poster || 'assets/images/hero.jpg'})`;
    document.getElementById("playHero").onclick = () => window.location.href = `/movie/${featured.id}`;
    document.getElementById("moreHero").onclick = () => window.location.href = `/movie/${featured.id}`;
  }

  movies.forEach(m => row.appendChild(makeCard(m)));
}

document.getElementById("searchInput").addEventListener("input", async (e) => {
  const q = e.target.value.trim();
  if (!q) {
    renderHome();
    return;
  }
  try {
    const r = await fetch(`${API_BASE}/movies/search?q=${encodeURIComponent(q)}`);
    const movies = await r.json();
    const row = document.getElementById("moviesRow");
    row.innerHTML = "";
    movies.forEach(m => row.appendChild(makeCard(m)));
  } catch (err) {
    console.error(err);
  }
});

// init
renderHome();
