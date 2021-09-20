let options = {
    root: null,
    rootMargin: '0px',
    threshold: 0.9,
  };


// observer1
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

// observer2
let observer2 = new IntersectionObserver(func, options);
let observed2 = document.querySelector('.trigger3');
let element2 = document.querySelector('.content2');
console.log(element2)

function func(entries){
    entries.forEach(entries =>{
        if(entries.isIntersecting){
            if(element2.classList.contains('.appear')){
                //do nothing
            }
            else{
                element2.classList.add('appear')
            }
        }
    })
}

// calling observers
observer.observe(observed);
observer2.observe(observed2);
