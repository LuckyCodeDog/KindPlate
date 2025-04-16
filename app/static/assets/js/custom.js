// =================== preloader js  ================== //
document.addEventListener('DOMContentLoaded', function () {
    var preloader = document.querySelector('.preloader');
    preloader.style.transition = 'opacity 0.5s ease';
    // Hide the preloader 1 second (1000 milliseconds) after DOM content is loaded
    setTimeout(function () {
        preloader.style.opacity = '0';
        setTimeout(function () {
            preloader.style.display = 'none';
        }, 500); // .5 seconds for the fade-out transition
    }, 1000); // 1 second delay before starting the fade-out effect
});
// =================== preloader js end ================== //





//Animation on Scroll initializing
AOS.init();




// =================== custom trk slider js here =================== //


// component slider here
const Feature = new Swiper('.featured-categories__slider', {
    spaceBetween: 5,
    grabCursor: true,
    loop: true,
    slidesPerView: 2,
    breakpoints: {
        576: {
            slidesPerView: 3,
        },
        768: {
            slidesPerView: 4,
        },
        992: {
            slidesPerView: 5,
            spaceBetween: 15,
        },
        1200: {
            slidesPerView: 7,
            spaceBetween: 25,
        },
    },

    speed: 800,
    navigation: {
        nextEl: ".featured-categories__slider-next",
        prevEl: ".featured-categories__slider-prev",
    },



});





// product  slider here
const product = new Swiper('.product__slider', {
    spaceBetween: 16,
    grabCursor: true,
    loop: true,
    slidesPerView: 1,
    breakpoints: {
        576: {
            slidesPerView: 2,
            spaceBetween: 24,
        },
        768: {
            slidesPerView: 3,
        },
        992: {
            slidesPerView: 3,
            spaceBetween: 24,
        },
        1200: {
            slidesPerView: 3,
        }
    },

    speed: 500,
    navigation: {
        nextEl: ".product__slider-next",
        prevEl: ".product__slider-prev",
    },
});

// product feature  slider here
const productFeature = new Swiper('.product-feature__slider', {
    spaceBetween: 16,
    grabCursor: true,
    loop: true,
    slidesPerView: 2,
    breakpoints: {
        768: {
            slidesPerView: 3,
            spaceBetween: 24,
        },
        992: {
            slidesPerView: 4,
        },
        1200: {
            slidesPerView: 5,
        }
    },

    speed: 500,
    navigation: {
        nextEl: ".product__slider-next",
        prevEl: ".product__slider-prev",
    },
});


// blog  slider here
const blog = new Swiper('.blog__slider', {
    spaceBetween: 24,
    grabCursor: true,
    loop: true,
    slidesPerView: 1,
    breakpoints: {
        576: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 3,
        }
    },

    autoplay: true,
    speed: 500,
    navigation: {
        nextEl: ".blog__slider-next",
        prevEl: ".blog__slider-prev",
    },
});

// testimonial slider

const testimonial = new Swiper('.testimonial__slider', {
    spaceBetween: 24,
    grabCursor: true,
    loop: true,
    slidesPerView: 1,
    breakpoints: {
        576: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 2,
        },
        1200: {
            slidesPerView: 2,
            spaceBetween: 25,
        },
    },

    autoplay: true,
    speed: 500,

    navigation: {
        nextEl: ".testimonial__slider-next",
        prevEl: ".testimonial__slider-prev",
    },
});



var galleryThumbs = new Swiper('.pro-single-thumbs', {
    spaceBetween: 10,
    slidesPerView: 3,
    loop: true,
    freeMode: true,
    loopedSlides: 5,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    navigation: {
        nextEl: '.pro-single-next',
        prevEl: '.pro-single-prev',
    },
});
var galleryTop = new Swiper('.pro-single-top', {
    spaceBetween: 10,
    loop: true,
    loopedSlides: 5,
    thumbs: {
        swiper: galleryThumbs,
    },
});
// =================== custom trk slider end here =================== //





// =================== scroll js start here =================== //

// Show/hide button on scroll
window.addEventListener('scroll', function () {
    var scrollToTop = document.querySelector('.scrollToTop');

    if (scrollToTop) {
        if (window.pageYOffset > 300) {
            scrollToTop.style.bottom = '5%';
            scrollToTop.style.opacity = '1';
            scrollToTop.style.visibility = 'visible';
        } else {
            scrollToTop.style.bottom = '-50px';
            scrollToTop.style.opacity = '0';
            scrollToTop.style.visibility = 'hidden';
        }
    }
});

// Click event to scroll to top
var scrollToTop = document.querySelector('.scrollToTop');

