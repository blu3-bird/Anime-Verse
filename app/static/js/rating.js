// app/static/js/rating.js
document.addEventListener('DOMContentLoaded', function() {
    
    const editRatingBtn = document.getElementById('edit-rating-btn');
    const ratingEditForm = document.getElementById('rating-edit-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');

    // Show edit form  when 'edit rating' is clicked
    if(editRatingBtn) {
        editRatingBtn.addEventListener('click', function() {
            const ratingDisplay = document.querySelector('.rating-display-header');
            const ratingActions = document.querySelector('.rating-actions');
            const ratingDate =  document.querySelector('.rating-date');

            if (ratingDisplay) ratingDisplay.style.display = 'none';
            if (ratingActions) ratingActions.style.display = 'none';
            if (ratingDate) ratingDate.style.display = 'none';

            if (ratingEditForm) {
                ratingEditForm.style.display = 'block';
            }

            ratingEditForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    // cancel editing and go back to display mode

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function(){
            const ratingDisplay = document.querySelector('.rating-display-header');
            const ratingActions = document.querySelector('.rating-actions');
            const ratingDate = document.querySelector('.rating-date');

            if (ratingDisplay) ratingDisplay.style.display = 'flex';
            if (ratingActions) ratingActions.style.display = 'flex';
            if (ratingDate) ratingDate.style.display = 'block';

            if (ratingEditForm) {
                ratingEditForm.style.display = 'none';
            }

            document.querySelector('.rating-section').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }

    // Star Rating Visual feedback

    const starOptions = document.querySelectorAll('.star-option');

    starOptions.forEach(function(option){
        option.addEventListener('click', function(){
            starOptions.forEach(function(opt){
                opt.classList.remove('selected');
            });

            option.classList.add('selected');

            const radio = option.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }

            // Visual feedback: brief scale animation
            option.style.transform = 'scale(1.02)';
            setTimeout(function(){
                option.style.transform = '';
            },200);
        });

        // keyboard accessibility (enter/space to select)
        option.addEventListener('keypress', function(e){
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                option.click();
            }
        });

        option.setAttribute('tabindex', '0');
    });

    // Form Submission Feedback

    const ratingForms = document.querySelectorAll('#rating-form, #edit-rating-form-element');

    ratingForms.forEach(function(form){
        form.addEventListener('submit', function(e){
            const selectedRating = form.querySelector('input[name="score"]:checked');

            if (!selectedRating) {
                e.preventDefault();
                showNotification('Please select a rating!', 'warning');
                return;
            }

            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Saving...';
                submitBtn.disabled = true;

                setTimeout(function(){
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                },3000);
            }
        });
    });

    //Delete Rating Confirmation

    const deleteRatingForm = document.querySelector('form[action*="delete_rating"]');

        if (deleteRatingForm) {
            deleteRatingForm.addEventListener('submit', function(e){

                e.preventDefault();
                
                let animeTitle = 'this anime';
                const titleElement = document.querySelector('.anime-info-main h1');
                if (titleElement && titleElement.textContent) {
                    animeTitle = titleElement.textContent.trim();
                }

                const confirmed = confirm(`Are you sure you want to delete your rating for "${animeTitle}"?\n\n` `This action cannot be undone.`);

                if(confirmed) {
                    const deleteBtn = deleteRatingForm.querySelector('button[type="submit"]');
                    if (deleteBtn) {
                        deleteBtn.textContent = 'Deleting....';
                        deleteBtn.disabled = true;
                    }

                    deleteRatingForm.submit();
                }
            });
        }

        // Rating hover preview

        starOptions.forEach(function(option, index) {
            option.addEventListener('mouseenter', function(){
                for (let i = 0; i <= index; i++) {
                    starOptions[i].style.background = 'rgba(233,69,96,0.08)';
                }
            });

        option.addEventListener('mouseleave', function(){
            starOptions.forEach(function(opt) {
                if (!opt.classList.contains('selected')) {
                    opt.style.background = '';
                }
            });
        });
    });

});

// Helper Function
/** 
@param {string} message
@param {string} type

*/

function showNotification(message, type) {
    const notification = document.createElement('div');
     notification.className = `alert alert-${type}`;
     notification.style.cssText = `
     position: fixed;
     top: 100px;
     right: 20px;
     z-index: 9999;
     min-width: 300px;
     animation: slideIn 0.3s ease;
     `;

     notification.innerHTML = `
     <span>${message}</span>
     <button class="alert-close" onclick="this.parentElement.remove()">&times;</button>
     `;

     document.body.appendChild(notification);

     setTimeout(function(){
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function(){
            notification.remove();
        }, 300);
     }, 3000);
}