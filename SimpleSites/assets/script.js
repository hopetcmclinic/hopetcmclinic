function toggleMenu() {
    var menuBox = document.getElementById('navMenu');
    if (menuBox.style.left == "0px") {
        menuBox.style.left = "-100%";
    } else {
        menuBox.style.left = "0px";
    }
}


function onToggleMenu(e) {
    const navLinks = document.querySelector('.nav-links');
    // Toggle hidden/flex for mobile menu logic
    // Default is hidden on mobile, lg:flex on desktop
    navLinks.classList.toggle('hidden');
    navLinks.classList.toggle('flex');
}

function closeMenu() {
    const navLinks = document.querySelector('.nav-links');
    // Ensure menu is closed (hidden)
    if (navLinks.classList.contains('flex')) {
        navLinks.classList.remove('flex');
        navLinks.classList.add('hidden');
    }
}