if (scrollToTop) {
    scrollToTop.addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// =================== scroll js end here =================== //




// =================== count start here =================== //
new PureCounter();
// =================== count end here =================== //





// =================== Custom accordion start here =================== //
document.addEventListener('DOMContentLoaded', () => {
    const sidebarFilters = document.querySelectorAll('.sidebar-filter--collapsible');

    sidebarFilters.forEach(filter => {
        const header = filter.querySelector('.sidebar-filter__header');
        const toggleBtn = filter.querySelector('.sidebar-filter__toggle');

        header.addEventListener('click', () => {
            const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            toggleBtn.setAttribute('aria-expanded', !isExpanded);
            filter.classList.toggle('is-collapsed');
        });
    });
});
// =================== Custom accordion end here =================== //





// =================== counter start here =================== //
document.addEventListener('DOMContentLoaded', function () {
    const countdownElement = document.querySelector(".countdown");
    const daysElement = document.getElementById("days");
    const hoursElement = document.getElementById("hours");
    const minutesElement = document.getElementById("minutes");
    const secondsElement = document.getElementById("seconds");

    // Only proceed if the countdown elements exist
    if (countdownElement && daysElement && hoursElement && minutesElement && secondsElement) {
        const countDownDate = new Date().getTime() + (2 * 24 * 60 * 60 * 1000) + (12 * 60 * 60 * 1000) + (45 * 60 * 1000) + (5 * 1000);

        function updateCountdown() {
            const now = new Date().getTime();
            const distance = countDownDate - now;

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            daysElement.textContent = days.toString().padStart(2, '0');
            hoursElement.textContent = hours.toString().padStart(2, '0');
            minutesElement.textContent = minutes.toString().padStart(2, '0');
            secondsElement.textContent = seconds.toString().padStart(2, '0');

            if (distance < 0) {
                clearInterval(interval);
                countdownElement.textContent = "EXPIRED";
            }
        }

        // Update the countdown every 1 second
        const interval = setInterval(updateCountdown, 1000);

        // Initial call to set the correct initial values
        updateCountdown();
    } else {
        console.log("Countdown elements not found. Skipping countdown initialization.");
    }
});

// =================== counter end here =================== //




// =================== print button style =================== //
function printInvoice() {
    window.print();
};





document.addEventListener('DOMContentLoaded', function () {
    // Shop cart +/- functionality
    const cartPlusMinusElements = document.querySelectorAll('.cart-plus-minus');

    cartPlusMinusElements.forEach(element => {
        const decButton = document.createElement('div');
        decButton.className = 'dec qtybutton';
        decButton.textContent = '-';
        element.prepend(decButton);

        const incButton = document.createElement('div');
        incButton.className = 'inc qtybutton';
        incButton.textContent = '+';
        element.append(incButton);

        const qtyButtons = element.querySelectorAll('.qtybutton');
        qtyButtons.forEach(button => {
            button.addEventListener('click', function () {
                const input = this.parentElement.querySelector('.form-control');
                let oldValue = parseFloat(input.value);
                let newVal;

                if (this.textContent === '+') {
                    newVal = oldValue + 1;
                } else {
                    newVal = oldValue > 0 ? oldValue - 1 : 1;
                }

                input.value = newVal;
            });
        });
    });
});

//Review Tabs
document.addEventListener('DOMContentLoaded', function () {
    // Review Tabs functionality
    const reviewNav = document.querySelector('ul.review-nav');
    if (reviewNav) {
        reviewNav.addEventListener('click', function (e) {
            if (e.target.tagName === 'LI') {
                e.preventDefault();
                const reviewContent = document.querySelector('.review-content');
                const viewRev = e.target.dataset.target;

                // Remove active class from all list items
                this.querySelectorAll('li').forEach(li => li.classList.remove('active'));

                // Add active class to clicked list item
                e.target.classList.add('active');

                // Update review content classes
                reviewContent.classList.remove('review-content-show', 'description-show');
                reviewContent.classList.add(viewRev);
            }
        });
    }
});

//quantity btn
document.addEventListener('DOMContentLoaded', function () {
    const quantityButtons = document.querySelectorAll('.quantity-button');

    quantityButtons.forEach(function (button) {
        const decreaseBtn = button.querySelector('.quantity-button__control--decrease');
        const increaseBtn = button.querySelector('.quantity-button__control--increase');
        const quantityDisplay = button.querySelector('.quantity-button__display');

        let quantity = parseInt(quantityDisplay.textContent);

        decreaseBtn.addEventListener('click', function () {
            if (quantity > 0) {
                quantity--;
                updateQuantity();
            }
        });

        increaseBtn.addEventListener('click', function () {
            quantity++;
            updateQuantity();
        });

        function updateQuantity() {
            quantityDisplay.textContent = quantity;
        }
    });
});