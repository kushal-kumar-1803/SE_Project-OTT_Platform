const API_BASE_ADMIN = "http://127.0.0.1:5000";

function getAuthHeaders(){
  const token = localStorage.getItem("token");
  return token ? { "Authorization": `Bearer ${token}`, "Content-Type":"application/json" } : { "Content-Type":"application/json" };
}

async function loadAdminMovies(){
  const r = await fetch(`${API_BASE_ADMIN}/movies/all`);
  const movies = await r.json();
  const container = document.getElementById("adminMovies");
  container.innerHTML = "";
  movies.forEach(m => {
    const el = document.createElement("div");
    el.className = "admin-movie";
    el.innerHTML = `<div><strong>${m.title}</strong> <div style="color:#999">${m.genre}</div></div>
    <div>
      <button class="del" data-id="${m.id}">Delete</button>
    </div>`;
    container.appendChild(el);
  });

  // attach delete handlers
  document.querySelectorAll("#adminMovies .del").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      if (!confirm("Delete movie #" + id + "?")) return;
      const res = await fetch(`${API_BASE_ADMIN}/admin/delete/${id}`, {
        method: "DELETE",
        headers: getAuthHeaders()
      });
      const data = await res.json();
      alert(JSON.stringify(data));
      loadAdminMovies();
    });
  });
}

document.getElementById("addMovieForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const genre = document.getElementById("genre").value;
  const description = document.getElementById("description").value;
  const video_url = document.getElementById("video_url").value;

  const res = await fetch(`${API_BASE_ADMIN}/admin/add`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ title, genre, description, video_url })
  });
  const data = await res.json();
  alert(JSON.stringify(data));
  loadAdminMovies();
});

document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "/";
});

// init admin page
loadAdminMovies();
