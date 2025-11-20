// =========================
//  API BASE
// =========================
const API_BASE = "http://127.0.0.1:5000";


// =========================
//  LOGOUT
// =========================
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.clear();
        alert("Logged out!");
        window.location.href = "/login";
    });
}


// =========================
//  LOAD MOVIES
// =========================
async function loadMovies() {
    const movieList = document.getElementById("movieList");
    if (!movieList) return;

    movieList.innerHTML = "<p style='color:#bbb;'>Loading...</p>";

    const res = await fetch(`${API_BASE}/movies/all`);
    const movies = await res.json();

    movieList.innerHTML = "";

    movies.forEach(movie => {
        movieList.innerHTML += `
            <div class="admin-movie-card">
                <img src="${movie.poster_url}">
                <h3>${movie.title}</h3>
                <p>${movie.genre}</p>
                <button onclick="openEditModal(${movie.id})">Edit</button>
            </div>
        `;
    });
}


// =========================
//  LOAD PENDING SUBSCRIPTIONS
// =========================
async function loadPayments() {
    const tableBody = document.getElementById("paymentBody");
    if (!tableBody) return;

    tableBody.innerHTML = `
        <tr><td colspan="5" style="text-align:center;color:#bbb;">Loading...</td></tr>
    `;

    const res = await fetch(`${API_BASE}/subscriptions/pending`);
    const data = await res.json();

    console.log("Pending:", data);

    tableBody.innerHTML = "";

    if (!data.length) {
        tableBody.innerHTML = `
            <tr><td colspan="5" style="text-align:center;color:#bbb;">No pending subscriptions</td></tr>
        `;
        return;
    }

    data.forEach(sub => {
        tableBody.innerHTML += `
            <tr>
                <td>${sub.user_id}</td>
                <td>${sub.plan}</td>
                <td>₹${sub.plan === "Standard" ? 299 : sub.plan === "Premium" ? 499 : 799}</td>
                <td>${sub.status}</td>
                <td>
                    <button class="approve-btn" onclick="approvePayment(${sub.id})">
                        Approve
                    </button>
                </td>
            </tr>
        `;
    });
}


// =========================
//  APPROVE SUBSCRIPTION
// =========================
window.approvePayment = async function (subId) {
    const res = await fetch(`${API_BASE}/subscriptions/approve/${subId}`, {
        method: "PUT"
    });

    const data = await res.json();

    if (data.success) {
        alert("Subscription Approved!");
        loadPayments();
    } else {
        alert("Failed: " + data.error);
    }
};


// INIT
if (document.getElementById("movieList")) loadMovies();
if (document.getElementById("paymentBody")) loadPayments();
