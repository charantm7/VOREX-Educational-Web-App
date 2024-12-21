const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menuBtn");

menuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});

// window.addEventListener("load", () => {
//   setTimeout(() => {
//     const preloader = document.getElementById("preloader");
//     preloader.style.opacity = "0";
//     setTimeout(() => {
//       preloader.style.display = "none";
//     }, 100);
//   }, 500);
// });
