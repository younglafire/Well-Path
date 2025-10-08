document.addEventListener('DOMContentLoaded', function () {
  const tabs = {
    'active': document.querySelector('#active-tab'),
    'completed': document.querySelector('#completed-tab'),
    'overdue': document.querySelector('#overdue-tab'),
  };
  const container = document.querySelector('#dashboard-content');

  // Define load_dashboard in outer scope
  function load_dashboard(filter = "active") {
    // Show loading state
    container.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading goals...</p>
      </div>
    `;

    fetch(`/api/goals?status=${filter}`, { credentials: "same-origin" })
      .then(r => {
        if (!r.ok) {
          throw new Error(`HTTP error! status: ${r.status}`);
        }
        return r.json();
      })
      .then(data => {
        container.innerHTML = `<div class="row">${data.html}</div>`;
        lucide.createIcons();
        container.classList.add('fade-in');
        
        // Prevent card click when interacting with progress form
        document.querySelectorAll('.goal-progress-form').forEach(form => {
          form.addEventListener('click', function(event) {
            event.stopPropagation();
          });
        });
      })
      .catch((error) => {
        console.error('Error loading goals:', error);
        container.innerHTML = `
          <div class="modern-card text-center">
            <div class="modern-card-body py-5">
              <i data-lucide="wifi-off" style="width: 48px; height: 48px; color: var(--neutral-400);" class="mb-3"></i>
              <h4 class="text-muted">Connection Error</h4>
              <p class="text-muted">Unable to load goals. Please try again.</p>
              <button class="btn btn-primary-modern" onclick="window.dashboardRetry('${filter}')">
                <i data-lucide="refresh-cw" class="me-2"></i>Retry
              </button>
            </div>
          </div>
        `;
        lucide.createIcons();
      });
  }

  // Make retry function globally accessible
  window.dashboardRetry = load_dashboard;

  // Attach event listeners
  Object.keys(tabs).forEach(status => {
    tabs[status].addEventListener('click', () => {
      // Update active tab
      Object.values(tabs).forEach(tab => tab.classList.remove('active'));
      tabs[status].classList.add('active');
      
      load_dashboard(status);
    });
  });

  // Default load
  load_dashboard('active');
});