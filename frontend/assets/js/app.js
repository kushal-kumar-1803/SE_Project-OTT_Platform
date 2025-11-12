async function loadMovies() {
  const movies = await getMovies();
  const container = document.getElementById("movieContainer");
  container.innerHTML = "";

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.className = "movie-card";
    card.innerHTML = `
      <img src="${movie.poster}" alt="${movie.title}">
      <h3>${movie.title}</h3>
      <p>${movie.genre}</p>
      <button onclick="viewMovie('${movie.id}')">View</button>
    `;
    container.appendChild(card);
  });
}

function viewMovie(id) {
  window.location.href = `movie_detail.html?id=${id}`;
}

function searchMovies() {
  const query = document.getElementById("searchBar").value;
  getMovies(query).then(displayMovies);
}

window.onload = loadMovies;
