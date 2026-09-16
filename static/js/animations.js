document.addEventListener('DOMContentLoaded', () => {
    // 1. Scroll Reveal (IntersectionObserver)
    const revealElements = document.querySelectorAll('.reveal-up');
    
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // 2. Sticky Header Shrink
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 3. Page/Route Transitions
    const links = document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            // Only intercept standard left clicks without modifiers
            if (e.button === 0 && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
                const href = link.getAttribute('href');
                
                // Skip if it's pointing to an anchor on the same page or javascript:void(0)
                if (href.startsWith('javascript:')) return;
                
                // Apply fade out
                document.body.classList.add('fade-out');
                
                // Fallback to remove the class if navigation is slow or cancelled
                setTimeout(() => {
                    document.body.classList.remove('fade-out');
                }, 1000);
            }
        });
    });
    
    // Ensure fade-out is removed when page is shown (e.g., via back button bfcache)
    window.addEventListener('pageshow', (e) => {
        if (e.persisted) {
            document.body.classList.remove('fade-out');
        }
    });
});
