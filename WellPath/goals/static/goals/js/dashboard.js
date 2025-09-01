document.addEventListener('DOMContentLoaded', function () {
  const tabs = {
    active: document.querySelector('#active-tab'),
    completed: document.querySelector('#completed-tab'),
    overdue: document.querySelector('#overdue-tab'),
  };
  const container = document.querySelector('#dashboard-content');

  // Attach event listeners in a loop
  Object.keys(tabs).forEach(status => {
    tabs[status].addEventListener('click', () => load_dashboard(status));
  });

  // Default load
  load_dashboard('active');

  function load_dashboard(filter = "active") {
    container.innerHTML = `<h3>Loading ${filter} goals...</h3>`; // temporary loading state

            fetch(`/api/goals?status=${filter}`, { credentials: "same-origin" })
            .then(r => r.json())
            .then(data => {
                container.innerHTML = data.html;
            })
            .catch(() => {
              container.innerHTML = "<p>Error loading goals.</p>";
            });
            }

  function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
});
            fetch(`/api/goals?status=${filter}`, { credentials: "same-origin" })
            .then(r => r.json())
            .then(data => {
                document.querySelector("#dashboard-content").innerHTML = data.html;
            })
            .catch(() => {
              document.querySelector("#dashboard-content").innerHTML = "<p>Error loading goals.</p>";
            });
            

  function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

