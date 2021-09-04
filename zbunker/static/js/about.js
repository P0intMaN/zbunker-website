// learning source StackOverflow

let aboutoptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0
  };
  
   
  let aboutobserver = new IntersectionObserver(callbackfun, aboutoptions);
  let aboutobserved = document.querySelector('.catch-me');
  elementtrans = document.querySelector('.below-about')
  aboutobserver.observe(aboutobserved);
  
  function callbackfun(entries) {
    entries.forEach(entries =>{
      if(entries.isIntersecting){
        if(elementtrans.classList.contains('.reveal-text')){
          // do nothing
        }
        else{
          elementtrans.classList.add('reveal-text')
          
        }
      }
    })
  }


  let anotheraboutobserver = new IntersectionObserver(callbackfun, aboutoptions);
  let anotheraboutobserved = document.querySelector('.catch-me');
  elementtrans = document.querySelectorAll('.below-abouty')
  anotheraboutobserver.observe(anotheraboutobserved);
  
  function callbackfun(entries) {
    entries.forEach(entries =>{
      if(entries.isIntersecting){
        var punk = false;
        for(let i=0;i<3;i++){
          if(elementtrans[i].classList.contains('.reveal-text')){
            punk = true;
            break;
          }
        }
        if(punk){
          //do nothing
        }
        
        else{
          for(let i=0;i<3;i++){
            elementtrans[i].classList.add('reveal-text')
          }
          
        }
      }
    })
  }