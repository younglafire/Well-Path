document.addEventListener('DOMContentLoaded', function () {
  const tabs = {
    'active': document.querySelector('#active-tab'),
    'completed': document.querySelector('#completed-tab'),
    'overdue': document.querySelector('#overdue-tab'),
  };
  const container = document.querySelector('#dashboard-content');

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

  function load_dashboard(filter = "active") {
    // Show loading state
    window.modernUI.showLoading(container);

    fetch(`/api/goals?status=${filter}`, { credentials: "same-origin" })
      .then(r => r.json())
      .then(data => {
        container.innerHTML = `<div class="row">${data.html}</div>`;
        // Re-initialize icons after content load
        lucide.createIcons();
        // Add fade-in animation
        container.classList.add('fade-in');
      })
      .catch(() => {
        container.innerHTML = `
          <div class="modern-card text-center">
            <div class="modern-card-body py-5">
              <i data-lucide="wifi-off" style="width: 48px; height: 48px; color: var(--neutral-400);" class="mb-3"></i>
              <h4 class="text-muted">Connection Error</h4>
              <p class="text-muted">Unable to load goals. Please try again.</p>
              <button class="btn btn-primary-modern" onclick="load_dashboard('${filter}')">
                <i data-lucide="refresh-cw" class="me-2"></i>Retry
              </button>
            </div>
          </div>
        `;
      });
  }
});

