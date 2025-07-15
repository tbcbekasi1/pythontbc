(function () {
  const sel = document.getElementById("langSelector");
  const dropdown = document.getElementById("langDropdown");
  const label = document.getElementById("selectedLangText");
  const toastCon = document.getElementById("toastContainer");

  function open() {
    sel.classList.add("active");
    sel.setAttribute("aria-expanded", "true");
  }
  function close() {
    sel.classList.remove("active");
    sel.setAttribute("aria-expanded", "false");
  }

  sel.addEventListener("click", (e) => {
    e.stopPropagation();
    sel.classList.contains("active") ? close() : open();
  });
  document.addEventListener("click", close);
  sel.addEventListener("keydown", (e) => {
    if (["Enter", " "].includes(e.key)) {
      e.preventDefault();
      sel.classList.contains("active") ? close() : open();
    } else if (e.key === "Escape") {
      close();
      sel.focus();
    }
  });

  dropdown.querySelectorAll("li").forEach((item) => {
    item.addEventListener("click", () => {
      const lang = item.textContent.trim();
      label.innerHTML = `${lang} <i class="fas fa-chevron-down"></i>`;
      close();
      showToast(`Bahasa diubah jadi: ${lang}`);
    });
    item.addEventListener("keydown", (e) => {
      if (["Enter", " "].includes(e.key)) {
        e.preventDefault();
        item.click();
      }
    });
  });

  // Fungsi bikin dan show toast
  function showToast(message, duration = 3000) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `
      <span>${message}</span>
      <button class="close-btn" aria-label="Tutup">&times;</button>
    `;
    // close button
    toast.querySelector(".close-btn").onclick = () => removeToast(toast);
    toastCon.appendChild(toast);
    // tampilkan
    requestAnimationFrame(() => toast.classList.add("show"));
    // auto-remove
    setTimeout(() => removeToast(toast), duration);
  }

  function removeToast(toast) {
    toast.classList.remove("show");
    toast.addEventListener("transitionend", () => toast.remove(), {
      once: true,
    });
  }
})();
