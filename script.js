function toggleMenu() {
    var menuBox = document.getElementById('navMenu');    
    if (menuBox.style.left == "0px"){ 
        menuBox.style.left = "-100%";
    } else {
        menuBox.style.left = "0px";
    }
}
