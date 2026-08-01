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

// Header Shrink on Scroll
function handleScroll() {
    const header = document.getElementById('site-header');
    const nav = document.getElementById('site-nav');
    const logo = document.getElementById('site-logo');
    const title1 = document.getElementById('site-title-1');
    const title2 = document.getElementById('site-title-2');
    const title3 = document.getElementById('site-title-3');

    if (!header || !nav || !logo) return;

    // Current state check (based on nav padding class)
    const isExpanded = nav.classList.contains('py-4');

    // Hysteresis thresholds
    const shrinkThreshold = 60; // Scroll down past this to shrink
    const expandThreshold = 20; // Scroll up past this to expand

    if (isExpanded && window.scrollY > shrinkThreshold) {
        // Scrolled down - Aggressive Shrink
        nav.classList.remove('py-4');
        nav.classList.add('py-1');

        logo.classList.remove('lg:w-24');
        logo.classList.add('lg:w-12');

        if (title1) {
            title1.classList.remove('lg:text-base');
            title1.classList.add('lg:text-xs');
        }
        if (title2) {
            title2.classList.remove('lg:text-xs');
            title2.classList.add('lg:text-[8px]');
        }
        if (title3) {
            title3.classList.remove('lg:text-base');
            title3.classList.add('lg:text-xs');
        }

        header.classList.add('shadow-md');
        header.classList.remove('shadow-sm');
    } else if (!isExpanded && window.scrollY < expandThreshold) {
        // Top - Original Size
        nav.classList.add('py-4');
        nav.classList.remove('py-1');

        logo.classList.add('lg:w-24');
        logo.classList.remove('lg:w-12');

        if (title1) {
            title1.classList.add('lg:text-base');
            title1.classList.remove('lg:text-xs');
        }
        if (title2) {
            title2.classList.add('lg:text-xs');
            title2.classList.remove('lg:text-[8px]');
        }
        if (title3) {
            title3.classList.add('lg:text-base');
            title3.classList.remove('lg:text-xs');
        }

        header.classList.remove('shadow-md');
        header.classList.add('shadow-sm');
    }
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('load', handleScroll);
