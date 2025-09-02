/**
 * Modern UI JavaScript Module
 * Handles animations, interactions, and dynamic behaviors
 */

class ModernUI {
  constructor() {
    this.init();
  }

  init() {
    this.setupAnimations();
    this.setupFormEnhancements();
    this.setupProgressAnimations();
    this.setupTooltips();
  }

  // Fade in elements as they come into view
  setupAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe all cards and major sections
    document.querySelectorAll('.modern-card, .chart-container, .hero-section').forEach(el => {
      observer.observe(el);
    });
  }

  // Enhanced form interactions
  setupFormEnhancements() {
    // Add floating label effect
    document.querySelectorAll('.modern-form-control').forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });

      input.addEventListener('blur', () => {
        if (!input.value) {
          input.parentElement.classList.remove('focused');
        }
      });

      // Check if already has value on page load
      if (input.value) {
        input.parentElement.classList.add('focused');
      }
    });

    // Form validation feedback
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', (e) => {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
          if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
          } else {
            field.classList.remove('is-invalid');
          }
        });

        if (!isValid) {
          e.preventDefault();
          this.showNotification('Please fill in all required fields', 'error');
        }
      });
    });
  }

  // Animate progress bars
  setupProgressAnimations() {
    document.querySelectorAll('.modern-progress-bar').forEach(bar => {
      const width = bar.style.width;
      bar.style.width = '0%';
      
      setTimeout(() => {
        bar.style.width = width;
      }, 300);
    });
  }

  // Setup tooltips for better UX
  setupTooltips() {
    // Simple tooltip implementation
    document.querySelectorAll('[data-tooltip]').forEach(element => {
      element.addEventListener('mouseenter', (e) => {
        const tooltip = document.createElement('div');
        tooltip.className = 'modern-tooltip';
        tooltip.textContent = e.target.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);

        const rect = e.target.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
      });

      element.addEventListener('mouseleave', () => {
        document.querySelectorAll('.modern-tooltip').forEach(tooltip => {
          tooltip.remove();
        });
      });
    });
  }

  // Show notifications
  showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `modern-notification modern-notification-${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <span>${message}</span>
        <button class="notification-close">&times;</button>
      </div>
    `;

    document.body.appendChild(notification);

    // Position notification
    const notifications = document.querySelectorAll('.modern-notification');
    notification.style.top = `${20 + (notifications.length - 1) * 80}px`;

    // Auto remove
    setTimeout(() => {
      this.removeNotification(notification);
    }, duration);

    // Manual close
    notification.querySelector('.notification-close').addEventListener('click', () => {
      this.removeNotification(notification);
    });
  }

  removeNotification(notification) {
    notification.style.transform = 'translateX(400px)';
    notification.style.opacity = '0';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }

  // Smooth scroll to element
  scrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }

  // Loading state management
  showLoading(container) {
    const loader = document.createElement('div');
    loader.className = 'loading-container';
    loader.innerHTML = `
      <div class="spinner"></div>
      <p>Loading...</p>
    `;
    container.innerHTML = '';
    container.appendChild(loader);
  }

  hideLoading(container) {
    const loader = container.querySelector('.loading-container');
    if (loader) {
      loader.remove();
    }
  }
}

// Additional notification styles
const notificationStyles = `
.modern-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  min-width: 300px;
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  transform: translateX(400px);
  opacity: 0;
  transition: all 0.3s ease;
  animation: slideInRight 0.3s ease forwards;
}

@keyframes slideInRight {
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.modern-notification-info {
  background-color: var(--primary-50);
  border-left: 4px solid var(--primary-500);
  color: var(--primary-700);
}

.modern-notification-success {
  background-color: var(--success-50);
  border-left: 4px solid var(--success-500);
  color: var(--success-700);
}

.modern-notification-error {
  background-color: var(--error-50);
  border-left: 4px solid var(--error-500);
  color: var(--error-700);
}

.notification-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  margin-left: var(--space-4);
  opacity: 0.7;
}

.notification-close:hover {
  opacity: 1;
}

.modern-tooltip {
  position: absolute;
  background: var(--neutral-800);
  color: white;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  z-index: 1000;
  pointer-events: none;
  animation: fadeIn 0.2s ease;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  color: var(--neutral-500);
}

.loading-container p {
  margin-top: var(--space-4);
  font-weight: 500;
}
`;

// Inject notification styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Initialize Modern UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.modernUI = new ModernUI();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ModernUI;
}