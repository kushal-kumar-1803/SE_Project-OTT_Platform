// frontend/assets/js/header.js
(function () {
  const loginLink = document.getElementById("loginLink");
  if (!loginLink) return;

  function updateHeader() {
    const token = localStorage.getItem("token");
    if (token) {
      loginLink.innerText = "Logout";
      loginLink.href = "#";
      loginLink.onclick = (e) => {
        e.preventDefault();
        localStorage.removeItem("token");
        window.location.reload();
      };
    } else {
      loginLink.innerText = "Login";
      loginLink.href = "/login";
      loginLink.onclick = null;
    }
  }

  updateHeader();
})();
