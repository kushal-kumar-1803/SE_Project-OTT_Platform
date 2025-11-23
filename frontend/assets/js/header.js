// frontend/assets/js/header.js
(function () {
  const loginLink = document.getElementById("loginLink");
  const logoutBtn = document.getElementById("logoutBtn");
  const adminLink = document.getElementById("adminLink");
  const homeLink = document.getElementById("homeLink");
  
  if (!loginLink) return;

  function updateHeader() {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    
    if (token) {
      // User is logged in - show Home and Logout, hide Login and Admin
      if (homeLink) {
        homeLink.style.display = "block";
      }
      if (loginLink) {
        loginLink.style.display = "none";
      }
      if (adminLink) {
        adminLink.style.display = "none";
      }
      if (logoutBtn) {
        logoutBtn.style.display = "block";
      }
    } else {
      // User is not logged in - show Login and Admin, hide Home and Logout
      if (homeLink) {
        homeLink.style.display = "none";
      }
      if (loginLink) {
        loginLink.style.display = "block";
        loginLink.innerText = "Login";
        loginLink.href = "/login";
        loginLink.onclick = null;
      }
      if (adminLink) {
        adminLink.style.display = "block";
      }
      if (logoutBtn) {
        logoutBtn.style.display = "none";
      }
    }
  }

  // Handle logout button click
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.clear();
      alert("Logged out successfully!");
      window.location.href = "/login";
    });
  }

  updateHeader();
})();
