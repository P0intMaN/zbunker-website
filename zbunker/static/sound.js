const mic = document.getElementById('mute');
const audio = document.getElementById("player");
const playbtn = document.querySelector('.playbtn');
const pausebtn = document.querySelector('.soundbars')
mic.addEventListener('click',musicHandler);




//event handler
function musicHandler(){
    if(audio.paused){
        playbtn.style.display = 'none';
        pausebtn.style.display = 'flex';     
        audio.play();

    }
    else{
        playbtn.style.display = 'flex';
        pausebtn.style.display = 'none';
        audio.pause();
    }


}