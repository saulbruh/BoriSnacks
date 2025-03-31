document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 1; // Empezamos en 1 porque agregaremos imágenes extra
    const slidesContainer = document.querySelector(".carousel-slide");
    const slides = document.querySelectorAll(".carousel-slide img");
    const totalSlides = slides.length;
    const prevButton = document.querySelector(".carousel-btn.left");
    const nextButton = document.querySelector(".carousel-btn.right");

    // Clonar primera y última imagen para hacer el efecto de bucle
    const firstClone = slides[0].cloneNode(true);
    const lastClone = slides[totalSlides - 1].cloneNode(true);
    
    slidesContainer.appendChild(firstClone);
    slidesContainer.insertBefore(lastClone, slides[0]);

    // Actualizar la referencia a las imágenes
    const updatedSlides = document.querySelectorAll(".carousel-slide img");

    function updateSlide() {
        slidesContainer.style.transition = "transform 0.5s ease-in-out";
        slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    function nextSlide() {
        if (currentIndex >= updatedSlides.length - 1) return;
        currentIndex++;
        updateSlide();
        
        // Si llega al final (imagen clonada), mover instantáneamente al inicio real
        if (currentIndex === updatedSlides.length - 1) {
            setTimeout(() => {
                slidesContainer.style.transition = "none"; // Deshabilitar transición
                currentIndex = 1; // Ir al primer slide original
                slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    }

    function prevSlide() {
        if (currentIndex <= 0) return;
        currentIndex--;
        updateSlide();
        
        // Si llega al principio (imagen clonada), mover instantáneamente al final real
        if (currentIndex === 0) {
            setTimeout(() => {
                slidesContainer.style.transition = "none";
                currentIndex = updatedSlides.length - 2; // Ir al último slide original
                slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    }

    prevButton.addEventListener("click", prevSlide);
    nextButton.addEventListener("click", nextSlide);

    setInterval(nextSlide, 3000);
});