const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const arrow = document.getElementById('anchor-arrow-1')
const arrowContainer  = document.getElementById('arrow-container')
const frontPageContainer = document.querySelector(".front-text-container")

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
}

const navLink = document.querySelectorAll(".nav-link");

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
  hamburger.classList.remove("active");
  navMenu.classList.remove("active");
}
