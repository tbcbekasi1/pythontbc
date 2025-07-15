(function () {
  const slides = document.querySelector(".slides");
  const prevBtn = document.querySelector(".slider-btn-prev");
  const nextBtn = document.querySelector(".slider-btn-next");
  const dots = document.querySelectorAll(".slider-dots button");
  let currentIndex = 0;

  if (slides == null) return;
  function goToSlide(idx) {
    const slideCount = slides.children.length;
    idx = (idx + slideCount) % slideCount;
    slides.style.transform = `translateX(-${idx * 100}%)`;
    currentIndex = idx;
    updateDots();
  }

  document.querySelectorAll(".accordion-header").forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.parentElement;
      item.classList.toggle("active");
    });
  });

  function updateDots() {
    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === currentIndex);
      dot.setAttribute("aria-selected", i === currentIndex);
      dot.tabIndex = i === currentIndex ? 0 : -1;
    });
  }

  prevBtn.addEventListener("click", () => goToSlide(currentIndex - 1));
  nextBtn.addEventListener("click", () => goToSlide(currentIndex + 1));
  dots.forEach((dot, i) => dot.addEventListener("click", () => goToSlide(i)));

  setInterval(() => goToSlide(currentIndex + 1), 7000);
  goToSlide(0);
})();
