const API_BASE = "http://127.0.0.1:5000/api";  // Flask backend URL

async function registerUser(name, email, password) {
  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  return res.json();
}

async function loginUser(email, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

async function getMovies(query = "") {
  const res = await fetch(`${API_BASE}/movies?search=${query}`);
  return res.json();
}
