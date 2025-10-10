// base.js

// MODAL FUNCTIONALITY.

const modal = document.getElementById('aboutModal');

function openModal() {
    modal.style.display = 'flex'
    document.body.style.overflow = 'hidden'; // prevent scrolling
}

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Re-enable scrolling
}

// Close modal when clicking outside 
window.onclick = function(event) {
    if (event.target == modal ) {
        closeModal();
    }
}

// close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});



// Flash messages

//Auto-close flash messages after 5 seconds

document.addEventListener('DOMContentLoaded', function(){
    const alerts = document.querySelector('.alert');

    alerts.forEach(function(alert) {
        setTimeout(function(){
            alert.style.opacity = '0';
            setTimeout(function(){
                alert.remove();
            } , 300);
        }, 5000);
    });
});