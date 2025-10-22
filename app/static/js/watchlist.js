document.addEventListener('DOMContentLoaded', function(){
    
    // ========================================
    // EPISODE INCREMENT BUTTONS
    // ========================================
    
    const incrementButtons = document.querySelectorAll('.episode-increase');
    incrementButtons.forEach(function(button) {
        button.addEventListener('click', function(){
            const itemId = button.dataset.itemId;
            const card = button.closest('.watchlist-card');
            
            fetch(`/watchlist/episode/increment/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    updateProgress(card, data.episodes_watched, data.total_episodes);

                    // If anime was auto-completed, show message and redirect
                    if (data.auto_completed) {
                        showNotification('🎉 Completed! Moving to Completed tab...', 'success');

                        // Redirect to completed tab after 1.5 seconds
                        setTimeout(function() {
                            window.location.href = '/watchlist?status=completed';
                        }, 1500);
                    }
                } else {
                    showNotification(data.error || 'Failed to update episode', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Network error. Please try again.', 'danger');
            });
        });
    });

    // ========================================
    // EPISODE DECREMENT BUTTONS
    // ========================================
    
    const decrementButtons = document.querySelectorAll('.episode-decrease');
    decrementButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const itemId = button.dataset.itemId;
            const card = button.closest('.watchlist-card');

            fetch(`/watchlist/episode/decrement/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateProgress(card, data.episodes_watched, data.total_episodes);

                    if (data.status_changed) {
                        showNotification('Status changed back to Watching', 'info');
                        updateStatusBadge(card, data.status);
                    }
                } else {
                    showNotification(data.error || 'Failed to update episode', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Network error. Please try again.', 'danger');
            });
        });
    });

    // ========================================
    // REMOVE BUTTONS
    // ========================================
    
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(function(button){
        button.addEventListener('click', function(){
            const itemId = button.dataset.itemId;
            const animeTitle = button.dataset.animeTitle;
            const card = button.closest('.watchlist-card');

            if (!confirm(`Remove "${animeTitle}" from watchlist?`)){
                return;
            }
            
            fetch(`/watchlist/remove/${itemId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    card.style.transition = 'all 0.3s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.8)';

                    setTimeout(function(){
                        card.remove();
                        showNotification(data.message, 'success');

                        const grid = document.querySelector('.watchlist-grid');
                        if (grid && grid.children.length === 0) {
                            location.reload();
                        }
                    }, 300);
                } else {
                    showNotification(data.error || 'Failed to remove from watchlist', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Network error. Please try again.', 'danger');
            });
        });
    });
});

// ========================================
// HELPER FUNCTIONS
// ========================================

/**
 * Update progress display on a card
 */
function updateProgress(card, episodesWatched, totalEpisodes) {  // ✅ Fixed typo
    // Update progress text
    const progressText = card.querySelector('.progress-text');
    if (progressText && totalEpisodes) {  // ✅ Fixed typo
        progressText.textContent = `${episodesWatched} / ${totalEpisodes} episodes`;  // ✅ Fixed typo
    }

    // Update circular progress
    if (totalEpisodes) {  // ✅ Fixed typo
        const percentage = (episodesWatched / totalEpisodes) * 100;  // ✅ Fixed typo
        const circle = card.querySelector('.progress-ring-circle');

        if (circle) {
            const circumference = 326.73;
            const offset = circumference * (1 - episodesWatched / totalEpisodes);  // ✅ Fixed typo
            circle.style.strokeDashoffset = offset;
        }

        // Update percentage text
        const percentValue = card.querySelector('.percent-value');
        if (percentValue) {
            percentValue.textContent = `${Math.round(percentage)}%`;
        }
    }

    // Update button states
    const decreaseBtn = card.querySelector('.episode-decrease');
    const increaseBtn = card.querySelector('.episode-increase');

    if (decreaseBtn) {
        decreaseBtn.disabled = episodesWatched <= 0;  // ✅ Fixed typo (was 'disabledd')
    }

    if (increaseBtn && totalEpisodes) {  // ✅ Fixed typo
        increaseBtn.disabled = episodesWatched >= totalEpisodes;  // ✅ Fixed typos
    }
}

/**
 * Update status badge on a card
 */
function updateStatusBadge(card, status) {
    const badge = card.querySelector('.status-badge');
    if (badge) {
        badge.className = `status-badge status-${status}`;
        
        // ✅ Moved inside if statement
        const formattedStatus = status
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
        
        badge.textContent = formattedStatus;
    }
}

/**
 * Show notification message
 */
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.style.cssText = `  
        position: fixed;
        top: 80px;
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

    // Auto-remove after 3 seconds
    setTimeout(function(){
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function(){
            notification.remove();
        }, 300);  // ✅ Fixed delay (was 3000)
    }, 3000);
}