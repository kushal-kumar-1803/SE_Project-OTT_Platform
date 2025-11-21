// Search bar for TMDB + Local DB with ENTER to open first result

(function () {
    const input = document.getElementById("searchInput");
    if (!input) return;

    const resultsBox = document.createElement("div");
    resultsBox.id = "searchResultsBox";
    resultsBox.style.position = "absolute";
    resultsBox.style.right = "160px";
    resultsBox.style.top = "60px";
    resultsBox.style.background = "#111";
    resultsBox.style.border = "1px solid #333";
    resultsBox.style.maxHeight = "400px";
    resultsBox.style.overflow = "auto";
    resultsBox.style.width = "320px";
    resultsBox.style.display = "none";
    resultsBox.style.zIndex = "9999";
    document.body.appendChild(resultsBox);

    let lastResults = []; // store results for ENTER key
    let delayTimer = null;

    input.addEventListener("input", () => {
        clearTimeout(delayTimer);
        const q = input.value.trim();

        if (!q) {
            resultsBox.style.display = "none";
            return;
        }

        delayTimer = setTimeout(() => doSearch(q), 350);
    });

    // 🎯 ENTER key → open first movie result
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            if (lastResults.length > 0) {
                window.location.href = `/movie/${lastResults[0].id}`;
            }
        }
    });

    async function doSearch(q) {
        resultsBox.innerHTML = "<div style='padding:10px'>Searching…</div>";
        resultsBox.style.display = "block";

        try {
            // 🔥 TMDB SEARCH endpoint
            const r = await fetch(`/movies/tmdb_search?q=${encodeURIComponent(q)}`);
            const data = await r.json();

            lastResults = data.results || [];
            resultsBox.innerHTML = "";

            if (lastResults.length === 0) {
                resultsBox.innerHTML = "<div style='padding:10px'>No results found</div>";
                return;
            }

            lastResults.slice(0, 7).forEach(movie => {
                const poster = movie.poster || "/assets/images/placeholder.jpg";

                const row = document.createElement("div");
                row.style.padding = "8px";
                row.style.borderBottom = "1px solid #222";
                row.style.cursor = "pointer";
                row.style.display = "flex";
                row.style.alignItems = "center";

                row.innerHTML = `
                    <img src="${poster}"
                         style="width:40px;height:60px;object-fit:cover;border-radius:3px;margin-right:10px" />
                    <span>${movie.title}</span>
                `;

                row.onclick = () => window.location.href = `/movie/${movie.id}`;

                resultsBox.appendChild(row);
            });

        } catch (err) {
            resultsBox.innerHTML = "<div style='padding:10px'>Error fetching results</div>";
            console.error(err);
        }
    }

    // hide results when clicking outside
    document.addEventListener("click", (ev) => {
        if (!resultsBox.contains(ev.target) && ev.target !== input) {
            resultsBox.style.display = "none";
       }
    });

})();