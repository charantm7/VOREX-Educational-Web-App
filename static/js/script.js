document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("nav-links");

  // Toggle nav-links on hamburger click
  hamburger.addEventListener("click", (e) => {
    navLinks.classList.toggle("active");
    e.stopPropagation(); // Stop click from propagating to the body
  });

  // Close nav-links when clicking anywhere on the body
  document.body.addEventListener("click", () => {
    navLinks.classList.remove("active");
  });

  // Prevent menu from closing when clicking inside nav-links
  navLinks.addEventListener("click", (e) => {
    e.stopPropagation();
  });
});
