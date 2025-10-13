// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Radio button styling
document.querySelectorAll('.choice-option').forEach(function(option) {
    option.addEventListener('click', function() {
        const radio = this.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
    });
});

// Add fade-in animation to cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.poll-card').forEach(card => {
    observer.observe(card);
});

// Confirm before logout
function confirmLogout(event) {
    if (!confirm('Are you sure you want to logout?')) {
        event.preventDefault();
    }
}

// Form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

// Live vote count animation
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Animate vote counts on results page
document.querySelectorAll('.vote-count').forEach(element => {
    const finalValue = parseInt(element.textContent);
    animateValue(element, 0, finalValue, 1000);
});
