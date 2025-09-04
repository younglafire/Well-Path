
    document.addEventListener("DOMContentLoaded", function () {
        // Select all like buttons
        const likeButtons = document.querySelectorAll(".like-btn");
      
        likeButtons.forEach(button => {
          button.addEventListener("click", function () {
            const url = this.dataset.likeUrl;   // URL from template
            const countSpan = this.querySelector(".like-count");
      
            fetch(url, {
              method: "POST",
              headers: {
                "X-CSRFToken": getCookie("csrftoken"),  // CSRF token
                "X-Requested-With": "XMLHttpRequest",
              },
            })
            .then(response => response.json())
            .then(data => {
              if (data.liked !== undefined) {
                countSpan.textContent = data.likes_count;
                // Optional: toggle button style
                this.classList.toggle("btn-outline-primary", !data.liked);
                this.classList.toggle("btn-primary", data.liked);
              }
            })
            .catch(err => console.error("Error liking goal:", err));
          });
        });
      
        // Helper to get CSRF token
        function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
              cookie = cookie.trim();
              if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
              }
            }
          }
          return cookieValue;
        }
      });
  