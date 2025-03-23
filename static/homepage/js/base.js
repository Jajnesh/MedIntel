document.addEventListener('DOMContentLoaded', function() {
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: {
              DEFAULT: '#1a73e8',
              50: '#f8f8f8',
              100: '#e8e8e8', 
              200: '#d3d3d3',
              300: '#a3a3a3',
              400: '#737373',
              500: '#525252',
              600: '#404040',
              700: '#262626',
              800: '#171717',
              900: '#0a0a0a',
              950: '#030303',
            },
            secondary: {
              DEFAULT: '#f5f7fa',
              50: '#f8f8f8',
              100: '#e8e8e8',
              200: '#d3d3d3', 
              300: '#a3a3a3',
              400: '#737373',
              500: '#525252',
              600: '#404040',
              700: '#262626',
              800: '#171717',
              900: '#0a0a0a',
              950: '#030303',
            },
            accent: {
              DEFAULT: '',
              50: '#f8f8f8',
              100: '#e8e8e8',
              200: '#d3d3d3',
              300: '#a3a3a3', 
              400: '#737373',
              500: '#525252',
              600: '#404040',
              700: '#262626',
              800: '#171717',
              900: '#0a0a0a',
              950: '#030303',
            },
          },
          fontFamily: {
            sans: ['Roboto, sans-serif', 'Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica Neue', 'Arial', 'sans-serif'],
            heading: ['Open Sans, sans-serif', 'Inter', 'system-ui', 'sans-serif'],
            body: ['Open Sans, sans-serif', 'Inter', 'system-ui', 'sans-serif'],
          },
          spacing: {
            '18': '4.5rem',
            '22': '5.5rem',
            '30': '7.5rem',
          },
          maxWidth: {
            '8xl': '88rem',
            '9xl': '96rem',
          },
          animation: {
            'fade-in': 'fadeIn 0.5s ease-in',
            'fade-out': 'fadeOut 0.5s ease-out',
            'slide-up': 'slideUp 0.5s ease-out',
            'slide-down': 'slideDown 0.5s ease-out',
            'slide-left': 'slideLeft 0.5s ease-out',
            'slide-right': 'slideRight 0.5s ease-out',
            'scale-in': 'scaleIn 0.5s ease-out',
            'scale-out': 'scaleOut 0.5s ease-out',
            'spin-slow': 'spin 3s linear infinite',
            'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            'bounce-slow': 'bounce 3s infinite',
            'float': 'float 3s ease-in-out infinite',
          },
          keyframes: {
            fadeIn: {
              '0%': { opacity: '0' },
              '100%': { opacity: '1' },
            },
            fadeOut: {
              '0%': { opacity: '1' },
              '100%': { opacity: '0' },
            },
            slideUp: {
              '0%': { transform: 'translateY(20px)', opacity: '0' },
              '100%': { transform: 'translateY(0)', opacity: '1' },
            },
            slideDown: {
              '0%': { transform: 'translateY(-20px)', opacity: '0' },
              '100%': { transform: 'translateY(0)', opacity: '1' },
            },
            slideLeft: {
              '0%': { transform: 'translateX(20px)', opacity: '0' },
              '100%': { transform: 'translateX(0)', opacity: '1' },
            },
            slideRight: {
              '0%': { transform: 'translateX(-20px)', opacity: '0' },
              '100%': { transform: 'translateX(0)', opacity: '1' },
            },
            scaleIn: {
              '0%': { transform: 'scale(0.9)', opacity: '0' },
              '100%': { transform: 'scale(1)', opacity: '1' },
            },
            scaleOut: {
              '0%': { transform: 'scale(1.1)', opacity: '0' },
              '100%': { transform: 'scale(1)', opacity: '1' },
            },
            float: {
              '0%, 100%': { transform: 'translateY(0)' },
              '50%': { transform: 'translateY(-10px)' },
            },
          },
          aspectRatio: {
            'portrait': '3/4',
            'landscape': '4/3',
            'ultrawide': '21/9',
          },
        },
      },
      variants: {
        extend: {
          opacity: ['disabled'],
          cursor: ['disabled'],
          backgroundColor: ['active', 'disabled'],
          textColor: ['active', 'disabled'],
        },
      },
    }
});


