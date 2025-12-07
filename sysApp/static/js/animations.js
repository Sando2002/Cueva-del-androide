/* Animaciones dinámicas e interactividad */

// Animación de carga para inputs
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
    const buttons = document.querySelectorAll('.btn-login, .btn-registro');
    
    // Agregar efecto de enfoque a inputs
    inputs.forEach((input, index) => {
        input.addEventListener('focus', function() {
            this.style.animation = `slideIn${index % 2 === 0 ? 'Left' : 'Right'} 0.4s ease-out`;
        });
    });
    
    // Agregar efecto ripple a botones
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Animación de aparición para forms
    const forms = document.querySelectorAll('.login-card, .registro-card');
    forms.forEach(form => {
        form.style.opacity = '0';
        form.style.transform = 'translateY(20px)';
        setTimeout(() => {
            form.style.transition = 'all 0.8s cubic-bezier(0.23, 1, 0.32, 1)';
            form.style.opacity = '1';
            form.style.transform = 'translateY(0)';
        }, 100);
    });
    
    // Efecto parallax en navbar
    const navbar = document.querySelector('.header');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
            } else {
                navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
            }
        });
    }
    
    // Validación en tiempo real para inputs
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#9a2ec5';
            }
        });
        
        input.addEventListener('blur', function() {
            if (this.value.length === 0) {
                this.style.borderColor = '#e2e8f0';
            }
        });
    });
    
    // Animación de hover para iconos del navbar
    const iconButtons = document.querySelectorAll('.icon-button');
    iconButtons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.animation = 'bounce 0.6s ease-out';
        });
    });
});

// Animación de bounce
const style = document.createElement('style');
style.innerHTML = `
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: rippleEffect 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll para navegación
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
