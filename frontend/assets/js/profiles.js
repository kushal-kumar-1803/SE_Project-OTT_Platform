const API_BASE = "http://127.0.0.1:5000";

function getUserId() {
    return localStorage.getItem("user_id");
}

// ---------------------------------
// CREATE PROFILE PAGE
// ---------------------------------
function initCreateProfile() {
    const grid = document.getElementById("avatarGrid");
    let selectedAvatar = "";

    // Defensive: ensure grid exists
    if (!grid) {
        console.error("avatarGrid element not found");
        return;
    }

    // Select avatar (use .avatar-img so we only target intended images)
    const avatars = grid.querySelectorAll(".avatar-img, img");
    avatars.forEach(img => {
        // make sure cursor indicates clickability
        img.style.cursor = "pointer";

        img.addEventListener("click", (e) => {
            // remove class from all avatars in the grid
            avatars.forEach(x => x.classList.remove("selected"));

            // toggle selected class on the clicked image
            img.classList.add("selected");

            // prefer data-src attribute, fallback to src
            selectedAvatar = img.getAttribute("data-src") || img.src || "";
                    console.log("Selected Avatar:", selectedAvatar);
        });
    });

    // Create profile button
    document.getElementById("createBtn").onclick = async () => {
        const name = document.getElementById("profileName").value.trim();
        const isKid = document.getElementById("isKid").checked;
        const user_id = getUserId();

        if (!user_id) {
            alert("Please login first.");
            return (window.location.href = "/login");
        }

        if (!name) {
            alert("Enter profile name");
            return;
        }

        if (!selectedAvatar) {
            alert("Please select an avatar!");
            return;
        }

        const payload = {
            user_id: parseInt(user_id),
            name,
            avatar: selectedAvatar,
            is_kid: isKid
        };

        console.log("Sending payload:", payload);

        const res = await fetch(`${API_BASE}/profiles/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        console.log("Response:", data);

        if (res.ok) {
            alert("Profile Created!");
            window.location.href = "/profiles";
        } else {
            alert(data.error || "Create failed");
        }
    };
}

// ---------------------------------
// PAGE AUTO-LOADER
// ---------------------------------
(function () {
    const path = window.location.pathname;

    // Support multiple possible paths that serve the profile-create page.
    // The Flask route serves `profile_create.html` at `/profiles/create`.
    if (path.includes("/profiles/create") || path.includes("profile_create")) {
        console.log("profiles.js: initializing create-profile page");
        initCreateProfile();
    }
})();
