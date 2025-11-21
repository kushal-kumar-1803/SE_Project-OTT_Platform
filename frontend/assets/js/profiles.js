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
    const previewAvatar = document.getElementById("previewAvatar");
    const previewName = document.getElementById("previewName");
    const previewBadge = document.getElementById("previewBadge");

    if (!grid) return;

    const avatars = grid.querySelectorAll(".avatar-img, img");
    avatars.forEach(img => {
        img.style.cursor = "pointer";
        img.addEventListener("click", () => {
            avatars.forEach(x => x.classList.remove("selected"));
            img.classList.add("selected");
            selectedAvatar = img.getAttribute("data-src") || img.src || "";
            if (previewAvatar) previewAvatar.src = selectedAvatar;
        });
    });

    const nameInput = document.getElementById("profileName");
    if (nameInput && previewName) {
        nameInput.addEventListener("input", () => {
            previewName.textContent = nameInput.value.trim() || "Your Name";
        });
    }

    const kidCheckbox = document.getElementById("isKid");
    if (kidCheckbox && previewBadge) {
        kidCheckbox.addEventListener("change", () => {
            previewBadge.hidden = !kidCheckbox.checked;
        });
    }

    const btn = document.getElementById("createBtn");
    if (!btn) return;

    btn.onclick = async () => {
        const name = document.getElementById("profileName").value.trim();
        const isKid = document.getElementById("isKid").checked;
        const user_id = getUserId();

        if (!user_id) {
            alert("Please login first.");
            return (window.location.href = "/login");
        }

        if (!name) return alert("Enter profile name");
        if (!selectedAvatar) return alert("Please select an avatar!");

        const payload = { user_id: parseInt(user_id), name, avatar: selectedAvatar, is_kid: isKid };

        const res = await fetch(`${API_BASE}/profiles/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (res.ok) {
            alert("Profile Created!");
            window.location.href = "/profiles";
        } else {
            alert(data.error || "Create failed");
        }
    };
}

// ---------------------------------
// RENDER PROFILE LIST
// ---------------------------------
async function renderProfilesPage() {
    const container = document.getElementById("profilesContainer");
    const noProfiles = document.getElementById("noProfiles");
    const user_id = getUserId();

    if (!user_id) {
        if (container) container.innerHTML = '<div>Please <a href="/login">login</a> to see profiles.</div>';
        return;
    }

    const res = await fetch(`${API_BASE}/profiles/list/${parseInt(user_id)}`);
    const data = await res.json();
    const profiles = data.profiles || [];

    if (!container) return;

    container.innerHTML = "";
    if (profiles.length === 0) {
        if (noProfiles) noProfiles.style.display = "block";
        return;
    }

    if (noProfiles) noProfiles.style.display = "none";

    profiles.forEach(p => {
        const card = document.createElement("div");
        card.className = "profile-card";
        card.style.width = "160px";
        card.style.textAlign = "center";

        const img = document.createElement("img");
        img.src = p.avatar || "/assets/images/avatar1.png";
        img.style.width = "140px";
        img.style.height = "140px";
        img.style.borderRadius = "12px";
        img.style.objectFit = "cover";

        const name = document.createElement("div");
        name.textContent = p.name;
        name.style.marginTop = "8px";

        const badge = document.createElement("div");
        badge.textContent = p.is_kid ? "Kids" : "";
        badge.style.color = "#777";

        card.appendChild(img);
        card.appendChild(name);
        card.appendChild(badge);

        container.appendChild(card);
    });
}

// ---------------------------------
// MANAGE PROFILES PAGE
// ---------------------------------
async function renderManageProfiles() {
    const container = document.getElementById("manageContainer");
    const user_id = getUserId();
    if (!container) return;
    if (!user_id) {
        container.innerHTML = '<div>Please <a href="/login">login</a> to manage profiles.</div>';
        return;
    }

    const res = await fetch(`${API_BASE}/profiles/list/${parseInt(user_id)}`);
    const data = await res.json();
    const profiles = data.profiles || [];

    container.innerHTML = "";
    profiles.forEach(p => {
        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.alignItems = "center";
        row.style.gap = "12px";
        row.style.marginBottom = "12px";

        const img = document.createElement("img");
        img.src = p.avatar || "/assets/images/avatar1.png";
        img.style.width = "80px";
        img.style.height = "80px";
        img.style.borderRadius = "8px";

        const info = document.createElement("div");
        info.innerHTML = `<strong>${p.name}</strong><br/><small>${p.is_kid ? 'Kids' : 'Standard'}</small>`;

        const del = document.createElement("button");
        del.textContent = "Delete";
        del.onclick = async () => {
            if (!confirm('Delete this profile?')) return;
            await fetch(`${API_BASE}/profiles/${p.id}/delete`, { method: 'POST' });
            renderManageProfiles();
        };

        row.appendChild(img);
        row.appendChild(info);
        row.appendChild(del);
        container.appendChild(row);
    });
}

// ---------------------------------
// PAGE AUTO-LOADER
// ---------------------------------
(function () {
    const path = window.location.pathname;
    if (path.includes("/profiles/create") || path.includes("profile_create")) {
        initCreateProfile();
    } else if (path === "/profiles" || path === "/profiles/") {
        renderProfilesPage();
    } else if (path.includes("/profiles/manage") || path.includes("manage_profiles")) {
        renderManageProfiles();
    }
})();
