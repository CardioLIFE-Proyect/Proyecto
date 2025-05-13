document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    
    if (!preloader) {
        createPreloader();
    }
    
    window.addEventListener('load', function() {
        setTimeout(function() {
            const preloader = document.getElementById('preloader');
            if (preloader) {
                preloader.style.opacity = '0';
                setTimeout(function() {
                    preloader.style.display = 'none';
                }, 500);
            }
            
            startAnimations();
        }, 1000);
    });

    // Aseguramos que esta función se ejecute inmediatamente
    initMobileMenu();
    
    initFormAnimations();
    
    initBenefitsAnimations();
    
    initFooterAnimations();
});

function createPreloader() {
    const preloader = document.createElement('div');
    preloader.id = 'preloader';
    
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    
    preloader.appendChild(spinner);
    document.body.prepend(preloader);
}

function startAnimations() {
    animateHeader();
    animateRegistrationSection();
}

function animateHeader() {
    const headerElements = [
        '.logo',
        '.desktop-nav',
        '.user-actions',
        '.download-btn'
    ];
    
    headerElements.forEach((selector, index) => {
        const element = document.querySelector(selector);
        if (element) {
            setTimeout(() => {
                element.style.opacity = '1';
            }, 200 * index);
        }
    });
}

function animateRegistrationSection() {
    const section = document.querySelector('.registration-section');
    if (section) {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 300);
        
        setTimeout(() => {
            const title = document.querySelector('.registration-title');
            if (title) {
                title.classList.add('animated');
            }
        }, 800);
    }
}

function initMobileMenu() {
    // La función ahora imprime un mensaje en la consola para debugging
    console.log("Inicializando menú móvil");
    
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    // Verificamos si los elementos existen antes de continuar
    if (menuToggle && mobileMenu) {
        console.log("Elementos del menú encontrados, añadiendo event listener");
        
        // Añadimos el listener de manera explícita
        menuToggle.addEventListener('click', function(e) {
            // Prevenimos comportamiento predeterminado por seguridad
            e.preventDefault();
            
            console.log("Menú toggle clickeado");
            
            // Agregamos/quitamos la clase active
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            
            // Log para verificar si la clase se ha añadido correctamente
            console.log("Estado del menú móvil:", mobileMenu.classList.contains('active') ? "activo" : "inactivo");
            
            if (mobileMenu.classList.contains('active')) {
                // Aseguramos que el menú sea visible con un estilo inline adicional
                mobileMenu.style.display = 'block';
                
                const menuItems = mobileMenu.querySelectorAll('li');
                menuItems.forEach((item, index) => {
                    item.style.opacity = '0';
                    item.style.transform = 'translateX(20px)';
                    setTimeout(() => {
                        item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                        item.style.opacity = '1';
                        item.style.transform = 'translateX(0)';
                    }, 100 * index);
                });
            } else {
                // Si se cierra el menú, aseguramos que se oculte correctamente
                setTimeout(() => {
                    // Solo ocultamos si la clase active no está presente
                    if (!mobileMenu.classList.contains('active')) {
                        mobileMenu.style.display = '';
                    }
                }, 300); // Tiempo suficiente para la animación
            }
        });
        
        // También cerramos el menú cuando se hace clic en un enlace del menú móvil
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
            });
        });
        
    } else {
        console.error('Error: Elementos del menú no encontrados.');
        console.log('menuToggle:', menuToggle);
        console.log('mobileMenu:', mobileMenu);
    }
}

function validateForm() {
    const form = document.getElementById('registrationForm');
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        shakeElement(document.getElementById('confirmPassword'));
        return false;
    }
    
    return true;
}

function initFormAnimations() {
    const formGroups = document.querySelectorAll('.form-group');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('form-animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        group.style.transitionDelay = `${index * 0.1}s`;
        
        observer.observe(group);
    });
    
    const form = document.getElementById('registrationForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                const button = form.querySelector('.form-button');
                button.innerHTML = 'Procesando...';
                button.style.width = '100%';
                
                setTimeout(() => {
                    button.innerHTML = '¡Cuenta creada!';
                    button.style.background = 'linear-gradient(to right, #4CAF50, #45a049)';
                    
                    createSuccessMessage();
                    
                    setTimeout(() => {
                        form.reset();
                        button.innerHTML = 'Crear mi cuenta';
                        button.style.background = 'linear-gradient(to right, #f72585, #7b2cbf)';
                    }, 3000);
                }, 1500);
            }
        });
    }
}

function createSuccessMessage() {
    const existingMessage = document.querySelector('.success-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const message = document.createElement('div');
    message.className = 'success-message';
    message.style.position = 'fixed';
    message.style.top = '20px';
    message.style.left = '50%';
    message.style.transform = 'translateX(-50%)';
    message.style.background = 'linear-gradient(to right, #4CAF50, #45a049)';
    message.style.color = 'white';
    message.style.padding = '15px 30px';
    message.style.borderRadius = '30px';
    message.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
    message.style.zIndex = '9999';
    message.style.opacity = '0';
    message.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    message.innerHTML = '¡Cuenta creada con éxito! Revisa tu correo electrónico.';
    
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.style.opacity = '1';
    }, 100);
    
    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateX(-50%) translateY(-20px)';
        setTimeout(() => {
            message.remove();
        }, 500);
    }, 4000);
}

function shakeElement(element) {
    element.style.border = '1px solid #e74c3c';
    element.style.animation = 'shake 0.5s ease-in-out';
    
    if (!document.querySelector('style#shake-animation')) {
        const style = document.createElement('style');
        style.id = 'shake-animation';
        style.innerHTML = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }
    
    setTimeout(() => {
        element.style.animation = '';
        setTimeout(() => {
            element.style.border = '1px solid #ddd';
        }, 300);
    }, 500);
}

function initBenefitsAnimations() {
    const benefits = document.querySelectorAll('.benefit-item');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateBenefit(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    benefits.forEach(benefit => {
        benefit.style.opacity = '0';
        benefit.style.transform = 'translateX(30px)';
        observer.observe(benefit);
    });
}

function animateBenefit(benefit) {
    benefit.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    benefit.style.opacity = '1';
    benefit.style.transform = 'translateX(0)';
}

function initFooterAnimations() {
    const footer = document.querySelector('footer');
    if (footer) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                const columns = footer.querySelectorAll('.footer-column');
                columns.forEach((column, index) => {
                    setTimeout(() => {
                        column.classList.add('visible');
                    }, 200 * index);
                });
                observer.unobserve(footer);
            }
        }, { threshold: 0.2 });
        
        observer.observe(footer);
    }
}

// Aseguramos que estos listeners también se añaden correctamente
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input, .form-select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focus');
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 10px rgba(123, 44, 191, 0.15)';
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focus');
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // También implementamos esto directamente aquí para asegurarnos
    initMobileMenu();
});

document.addEventListener('DOMContentLoaded', function() {
    const socialButtons = document.querySelectorAll('.social-button');
    
    socialButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const img = this.querySelector('img');
            if (img) {
                img.style.transition = 'transform 0.3s ease';
                img.style.transform = 'scale(1.2)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            const img = this.querySelector('img');
            if (img) {
                img.style.transform = 'scale(1)';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});