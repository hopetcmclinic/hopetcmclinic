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
    // Default is hidden on mobile, md:flex on desktop
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
// Dropdown Toggle
function toggleDropdown(event) {
    event.stopPropagation(); // Prevent event bubbling
    const dropdown = document.getElementById('treatments-dropdown');
    const arrow = document.querySelector('#dropdown-arrow');

    // Check if open based on maxHeight (mobile) or inline opacity (desktop)
    const isOpen = dropdown.style.maxHeight || dropdown.style.opacity === '1';

    if (isOpen) {
        // Close
        dropdown.style.maxHeight = null;
        arrow.classList.remove('rotate-180');

        // Remove overrides (return to formatting via CSS classes)
        dropdown.style.opacity = '';
        dropdown.style.visibility = '';
    } else {
        // Open
        dropdown.style.maxHeight = dropdown.scrollHeight + "px";
        arrow.classList.add('rotate-180');

        // Add overrides to force show on desktop
        dropdown.style.opacity = '1';
        dropdown.style.visibility = 'visible';
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('treatments-dropdown');
    const arrow = document.querySelector('#dropdown-arrow');

    // If dropdown exists and click is outside of it
    // Note: The toggle button stops propagation, so this listener only sees outside clicks 
    // or clicks inside the dropdown (which bubble up).
    if (dropdown && !dropdown.contains(event.target)) {
        dropdown.style.maxHeight = null;
        if (arrow) arrow.classList.remove('rotate-180');

        // Remove overrides
        dropdown.style.opacity = '';
        dropdown.style.visibility = '';
    }
});
