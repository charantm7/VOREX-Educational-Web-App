// Toggle upload card
function toggleUploadCard() {
  const uploadSection = document.getElementById("uploadSection");
  uploadSection.classList.toggle("active");
}

// Copy code to clipboard
function copyCode(button) {
  const code = button.getAttribute("data-code");
  navigator.clipboard.writeText(code).then(() => {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> Copied!';
    setTimeout(() => {
      button.innerHTML = originalText;
    }, 2000);
  });
}

// Delete snippet
function deleteSnippet(snippetId) {
  if (confirm("Are you sure you want to delete this code snippet?")) {
    fetch(`/delete-snippet/${snippetId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    }).then((response) => {
      if (response.ok) {
        location.reload();
      }
    });
  }
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Initialize Prism.js
document.addEventListener("DOMContentLoaded", () => {
  Prism.highlightAll();
});
