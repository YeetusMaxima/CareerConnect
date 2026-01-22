// ===================================
// CareerConnect - MINIMAL JavaScript
// Only the absolutely necessary stuff
// ===================================

document.addEventListener("DOMContentLoaded", function () {
  // 1. Mobile menu toggle
  const navbar = document.querySelector(".navbar");
  const navMenu = document.querySelector(".nav-menu");

  if (navbar && navMenu && window.innerWidth <= 768) {
    const menuBtn = document.createElement("button");
    menuBtn.className = "mobile-menu-toggle";
    menuBtn.innerHTML = "<span></span><span></span><span></span>";
    navbar.insertBefore(menuBtn, navMenu);

    menuBtn.onclick = () => navMenu.classList.toggle("active");
  }

  // 2. Auto-close alert messages after 5 seconds
  document.querySelectorAll(".message").forEach((msg) => {
    setTimeout(() => msg.remove(), 5000);
  });

  // 3. Confirm before deleting
  document.querySelectorAll('a[href*="delete"]').forEach((link) => {
    link.onclick = (e) => {
      if (!confirm("Are you sure you want to delete this?")) {
        e.preventDefault();
      }
    };
  });

  console.log("✅ CareerConnect loaded");
});
