/**
 * Social Feed JavaScript
 * Handles likes, comments, and social interactions
 */

class SocialFeed {
  constructor() {
    this.init();
  }

  init() {
    this.setupLikeButtons();
    this.setupCommentButtons();
    this.setupCommentForms();
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

  // Setup comment toggle functionality
  setupCommentButtons() {
    document.querySelectorAll('.comment-btn').forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleComments(button);
      });
    });
  }

  // Setup comment form submission
  setupCommentForms() {
    document.querySelectorAll('.comment-form').forEach(form => {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleCommentSubmit(form);
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
        },
        credentials: 'same-origin'
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

  // Toggle comments section
  async toggleComments(button) {
    const goalId = button.dataset.goalId;
    const commentsUrl = button.dataset.commentsUrl;
    const commentsSection = document.getElementById(`comments-${goalId}`);
    const commentsList = commentsSection.querySelector('.comments-list');

    if (commentsSection.style.display === 'none' || !commentsSection.style.display) {
      // Show comments
      commentsSection.style.display = 'block';
      commentsSection.classList.add('slide-down');

      // Load comments if not already loaded
      if (!commentsList.dataset.loaded) {
        await this.loadComments(goalId, commentsUrl, commentsList);
      }
    } else {
      // Hide comments
      commentsSection.style.display = 'none';
      commentsSection.classList.remove('slide-down');
    }
  }

  // Load comments via AJAX
  async loadComments(goalId, commentsUrl, commentsList) {
    try {
      commentsList.innerHTML = '<div class="loading-comments"><div class="spinner"></div> Loading comments...</div>';
      
      const response = await fetch(commentsUrl, {
        credentials: 'same-origin'
      });

      const data = await response.json();
      
      if (response.ok) {
        this.renderComments(data, commentsList);
        commentsList.dataset.loaded = 'true';
      } else {
        commentsList.innerHTML = '<div class="text-muted text-center py-3">Failed to load comments</div>';
      }
    } catch (error) {
      commentsList.innerHTML = '<div class="text-muted text-center py-3">Error loading comments</div>';
    }
  }

  // Render comments in the UI
  renderComments(comments, container) {
    if (comments.length === 0) {
      container.innerHTML = '<div class="text-muted text-center py-3">No comments yet. Be the first to comment!</div>';
      return;
    }

    const commentsHtml = comments.map(comment => `
      <div class="comment-item">
        <div class="comment-avatar">
          <i data-lucide="user" style="width: 14px; height: 14px;"></i>
        </div>
        <div class="comment-content">
          <div class="comment-header">
            <span class="comment-username">${comment.user__username}</span>
            <span class="comment-time">${this.formatTime(comment.created_at)}</span>
          </div>
          <div class="comment-text">${comment.text}</div>
        </div>
      </div>
    `).join('');

    container.innerHTML = commentsHtml;
  }

  // Handle comment form submission
  async handleCommentSubmit(form) {
    const goalId = form.dataset.goalId;
    const commentsUrl = form.dataset.commentsUrl;
    const input = form.querySelector('.comment-input');
    const commentText = input.value.trim();

    if (!commentText) return;

    // Disable form during submission
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnContent = submitBtn.innerHTML;
    submitBtn.innerHTML = '<div class="spinner"></div>';
    submitBtn.disabled = true;
    input.disabled = true;

    try {
      const response = await fetch(commentsUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify({ text: commentText })
      });

      const data = await response.json();

      if (response.ok) {
        // Add new comment to the list
        const commentsList = form.closest('.comments-section').querySelector('.comments-list');
        this.addNewComment(data, commentsList);
        
        // Update comment count
        const commentBtn = document.querySelector(`[data-goal-id="${goalId}"].comment-btn`);
        const commentCount = commentBtn.querySelector('.comment-count');
        commentCount.textContent = parseInt(commentCount.textContent) + 1;
        
        // Clear form
        input.value = '';
      } else {
        this.showError('Failed to post comment');
      }
    } catch (error) {
      this.showError('Network error');
    } finally {
      // Re-enable form
      submitBtn.innerHTML = originalBtnContent;
      submitBtn.disabled = false;
      input.disabled = false;
    }
  }

  // Add new comment to the comments list
  addNewComment(comment, commentsList) {
    const newCommentHtml = `
      <div class="comment-item new-comment">
        <div class="comment-avatar">
          <i data-lucide="user" style="width: 14px; height: 14px;"></i>
        </div>
        <div class="comment-content">
          <div class="comment-header">
            <span class="comment-username">${comment.user}</span>
            <span class="comment-time">just now</span>
          </div>
          <div class="comment-text">${comment.text}</div>
        </div>
      </div>
    `;

    if (commentsList.innerHTML.includes('No comments yet')) {
      commentsList.innerHTML = newCommentHtml;
    } else {
      commentsList.insertAdjacentHTML('beforeend', newCommentHtml);
    }

    // Re-initialize icons for new content
    lucide.createIcons();
    
    // Scroll to new comment
    const newComment = commentsList.querySelector('.new-comment');
    newComment.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Remove new-comment class after animation
    setTimeout(() => {
      newComment.classList.remove('new-comment');
    }, 1000);
  }

  // Utility functions
  getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
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