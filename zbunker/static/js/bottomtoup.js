//Get the button:
elle = document.getElementById("bottomtoup").addEventListener('click',tophandler);

mybutton = document.getElementById("bottomtoup")

// initially, the button stays hidden
var visible = false

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {
  scrollFunction()
};

function scrollFunction() {
    var threshold = 400;
    var below_threshold = document.body.scrollTop > threshold || document.documentElement.scrollTop > threshold;
  
  if (below_threshold) {
    if (!visible) { // if the button is not visible,
      unfade(mybutton); // function to gradually fadein button
    }
    
    return;
  }

  if (visible) { // if the button is visible,
    fade(mybutton); // function to gradually fadeout button
  }
}

var current_opacity = 0.1;
var is_unfading = false;
var is_fading = false;

function unfade(element) {
    if(!visible){
    element.style.display = 'flex';
    visible = true;
  }
  
  is_fading = false;
  is_unfading = true;
  
  unfade_step(element);
}

function unfade_step(element){
    element.style.opacity = current_opacity;
    element.style.filter = 'alpha(opacity=' + current_opacity * 100 + ")";
    
    if (current_opacity >= 1){
        // end
      is_unfading = false;
      current_opacity = 1;
        return;
    }
    
    current_opacity += 0.01;
    if(is_unfading){
      setTimeout(function(){
        unfade_step(element);
      }, 10);
    }
}

function fade(element) {
    if(!visible){
    return;
  }
  
  is_fading = true;
  is_unfading = false;
  
  fade_step(element);
}


function fade_step(element) {
    element.style.opacity = current_opacity;
    element.style.filter = 'alpha(opacity=' + current_opacity * 100 + ")";
    
    if (current_opacity <= 0.001){
        // end
      is_fading = false;
      visible = false;
      current_opacity = 0.1;
        element.style.display = 'none';
        return;
    }
    
    current_opacity -= 0.01;
    if(is_fading){
      setTimeout(function(){
        fade_step(element);
      }, 10);
    }
}
function tophandler(){
    window.scrollTo(0,0);
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


let options = {
  root: null,
  rootMargin: '0px',
  threshold: 0.6
};


let observer = new IntersectionObserver(callbackFunc, options);
let observed = document.getElementById('observed')
observer.observe(observed);
element = document.querySelector('.solla')

function callbackFunc(entries){
  entries.forEach(entries =>{
    if(entries.isIntersecting){
      if(element.classList.contains('.icon-3d')){
        // do nothing
      }
      else{
        element.classList.add('icon-3d')
        
      }
    }
  });

}

// InteresectionObserver from StackOverflow

let newoptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0
};

let anotherobserver = new IntersectionObserver(callbackfun, newoptions);
let anotherobserved = document.querySelector('.another-section');
elementtrans = document.querySelector('.avax')
anotherobserver.observe(anotherobserved);

function callbackfun(entries) {
  entries.forEach(entries =>{
    if(entries.isIntersecting){
      if(elementtrans.classList.contains('.finalin')){
        // do nothing
      }
      else{
        elementtrans.classList.add('finalin')
        
      }
    }
  })
}




