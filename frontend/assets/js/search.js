// frontend/assets/js/search.js
// Attach to search input on index.html. Uses backend endpoint GET /movies/search?q=...

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
  document.body.appendChild(resultsBox);

  let timeout = null;
  input.addEventListener("input", (e) => {
    clearTimeout(timeout);
    const q = e.target.value.trim();
    if (!q) {
      resultsBox.style.display = "none";
      return;
    }
    timeout = setTimeout(() => doSearch(q), 350);
  });

  async function doSearch(q) {
    resultsBox.innerHTML = "<div style='padding:10px'>Searching…</div>";
    resultsBox.style.display = "block";
    try {
      const r = await fetch(`/movies/search?q=${encodeURIComponent(q)}`);
      const data = await r.json();
      resultsBox.innerHTML = "";
      if (!data.results || data.results.length === 0) {
        resultsBox.innerHTML = "<div style='padding:10px'>No results</div>";
        return;
      }
      data.results.slice(0, 7).forEach(m => {
        const row = document.createElement("div");
        row.style.padding = "8px";
        row.style.borderBottom = "1px solid #222";
        row.style.cursor = "pointer";
        row.innerHTML = `<img src="${m.poster || '/assets/images/placeholder.jpg'}" style="width:40px;height:60px;object-fit:cover;margin-right:8px;vertical-align:middle;border-radius:3px"/> <span style="vertical-align:middle">${m.title}</span>`;
        row.onclick = () => window.location.href = `/movie/${m.id}`;
        resultsBox.appendChild(row);
      });
    } catch (err) {
      resultsBox.innerHTML = "<div style='padding:10px'>Search failed</div>";
      console.error(err);
    }
  }

  // click outside hides box
  document.addEventListener("click", (ev) => {
    if (!resultsBox.contains(ev.target) && ev.target !== input) {
      resultsBox.style.display = "none";
    }
  });
})();
