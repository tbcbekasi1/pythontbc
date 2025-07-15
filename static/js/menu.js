(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector(".menu-toggle");
    const nav = document.querySelector("header nav");
    const icon = btn.querySelector("i");

    // Ensure initial state
    nav.classList.remove("open");
    icon.classList.add("fa-bars");
    icon.classList.remove("fa-times");

    btn.addEventListener("click", () => {
      const opened = nav.classList.toggle("open");
      if (opened) {
        icon.classList.replace("fa-bars", "fa-times");
      } else {
        icon.classList.replace("fa-times", "fa-bars");
      }
    });
  });
})();
