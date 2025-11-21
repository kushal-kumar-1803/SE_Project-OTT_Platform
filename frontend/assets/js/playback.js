async function loadMovieDetails() {
  const urlParams = new URLSearchParams(window.location.search);
  const movieId = urlParams.get("id");
  
  const res = await fetch(`${API_BASE}/movies/${movieId}`);
  const movie = await res.json();

  document.getElementById("title").textContent = movie.title;
  document.getElementById("description").textContent = movie.description;
  document.getElementById("poster").src = movie.poster;
  document.getElementById("videoSrc").src = movie.video_url;
}

window.onload = loadMovieDetails;
