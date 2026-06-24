document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling adjustments for anchor references taking the sticky header offset into account
    const links = document.querySelectorAll('a[href^="#"]');
    const header = document.querySelector('.header');
    const headerHeight = header ? header.offsetHeight : 70;

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerHeight - 10;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});