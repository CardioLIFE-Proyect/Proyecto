// Menú móvil
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });

        // Cerrar menú al hacer clic fuera de él
        document.addEventListener('click', function(event) {
            if (!menuToggle.contains(event.target) && !mobileMenu.contains(event.target)) {
                menuToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
            }
        });
    }
});

// Función para detectar cuando un elemento es visible en el viewport
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
        rect.bottom >= 0
    );
}

// Función para añadir la clase 'visible' cuando el elemento aparece en pantalla
function handleScroll() {
    const sections = [
        ...document.querySelectorAll('.content-section'),
        ...document.querySelectorAll('.seccion-contenido'),
        ...document.querySelectorAll('.testimonial-section'),
        ...document.querySelectorAll('.footer-column')
    ];
    
    sections.forEach(section => {
        if (isElementInViewport(section) && !section.classList.contains('visible')) {
            section.classList.add('visible');
            
            // Efecto especial para las imágenes
            const image = section.querySelector('.section-image') || section.querySelector('.imagen-seccion');
            if(image) {
                setTimeout(() => {
                    image.style.transition = 'transform 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)';
                    image.style.transform = 'scale(1)';
                }, 300);
            }
            
            // Efecto para los párrafos
            const paragraphs = section.querySelectorAll('p');
            paragraphs.forEach((paragraph, index) => {
                paragraph.style.opacity = '0';
                paragraph.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    paragraph.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                    paragraph.style.opacity = '1';
                    paragraph.style.transform = 'translateY(0)';
                }, 300 + (index * 200));
            });
            
            // Efecto para los títulos
            const title = section.querySelector('.section-title') || section.querySelector('.titulo-seccion');
            if (title) {
                setTimeout(() => {
                    if (title.querySelector('::after')) {
                        title.style.setProperty('--title-after-width', '100%');
                    }
                }, 300);
            }
        }
    });

    const featuresSection = document.querySelector('.features-section');
    if (featuresSection && isElementInViewport(featuresSection) && !featuresSection.classList.contains('visible')) {
        featuresSection.classList.add('visible');
        
        // Animar el título
        const featuresTitle = featuresSection.querySelector('.features-title');
        if (featuresTitle) {
            setTimeout(() => {
                featuresTitle.style.setProperty('--title-after-width', '80%');
            }, 300);
        }
        
        // Animar las tarjetas
        const cards = featuresSection.querySelectorAll('.feature-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 300 + (index * 200));
        });
    }

    // Detectar y animar la sección CTA
    const ctaSection = document.querySelector('.cta-section');
    if (ctaSection && isElementInViewport(ctaSection) && !ctaSection.classList.contains('visible')) {
        ctaSection.classList.add('visible');
        ctaSection.style.opacity = '0';
        ctaSection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            ctaSection.style.transition = 'opacity 1s ease, transform 1s ease';
            ctaSection.style.opacity = '1';
            ctaSection.style.transform = 'translateY(0)';
        }, 300);
        
        // Animar la imagen
        const ctaImage = ctaSection.querySelector('.cta-image img');
        if (ctaImage) {
            ctaImage.style.opacity = '0';
            ctaImage.style.transform = 'rotate(3deg) scale(0.9)';
            
            setTimeout(() => {
                ctaImage.style.transition = 'opacity 1s ease, transform 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)';
                ctaImage.style.opacity = '1';
                ctaImage.style.transform = 'rotate(3deg) scale(1)';
            }, 500);
        }
    }
}

// Configurar los eventos de scroll
window.addEventListener('scroll', handleScroll);
window.addEventListener('resize', handleScroll);
window.addEventListener('load', () => {
    // Iniciar las animaciones después de que la página haya cargado
    setTimeout(handleScroll, 100);
});

// Animación de preloader
document.addEventListener('DOMContentLoaded', function() {
    // Comprobar si las imágenes están cargadas
    let imagesLoaded = 0;
    const images = document.querySelectorAll('img');
    const totalImages = images.length;
    
    // Si no hay imágenes, ocultar preloader
    if (totalImages === 0) {
        hidePreloader();
        return;
    }
    
    // Función para ocultar el preloader
    function hidePreloader() {
        const preloader = document.getElementById('preloader');
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
                // Iniciar animaciones de la página
                handleScroll();
            }, 500);
        }
    }
    
    // Verificar carga de imágenes
    images.forEach(img => {
        if (img.complete) {
            imageLoaded();
        } else {
            img.addEventListener('load', imageLoaded);
            img.addEventListener('error', imageLoaded);
        }
    });
    
    function imageLoaded() {
        imagesLoaded++;
        if (imagesLoaded >= totalImages || imagesLoaded >= 5) { // Mostrar después de 5 imágenes o todas
            setTimeout(hidePreloader, 1000); // Añadimos un segundo más para asegurar una buena experiencia
        }
    }
    
    // Por si acaso, establecer un tiempo máximo para el preloader
    setTimeout(hidePreloader, 3000);
});

// Mejorar la adaptación de imágenes
window.addEventListener('load', function() {
    const images = document.querySelectorAll('.section-image, .imagen-seccion');
    images.forEach(img => {
        const container = img.parentElement;
        const containerWidth = container.offsetWidth;
        img.style.maxWidth = containerWidth + 'px';
    });
});

window.addEventListener('resize', function() {
    const images = document.querySelectorAll('.section-image, .imagen-seccion');
    
    images.forEach(img => {
        const container = img.parentElement;
        const containerWidth = container.offsetWidth;
        img.style.maxWidth = containerWidth + 'px';
    });
});