document.addEventListener('DOMContentLoaded', function() {
const contactForm = document.getElementById('contact-form');
    
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
        
        // Here you would typically send the form data to your backend
        // For demonstration, we'll just show a success message
        
        // Get form data
    const formData = new FormData(contactForm);
    const formDataObj = {};
    formData.forEach((value, key) => {
    formDataObj[key] = value;
  });
        
        // Simulate form submission
        // In a real implementation, you would send this data to your server
    console.log('Form submitted with data:', formDataObj);
        
        // Reset form
    contactForm.reset();
        
        // Show success message (in a real implementation)
    alert('Thank you for your message! We will get back to you soon.');
  });
  }
});

  // Back to Top Button Functionality
  document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('back-to-top');
    
    // Show button when scrolling down
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        backToTopButton.classList.remove('opacity-0', 'invisible');
        backToTopButton.classList.add('opacity-100', 'visible');
      } else {
        backToTopButton.classList.remove('opacity-100', 'visible');
        backToTopButton.classList.add('opacity-0', 'invisible');
      }
    });
    
    // Smooth scroll to top
    backToTopButton.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  });


  // FAQ Toggle Functionality
  document.addEventListener('DOMContentLoaded', function () {
    const faqToggles = document.querySelectorAll('.faq-toggle');

    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const content = toggle.nextElementSibling;
            const icon = toggle.querySelector('svg');
            const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

            // Toggle the aria-expanded state
            toggle.setAttribute('aria-expanded', !isExpanded);

            if (isExpanded) {
                // Collapse the content
                content.style.maxHeight = '0';
                icon.classList.remove('rotate-180');
                setTimeout(() => content.classList.add('hidden'), 300); // Delay to allow transition
            } else {
                // Expand the content
                content.classList.remove('hidden'); // Make it visible before animation
                content.style.maxHeight = content.scrollHeight + 'px';
                icon.classList.add('rotate-180');
            }
        });
    });
});


      // Testimonials Slider Functionality
      document.addEventListener('DOMContentLoaded', function() {
        const track = document.getElementById('testimonials-track');
        const slides = track.children;
        const nextButton = document.getElementById('next-testimonial');
        const prevButton = document.getElementById('prev-testimonial');
        const dots = document.querySelectorAll('.flex.justify-center.mt-8 button');
        
        let currentIndex = 0;
        const slideWidth = 100; // percentage
        
        // Set initial position
        updateSlidePosition();
        
        // Update dots indicator
        function updateDots() {
          dots.forEach((dot, index) => {
            if (index === currentIndex) {
              dot.classList.remove('bg-gray-300', 'dark:bg-gray-600');
              dot.classList.add('bg-blue-600');
              dot.setAttribute('aria-current', 'true');
            } else {
              dot.classList.remove('bg-blue-600');
              dot.classList.add('bg-gray-300', 'dark:bg-gray-600');
              dot.removeAttribute('aria-current');
            }
          });
        }
        
        // Update slide position
        function updateSlidePosition() {
          // For mobile view (1 slide visible)
          if (window.innerWidth < 768) {
            track.style.transform = `translateX(-${currentIndex * 100}%)`;
          } 
          // For tablet view (2 slides visible)
          else if (window.innerWidth < 1024) {
            if (currentIndex > slides.length - 2) {
              currentIndex = slides.length - 2;
            }
            track.style.transform = `translateX(-${currentIndex * 50}%)`;
          } 
          // For desktop view (3 slides visible)
          else {
            if (currentIndex > slides.length - 3) {
              currentIndex = slides.length - 3;
            }
            track.style.transform = `translateX(-${currentIndex * 33.33}%)`;
          }
          
          updateDots();
        }
        
        // Next button click
        nextButton.addEventListener('click', () => {
          if (window.innerWidth < 768) {
            // Mobile: 1 slide visible
            currentIndex = Math.min(currentIndex + 1, slides.length - 1);
          } else if (window.innerWidth < 1024) {
            // Tablet: 2 slides visible
            currentIndex = Math.min(currentIndex + 1, slides.length - 2);
          } else {
            // Desktop: 3 slides visible
            currentIndex = Math.min(currentIndex + 1, slides.length - 3);
          }
          updateSlidePosition();
        });
        
        // Previous button click
        prevButton.addEventListener('click', () => {
          currentIndex = Math.max(currentIndex - 1, 0);
          updateSlidePosition();
        });
        
        // Dot navigation
        dots.forEach((dot, index) => {
          dot.addEventListener('click', () => {
            currentIndex = index;
            updateSlidePosition();
          });
        });
        
        // Handle window resize
        window.addEventListener('resize', updateSlidePosition);
      });


  // Mobile menu toggle
  document.getElementById('mobile-menu-button').addEventListener('click', function() {
    const menu = document.getElementById('mobile-menu');
    const menuButton = document.getElementById('mobile-menu-button');
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    
    menu.classList.toggle('hidden');
    menuButton.setAttribute('aria-expanded', !expanded);
    
    if (!expanded) {
      menuButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>';
    } else {
      menuButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>';
    }
  });     