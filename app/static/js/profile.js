// PROFILE PAGE JAVASCRIPT


document.addEventListener('DOMContentLoaded', function() {
    
    
    // THEME TOGGLE
    
    const themeButtons = document.querySelectorAll('.theme-option');
    
    themeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const theme = button.dataset.theme;
            
            // Remove active class from all buttons
            themeButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Apply theme to body
            if (theme === 'light') {
                document.body.classList.add('light-theme');
            } else {
                document.body.classList.remove('light-theme');
            }
            
            // Save theme to database
            fetch('/update-theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ theme: theme })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Theme updated!', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to save theme', 'danger');
            });
        });
    });
    
    // AVATAR MODAL
    
    const avatarModal = document.getElementById('avatar-modal');
    const changeAvatarBtn = document.getElementById('change-avatar-btn');
    const avatarChoices = document.querySelectorAll('.avatar-choice');
    const saveAvatarBtn = document.getElementById('save-avatar-btn');
    let selectedAvatar = null;
    
    // Open avatar modal
    if (changeAvatarBtn) {
        changeAvatarBtn.addEventListener('click', function() {
            avatarModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    }
    
    // Select avatar
    avatarChoices.forEach(function(choice) {
        choice.addEventListener('click', function() {
            // Remove selected class from all
            avatarChoices.forEach(c => c.classList.remove('selected'));
            
            // Add selected class to clicked
            choice.classList.add('selected');
            
            // Store selected avatar
            selectedAvatar = choice.dataset.avatar;
        });
    });
    
    // Save avatar
    if (saveAvatarBtn) {
        saveAvatarBtn.addEventListener('click', function() {
            if (!selectedAvatar) {
                showNotification('Please select an avatar', 'warning');
                return;
            }
            
            // Send to server
            fetch('/auth/update-avatar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ avatar: selectedAvatar })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Avatar updated!', 'success');
                    // Reload page to show new avatar
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    showNotification(data.error || 'Failed to update avatar', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to update avatar', 'danger');
            });
        });
    }
    
    // BIO MODAL
    
    const bioModal = document.getElementById('bio-modal');
    const editBioBtn = document.getElementById('edit-bio-btn');
    const bioTextarea = document.getElementById('bio');
    const charCount = document.querySelector('.char-count');
    
    // Open bio modal
    if (editBioBtn) {
        editBioBtn.addEventListener('click', function() {
            bioModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Focus textarea
            if (bioTextarea) {
                bioTextarea.focus();
            }
        });
    }
    
    // Update character count
    if (bioTextarea && charCount) {
        bioTextarea.addEventListener('input', function() {
            const length = bioTextarea.value.length;
            charCount.textContent = length + '/500';
            
            // Change color if near limit
            if (length > 450) {
                charCount.style.color = 'var(--warning)';
            } else {
                charCount.style.color = 'var(--text-muted)';
            }
        });
    }
    
    // DELETE ACCOUNT CONFIRMATION
    
    const deleteAccountBtn = document.getElementById('delete-account-btn');
    
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            const confirmed = confirm(
                '⚠️ WARNING ⚠️\n\n' +
                'Are you ABSOLUTELY SURE you want to delete your account?\n\n' +
                'This will permanently delete:\n' +
                '• Your profile\n' +
                '• Your watchlist\n' +
                '• Your ratings\n' +
                '• All your data\n\n' +
                'THIS CANNOT BE UNDONE!\n\n' +
                'Type "DELETE" in the next prompt to confirm.'
            );
            
            if (confirmed) {
                const confirmation = prompt('Type DELETE to confirm account deletion:');
                
                if (confirmation === 'DELETE') {
                    // Send delete request
                    fetch('/auth/delete-account', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            showNotification('Account deleted. Redirecting...', 'success');
                            setTimeout(function() {
                                window.location.href = '/';
                            }, 2000);
                        } else {
                            showNotification(data.error || 'Failed to delete account', 'danger');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showNotification('Failed to delete account', 'danger');
                    });
                } else {
                    showNotification('Account deletion cancelled', 'info');
                }
            }
        });
    }
    
    // EDIT INFO BUTTON 
    
    const editInfoBtn = document.getElementById('edit-info-btn');
    
    if (editInfoBtn) {
        editInfoBtn.addEventListener('click', function() {
            showNotification('Edit info feature coming soon!', 'info');
            // TODO: Will implement this later
        });
    }
    
    // CHANGE PASSWORD BUTTON (Placeholder)
    
    const changePasswordBtn = document.getElementById('change-password-btn');
    
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function() {
            showNotification('Change password feature coming soon!', 'info');
            // TODO: Will implement this later
        });
    }
    
});

// MODAL CLOSE FUNCTIONS

function closeAvatarModal() {
    const modal = document.getElementById('avatar-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function closeBioModal() {
    const modal = document.getElementById('bio-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modals on outside click
window.addEventListener('click', function(event) {
    const avatarModal = document.getElementById('avatar-modal');
    const bioModal = document.getElementById('bio-modal');
    
    if (event.target === avatarModal) {
        closeAvatarModal();
    }
    
    if (event.target === bioModal) {
        closeBioModal();
    }
});

// Close modals on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeAvatarModal();
        closeBioModal();
    }
});

// NOTIFICATION HELPER (Reuse from other files)

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
    
    // Auto-remove after 3 seconds
    setTimeout(function() {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            notification.remove();
        }, 300);
    }, 3000);
}

// Get CSRF token from meta tag

function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}