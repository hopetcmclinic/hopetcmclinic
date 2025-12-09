function toggleMenu() {
    var menuBox = document.getElementById('navMenu');    
    if (menuBox.style.left == "0px"){ 
        menuBox.style.left = "-100%";
    } else {
        menuBox.style.left = "0px";
    }
}


function onToggleMenu(e){
    const navLinks = document.querySelector('.nav-links');
    e.name = e.name === 'menu' ? 'close' : 'menu';
    navLinks.classList.toggle('top-[9%]')
}
