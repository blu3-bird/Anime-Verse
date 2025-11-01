// app/static/js/carousel.js

document.addEventListener('DOMContentLoaded', function(){

    const carousel = document.querySelector('.hero-carousel');

    if (!carousel) return;

    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');

    let currentSlide = 0;
    let autoScrollInterval;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('activie'));

        slides[index].classList.add('active');
        indicators[index].classList.add('active');

        currentSlide = index;
    }

    //Next Slide

    function nextSlide() {
        let nextIndex = currentSlide + 1;

        if(nextIndex >= slides.length) {
            nextIndex = 0;
        }

        showSlide(nextIndex);
    }

    // Previous slide

    function prevSlide(){
        let prevSlide = currentSlide - 1;

        if (prevIndex < 0) {
            prevIndex = slides.length - 1;
        }

        showSlide(prevIndex);
    }

    // Auto Scroll 

    function startAutoScroll() {
        autoScrollInterval = setInterval(function(){
            nextSlide();
        }, 8000);
    }

    function stopAutoScroll(){
        clearInterval(autoScrollInterval);
    }

    //Event Listeners

    if (nextBtn) {
        nextBtn.addEventListener('click', function(){
            nextSlide();
            stopAutoScroll();
            startAutoScroll();
        });
    }

    // Previous Btn click
    if (prevBtn) {
        prevBtn.addEventListener('click', function(){
            prevSlide();
            stopAutoScroll();
            startAutoScroll();
        });
    }

    //Indicator clicks

    indicators.forEach(function(indicator, index){
        indicator.addEventListener('click', function(){
            showSlide(index);
            stopAutoScroll();
            startAutoScroll();
        });
    });

    carousel.addEventListener('mouseenter', function(){
        stopAutoScroll();
    });

    carousel.addEventListener('mouseleave', function(){
        startAutoScroll();
    });

    startAutoScroll();
});