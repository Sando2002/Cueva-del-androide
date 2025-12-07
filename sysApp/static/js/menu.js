/* Menú móvil - Toggle y funcionalidades */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle (reusable)
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => mobileMenu.classList.remove('hidden'));
    }
    
    if (closeMobileMenu && mobileMenu) {
        closeMobileMenu.addEventListener('click', () => mobileMenu.classList.add('hidden'));
    }
    
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link, .account-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (mobileMenu) {
                mobileMenu.classList.add('hidden');
            }
        });
    });
});
