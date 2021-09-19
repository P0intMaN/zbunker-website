let options = {
    root: null,
    rootMargin: '0px',
    threshold: 0.9,
  };


// observer
let observer = new IntersectionObserver(callbackfun, options);
let observed = document.querySelector('.trigger2')
let element = document.querySelector('.shift2')
console.log(element)
function callbackfun(entries){
    entries.forEach(entries =>{
        if(entries.isIntersecting){
            if(element.classList.contains('.shift-done')){
                //do nothing
            }
            else{
                element.classList.add('shift-done')
            }
        }
    })
}


// calling observers
observer.observe(observed);
