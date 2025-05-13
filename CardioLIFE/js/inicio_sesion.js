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
    animateLoginSection();
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

function animateLoginSection() {
    const section = document.querySelector('.login-section');
    if (section) {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 300);
        
        setTimeout(() => {
            const title = document.querySelector('.login-title');
            if (title) {
                title.classList.add('animated');
            }
        }, 800);
    }
}

function initMobileMenu() {
    console.log("Inicializando menú móvil");
    
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (menuToggle && mobileMenu) {
        console.log("Elementos del menú encontrados, añadiendo event listener");
        
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            console.log("Menú toggle clickeado");
            
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            
            console.log("Estado del menú móvil:", mobileMenu.classList.contains('active') ? "activo" : "inactivo");
            
            if (mobileMenu.classList.contains('active')) {
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
                setTimeout(() => {
                    if (!mobileMenu.classList.contains('active')) {
                        mobileMenu.style.display = '';
                    }
                }, 300);
            }
        });
        
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

function initFormAnimations() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        group.style.transitionDelay = `${index * 0.1}s`;
        
        setTimeout(() => {
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 500 + (index * 100));
    });
    
    const loginOptions = document.querySelector('.login-options');
    if (loginOptions) {
        loginOptions.style.opacity = '0';
        setTimeout(() => {
            loginOptions.style.transition = 'opacity 0.5s ease';
            loginOptions.style.opacity = '1';
        }, 800);
    }
    
    const button = document.querySelector('.form-button');
    if (button) {
        button.style.opacity = '0';
        setTimeout(() => {
            button.style.transition = 'opacity 0.5s ease';
            button.style.opacity = '1';
        }, 900);
    }
    
    const socialLogin = document.querySelector('.social-login');
    if (socialLogin) {
        socialLogin.style.opacity = '0';
        setTimeout(() => {
            socialLogin.style.transition = 'opacity 0.5s ease';
            socialLogin.style.opacity = '1';
        }, 1000);
    }
    
    const registerLink = document.querySelector('.register-link');
    if (registerLink) {
        registerLink.style.opacity = '0';
        setTimeout(() => {
            registerLink.style.transition = 'opacity 0.5s ease';
            registerLink.style.opacity = '1';
        }, 1100);
    }
    
    animateInfoColumn();
    
    const form = document.getElementById('loginForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const button = form.querySelector('.form-button');
            button.innerHTML = 'Procesando...';
            
            setTimeout(() => {
                button.innerHTML = '¡Iniciando sesión!';
                button.style.background = 'linear-gradient(to right, #4CAF50, #45a049)';
                
                createSuccessMessage();
                
                setTimeout(() => {
                    // Aquí podrías redirigir al usuario a su dashboard
                    // window.location.href = 'dashboard.html';
                    
                    // Por ahora, solo restablecemos el botón
                    button.innerHTML = 'Iniciar Sesión';
                    button.style.background = 'linear-gradient(to right, #f72585, #7b2cbf)';
                }, 1500);
            }, 1500);
        });
    }
}

function animateInfoColumn() {
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.style.opacity = '0';
        loginCard.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            loginCard.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            loginCard.style.opacity = '1';
            loginCard.style.transform = 'translateY(0)';
        }, 700);
    }
    
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(30px)';
        
        setTimeout(() => {
            item.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 900 + (index * 200));
    });
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
    message.innerHTML = '¡Sesión iniciada con éxito! Redirigiendo...';
    
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
    }, 3000);
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

// Listeners para los inputs
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input');
    
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
    
    // Efecto hover para los botones sociales
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