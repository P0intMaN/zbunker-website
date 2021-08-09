var options = {
    loop: true,
    slidesPerView: 1.5,
    watchSlidesProgress: true,
    mousewheel: true,
    allowSlidePrev: true,
    centeredSlides: true,

    on:{
        init: function(){
            var swiper = this;
            const backImg = document.querySelector('.container-fluid > .gallery-items > i')
            const aSlide = swiper.slides[swiper.activeIndex]
            actSlide = aSlide.querySelector('.swiper-slide > .heading')
            const dataImg = actSlide.getAttribute('data-text')
            backImg.innerHTML = dataImg
        }
    }
};


var swiper = new Swiper('.swiper-text-container', options)


swiper.on('slideChange', function(){

        const backImg = document.querySelector('.container-fluid > .gallery-items > i')
        const aSlide = swiper.slides[swiper.activeIndex]
        actSlide = aSlide.querySelector('.swiper-slide > .heading')
        const dataImg = actSlide.getAttribute('data-text')
        backImg.innerHTML = dataImg

})


