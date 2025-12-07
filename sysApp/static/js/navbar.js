/* Funcionalidades del navbar */

document.addEventListener('DOMContentLoaded', function() {
    // Control del menú móvil
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    if (closeMobileMenu && mobileMenu) {
        closeMobileMenu.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    }

    // Cerrar menú al hacer clic en un enlace
    if (mobileMenu) {
        const links = mobileMenu.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // Cerrar menú al hacer clic fuera del panel (overlay)
    if (mobileMenu) {
        mobileMenu.addEventListener('click', (e) => {
            // si el clic fue sobre el overlay (no dentro del .container), cerramos
            const container = mobileMenu.querySelector('.container');
            if (container && !container.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    // Cerrar con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenu && !mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
        }
    });

    // Toggle admin menu (desktop)
    const adminToggle = document.getElementById('adminToggle');
    const adminMenu = document.getElementById('adminMenu');
    if (adminToggle && adminMenu) {
        adminToggle.addEventListener('click', (ev) => {
            ev.stopPropagation();
            adminMenu.classList.toggle('hidden');
        });

        // cerrar si hacemos clic fuera
        document.addEventListener('click', (e) => {
            if (!adminMenu.classList.contains('hidden')) {
                const container = adminMenu;
                if (container && !container.contains(e.target) && e.target !== adminToggle) {
                    adminMenu.classList.add('hidden');
                }
            }
        });
    }

    // Manejo del dropdown de notificaciones
    const notifBell = document.getElementById('notifBell');
    const notifDropdown = document.getElementById('notifDropdown');
    const notifContainer = document.querySelector('.notif-container');

    if (notifBell && notifDropdown && notifContainer) {
        // Toggle del dropdown
        notifBell.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isHidden = notifDropdown.style.display === 'none' || notifDropdown.style.display === '';
            notifDropdown.style.display = isHidden ? 'block' : 'none';
        });

        // Evitar que se cierre al hacer click dentro del dropdown
        notifDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // Cerrar al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!notifContainer.contains(e.target)) {
                notifDropdown.style.display = 'none';
            }
        });
    }
});
