function paginateTable(tableId, rowsPerPage) {
  const table = document.getElementById(tableId);
  if (!table) return;
  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));
  let currentPage = 1;
  const totalPages = Math.ceil(rows.length / rowsPerPage);
  const controls = document.getElementById("paginationControls");

  function render() {
    rows.forEach((row, i) => {
      row.style.display =
        i >= (currentPage - 1) * rowsPerPage && i < currentPage * rowsPerPage
          ? ""
          : "none";
    });
    renderControls();
  }

  function renderControls() {
    controls.innerHTML = "";
    // Prev button
    const prev = document.createElement("button");
    prev.textContent = "« Prev";
    prev.disabled = currentPage === 1;
    prev.onclick = () => {
      currentPage--;
      render();
    };
    controls.appendChild(prev);

    // nomor halaman
    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      btn.classList.toggle("active", i === currentPage);
      btn.onclick = () => {
        currentPage = i;
        render();
      };
      controls.appendChild(btn);
    }

    // Next button
    const next = document.createElement("button");
    next.textContent = "Next »";
    next.disabled = currentPage === totalPages;
    next.onclick = () => {
      currentPage++;
      render();
    };
    controls.appendChild(next);
  }

  render(); // tampilkan halaman pertama
}

document.addEventListener("DOMContentLoaded", () => {
  // pagination: misal 10 baris per halaman
  paginateTable("tbcTable", 5);
});
