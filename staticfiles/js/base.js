document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.getElementById('hamburger');
    const navWrapper = document.getElementById('nav-wrapper');

    if (hamburger && navWrapper) {
        hamburger.addEventListener('click', () => {
            const isOpen = navWrapper.classList.toggle('active');
            hamburger.classList.toggle('active');
            
            // Set accessibility attributes
            hamburger.setAttribute('aria-expanded', isOpen);
        });

        // Close mobile drawer when clicking a navigation link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navWrapper.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }
});