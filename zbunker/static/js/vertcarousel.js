var options = {
    loop: true,
    direction: 'vertical',
    watchSlidesProgress: true,
    mousewheel: true,
    allowSlidePrev: true,
    centeredSlides: true,
    slidesPerView: 1.25,
    autoplay:true,
    navigation:{
        nextEl: '.prev',
        prevEl: '.next',
    },

    on:{
        init:function(){
            var scndswiper = this;
            const rightText = document.querySelector('.gallery-right > .gallery-text-container > .heading')
            const rightPara = document.querySelector('.gallery-right > .gallery-text-container > p')
            const slideno = document.querySelector('.gallery-container > .counter > .slideno')
            const hrefButton = document.querySelector('.firstbutton')

            const aSlide = scndswiper.slides[scndswiper.activeIndex]
            const image = aSlide.querySelector('.swiper-slide > img')
            const text = image.getAttribute('data-title')
            const para = image.getAttribute('data-para')
            const id = image.getAttribute('data-id')
            const url = image.getAttribute('data-url')

            rightText.innerHTML = text
            image.style.borderColor = 'white';
            rightPara.innerHTML = para
            slideno.innerHTML = id;
            hrefButton.setAttribute('href',url)


        }
    }
    
};



var scndswiper = new Swiper('.gallery-main', options)


scndswiper.on('slideChange', function(){

    var scndswiper = this;
    const rightText = document.querySelector('.gallery-right > .gallery-text-container > .heading')
    const rightPara = document.querySelector('.gallery-right > .gallery-text-container > p')
    const slideno = document.querySelector('.gallery-container > .counter > .slideno')

    const aSlide = scndswiper.slides[scndswiper.activeIndex]
    const image = aSlide.querySelector('.swiper-slide > img')
    image.style.borderColor = 'white';
    const id = image.getAttribute('data-id')

    const text = image.getAttribute('data-title')
    const para = image.getAttribute('data-para')
    rightText.innerHTML = text
    rightPara.innerHTML = para
    slideno.innerHTML = id;

})

scndswiper.on('activeIndexChange', function(){

    var scndswiper = this;

    // fetch values here:
    const rightText = document.querySelector('.gallery-right > .gallery-text-container > .heading')
    const hrefButton = document.querySelector('.firstbutton')
    
    // slide variables
    const aSlide = scndswiper.slides[scndswiper.previousIndex]
    const image = aSlide.querySelector('.swiper-slide > img')
    const text = image.getAttribute('data-title')
    const url = image.getAttribute('data-url')

    // set values here:
    rightText.innerHTML = text
    image.style.borderColor = '#434343';
    hrefButton.setAttribute('href',url)
})

