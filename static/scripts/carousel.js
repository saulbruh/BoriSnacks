document.addEventListener("DOMContentLoaded", function () {
  let currentIndex = 0;
  const slides = document.querySelectorAll(".carousel-slide img");
  const totalSlides = slides.length;
  const prevButton = document.querySelector(".carousel-btn.left");
  const nextButton = document.querySelector(".carousel-btn.right");

  function updateSlide() {
      document.querySelector(".carousel-slide").style.transform = `translateX(-${currentIndex * 100}%)`;
  }

  function nextSlide() {
      currentIndex = (currentIndex + 1) % totalSlides;
      updateSlide();
  }

  function prevSlide() {
      currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      updateSlide();
  }

  prevButton.addEventListener("click", prevSlide);
  nextButton.addEventListener("click", nextSlide);

  setInterval(nextSlide, 3000);
});