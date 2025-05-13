// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Remover el preloader cuando la página haya cargado completamente
    window.addEventListener('load', function() {
        const preloader = document.getElementById('preloader');
        if (preloader) {
            setTimeout(function() {
                preloader.style.opacity = '0';
                setTimeout(function() {
                    preloader.style.display = 'none';
                }, 500);
            }, 800);
        }
    });

    // Funcionalidad del menú móvil
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }

    // Observador de intersecciones para animar secciones al desplazarse
    const sections = document.querySelectorAll('.content-section, .seccion-contenido, .features-section, .mission-values-section, .achievements-section, .partners-section');
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.25
    };

    // Función para animar los números en la sección de logros
    function animateNumbers() {
        const achievementNumbers = document.querySelectorAll('.achievement-number');
        
        achievementNumbers.forEach((numberElement, index) => {
            const finalNumber = numberElement.innerText.replace(/[^\d.]/g, '');
            const hasPlusSign = numberElement.innerText.includes('+');
            const hasPercentSign = numberElement.innerText.includes('%');
            
            // Restablecer el texto para la animación
            numberElement.innerText = '0';
            
            // Determinar el incremento basado en el número final
            const duration = 2000; // duración de la animación en milisegundos
            const steps = 60; // número de pasos en la animación
            
            let finalValue = parseFloat(finalNumber);
            let increment = finalValue / steps;
            let currentValue = 0;
            
            // Retrasar el inicio de la animación para cada número
            setTimeout(() => {
                let timer = setInterval(() => {
                    currentValue += increment;
                    
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    
                    // Formatear el número según sea un porcentaje, tenga signo más, etc.
                    let displayValue = '';
                    
                    if (finalValue % 1 !== 0) {
                        // Es un número decimal
                        displayValue = currentValue.toFixed(1);
                    } else {
                        // Es un número entero
                        displayValue = Math.floor(currentValue);
                    }
                    
                    // Añadir signo + o % si es necesario
                    if (hasPlusSign) displayValue += '+';
                    if (hasPercentSign) displayValue += '%';
                    
                    numberElement.innerText = displayValue;
                }, duration / steps);
            }, index * 200); // Retraso escalonado para cada número
        });
    }

    const sectionObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Animación específica para la sección de logros
                if (entry.target.classList.contains('achievements-section')) {
                    entry.target.classList.add('animating');
                    animateNumbers();
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

    // Efecto de parallax suave para el hero
    const heroSection = document.querySelector('.about-hero-section');
    const heroImage = document.querySelector('.about-hero-image');
    
    if (heroSection && heroImage) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            const speed = 0.5; // Velocidad del efecto parallax
            
            // Solo aplicar parallax si la sección está visible
            if (scrollPosition < heroSection.offsetHeight) {
                // Mover la imagen hacia abajo mientras hacemos scroll
                heroImage.style.transform = `translateY(${scrollPosition * speed}px)`;
            }
        });
    }

    // Animación al hacer hover en las tarjetas
    const cards = document.querySelectorAll('.mission-card, .value-card, .achievement-card, .partner-logo');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 35px rgba(90, 24, 154, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 10px 25px rgba(90, 24, 154, 0.1)';
        });
    });

    // Inicializar las columnas del footer como visibles
    const footerColumns = document.querySelectorAll('.footer-column');
    
    footerColumns.forEach((column, index) => {
        setTimeout(() => {
            column.classList.add('visible');
        }, 300 * index);
    });

    // --------- VENTANAS MODALES ---------
    
    // Funciones globales para los modales
    function showTermsModal() {
        const termsModal = document.getElementById('termsModal');
        if (termsModal) {
            termsModal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeTermsModal() {
        const termsModal = document.getElementById('termsModal');
        if (termsModal) {
            termsModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    function showCookiesModal() {
        const cookiesModal = document.getElementById('cookiesModal');
        if (cookiesModal) {
            cookiesModal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeCookiesModal() {
        const cookiesModal = document.getElementById('cookiesModal');
        if (cookiesModal) {
            cookiesModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // Configuración del modal de términos y condiciones
    const termsModal = document.getElementById('termsModal');
    if (termsModal) {
        const closeTermsBtn = termsModal.querySelector('.close-modal');
        const acceptTermsBtn = document.getElementById('acceptTerms');
        
        // Eventos para cerrar el modal
        if (closeTermsBtn) {
            closeTermsBtn.addEventListener('click', closeTermsModal);
        }
        
        if (acceptTermsBtn) {
            acceptTermsBtn.addEventListener('click', closeTermsModal);
        }
        
        // Cerrar al hacer clic fuera del modal
        window.addEventListener('click', function(event) {
            if (event.target === termsModal) {
                closeTermsModal();
            }
        });
        
        // Añadir evento a los enlaces de términos
        document.querySelectorAll('a').forEach(link => {
            if (link.textContent.includes('Términos') || link.textContent.includes('Condiciones')) {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    showTermsModal();
                });
            }
        });
        
        // Cerrar con tecla ESC
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && termsModal.style.display === 'block') {
                closeTermsModal();
            }
        });
    }
    
    // Configuración del modal de cookies
    const cookiesModal = document.getElementById('cookiesModal');
    if (cookiesModal) {
        const closeCookiesBtn = cookiesModal.querySelector('.close-modal');
        const acceptCookiesBtn = document.getElementById('acceptCookies');
        const rejectCookiesBtn = document.getElementById('rejectCookies');
        
        // Eventos para cerrar el modal
        if (closeCookiesBtn) {
            closeCookiesBtn.addEventListener('click', closeCookiesModal);
        }
        
        // Cerrar al hacer clic fuera del modal
        window.addEventListener('click', function(event) {
            if (event.target === cookiesModal) {
                closeCookiesModal();
            }
        });
        
        // Acciones para los botones
        if (acceptCookiesBtn) {
            acceptCookiesBtn.addEventListener('click', function() {
                setCookieConsent('accept_all');
                closeCookiesModal();
                hideCookieBanner();
            });
        }
        
        if (rejectCookiesBtn) {
            rejectCookiesBtn.addEventListener('click', function() {
                setCookieConsent('essential_only');
                closeCookiesModal();
                hideCookieBanner();
            });
        }
        
        // Añadir evento a enlaces de política de cookies
        document.querySelectorAll('a').forEach(link => {
            if (link.textContent.includes('Cookies') || link.textContent.includes('cookies')) {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    showCookiesModal();
                });
            }
        });
    }
    
    // Banner de cookies
    createCookieBanner();
    
    // Verificar preferencia existente
    const cookieConsent = getCookie('cookieConsent');
    if (!cookieConsent) {
        setTimeout(showCookieBanner, 1000);
    }
    
    // Funciones para el banner de cookies
    function createCookieBanner() {
        // Verificar si ya existe para evitar duplicados
        if (document.getElementById('cookieBanner')) return;
        
        const banner = document.createElement('div');
        banner.className = 'cookie-banner';
        banner.id = 'cookieBanner';
        banner.style.display = 'none';
        
        const bannerContent = `
            <div class="cookie-banner-text">
                <p>Utilizamos cookies para mejorar su experiencia en nuestro sitio web. Al continuar navegando, acepta nuestra <a href="#" id="cookiePolicyLink">política de cookies</a>.</p>
            </div>
            <div class="cookie-banner-actions">
                <button id="acceptAllCookies" class="cookie-banner-button cookie-banner-accept">Aceptar todas</button>
                <button id="customizeCookies" class="cookie-banner-button cookie-banner-customize">Personalizar</button>
            </div>
        `;
        
        banner.innerHTML = bannerContent;
        document.body.appendChild(banner);
        
        // Eventos para el banner
        document.getElementById('acceptAllCookies').addEventListener('click', function() {
            setCookieConsent('accept_all');
            hideCookieBanner();
        });
        
        document.getElementById('customizeCookies').addEventListener('click', function() {
            showCookiesModal();
        });
        
        document.getElementById('cookiePolicyLink').addEventListener('click', function(e) {
            e.preventDefault();
            showCookiesModal();
        });
    }
    
    function showCookieBanner() {
        const banner = document.getElementById('cookieBanner');
        if (banner) {
            banner.style.display = 'flex';
        }
    }
    
    function hideCookieBanner() {
        const banner = document.getElementById('cookieBanner');
        if (banner) {
            banner.style.display = 'none';
        }
    }
    
    // Funciones para manejo de cookies
    function setCookieConsent(value) {
        const expiryDate = new Date();
        expiryDate.setMonth(expiryDate.getMonth() + 6);
        
        document.cookie = `cookieConsent=${value};expires=${expiryDate.toUTCString()};path=/;SameSite=Lax`;
        
        if (value === 'accept_all') {
            enableAllCookies();
        } else {
            enableEssentialCookies();
        }
    }
    
    function getCookie(name) {
        const cookieArr = document.cookie.split(';');
        
        for (let i = 0; i < cookieArr.length; i++) {
            const cookiePair = cookieArr[i].split('=');
            const cookieName = cookiePair[0].trim();
            
            if (cookieName === name) {
                return decodeURIComponent(cookiePair[1]);
            }
        }
        
        return null;
    }
    
    function enableAllCookies() {
        console.log('Todas las cookies activadas');
        // Implementación para activar todas las cookies
    }
    
    function enableEssentialCookies() {
        console.log('Solo cookies esenciales activadas');
        // Implementación para activar solo cookies esenciales
    }
});