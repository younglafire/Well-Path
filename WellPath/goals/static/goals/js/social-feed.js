/**
 * Social Feed JavaScript
 * Handles likes, and social interactions
 */

class SocialFeed {
  constructor() {
    this.init();
  }

  init() {
    this.setupLikeButtons();
  }

  // Setup like button functionality
  setupLikeButtons() {
    document.querySelectorAll('.like-btn').forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        this.handleLike(button);
      });
    });
  }



  // Handle like button click
  async handleLike(button) {
    const goalId = button.dataset.goalId;
    const likeUrl = button.dataset.likeUrl;
    const likeCount = button.querySelector('.like-count');
    
    // Optimistic UI update
    const wasLiked = button.classList.contains('liked');
    button.classList.toggle('liked');
    likeCount.textContent = parseInt(likeCount.textContent) + (wasLiked ? -1 : 1);

    try {
      const response = await fetch(likeUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'  // Add this to identify AJAX requests
        },
        credentials: 'include'  // Changed from same-origin to include
      });

      const data = await response.json();
      
      if (response.ok) {
        // Update with server response
        likeCount.textContent = data.likes_count;
        if (data.liked) {
          button.classList.add('liked');
        } else {
          button.classList.remove('liked');
        }
      } else {
        // Revert optimistic update on error
        button.classList.toggle('liked');
        likeCount.textContent = parseInt(likeCount.textContent) + (wasLiked ? 1 : -1);
        this.showError('Failed to update like');
      }
    } catch (error) {
      // Revert optimistic update on error
      button.classList.toggle('liked');
      likeCount.textContent = parseInt(likeCount.textContent) + (wasLiked ? 1 : -1);
      this.showError('Network error');
    }
  }


 
  // Utility functions
  getCsrfToken() {
    // First try to get from csrf_token input
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (tokenInput) return tokenInput.value;
    
    // Then try to get from meta tag
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    if (tokenMeta) return tokenMeta.content;
    
    return '';
  }

  formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}d`;
    return date.toLocaleDateString();
  }

  showError(message) {
    // Use the existing modern UI notification system
    if (window.modernUI) {
      window.modernUI.showNotification(message, 'error');
    } else {
      alert(message);
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new SocialFeed();
});