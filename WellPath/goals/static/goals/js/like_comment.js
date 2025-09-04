
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

        // Comments
// Toggle + load comments
document.querySelectorAll(".comment-btn").forEach(button => {
    button.addEventListener("click", function () {
      const goalId = this.dataset.goalId;
      const url = this.dataset.commentsUrl;
      const commentSection = document.getElementById(`comments-${goalId}`);
  
      if (commentSection.style.display === "none") {
        commentSection.style.display = "block";
  
        // Load comments if empty
        const list = commentSection.querySelector(".comment-list");
        if (!list.dataset.loaded) {
          fetch(url, { credentials: "same-origin" })
            .then(r => r.json())
            .then(data => {
              list.innerHTML = "";
              data.comments.forEach(c => {
                const div = document.createElement("div");
                div.className = "comment mb-1";
                div.innerHTML = `<strong>${c.user}</strong>: ${c.text}`;
                list.appendChild(div);
              });
              list.dataset.loaded = "true";
            })
            .catch(() => {
              list.innerHTML = "<p class='text-muted'>Error loading comments.</p>";
            });
        }
  
      } else {
        commentSection.style.display = "none";
      }
    });
  });
  
  // Submit new comment
  document.querySelectorAll(".comment-form").forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const goalId = this.dataset.goalId;
      const url = this.dataset.commentsUrl;
      const input = this.querySelector(".comment-input");
      const list = this.closest(".comments-container").querySelector(".comment-list");
  
      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
          "Content-Type": "application/json"
        },
        credentials: "same-origin",
        body: JSON.stringify({ text: input.value })
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            const div = document.createElement("div");
            div.className = "comment mb-1";
            div.innerHTML = `<strong>${data.comment.user}</strong>: ${data.comment.text}`;
            list.appendChild(div);
            input.value = "";
          }
        });
    });
  });
  

      });


  