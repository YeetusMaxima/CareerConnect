/* CareerConnect - Main JavaScript (Fixed - No Visible Button on Desktop) */

// ==================== DOCUMENT READY ====================
document.addEventListener("DOMContentLoaded", function () {
  initMobileMenuFixed(); // Fixed version
  initFormValidation();
  initPasswordToggle();
  initCharacterCount();
  initAutoHideMessages();
  initConfirmDialogs();
  initSmoothScroll();
  initBackToTop();
  initImagePreview();
});

// ==================== MOBILE MENU (FIXED VERSION) ====================
function initMobileMenuFixed() {
  // Only create button if screen is mobile
  if (window.innerWidth <= 768) {
    createMobileMenu();
  }

  // Listen for window resize
  window.addEventListener("resize", function () {
    const existingToggle = document.querySelector(".mobile-menu-toggle");

    if (window.innerWidth <= 768 && !existingToggle) {
      createMobileMenu();
    } else if (window.innerWidth > 768 && existingToggle) {
      existingToggle.remove();
      const navMenu = document.querySelector(".nav-menu");
      if (navMenu) {
        navMenu.classList.remove("active");
      }
    }
  });
}

function createMobileMenu() {
  const navbar = document.querySelector(".navbar");
  const navMenu = document.querySelector(".nav-menu");

  if (!navbar || !navMenu) return;

  // Check if toggle already exists
  if (document.querySelector(".mobile-menu-toggle")) return;

  // Create toggle button
  const menuToggle = document.createElement("button");
  menuToggle.className = "mobile-menu-toggle";
  menuToggle.setAttribute("aria-label", "Toggle menu");
  menuToggle.innerHTML = `
        <div class="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

  // Insert before nav menu
  navbar.insertBefore(menuToggle, navMenu);

  // Toggle menu
  menuToggle.addEventListener("click", function (e) {
    e.stopPropagation();
    navMenu.classList.toggle("active");
    this.classList.toggle("active");
  });

  // Close menu when clicking outside
  document.addEventListener("click", function (e) {
    if (!navbar.contains(e.target)) {
      navMenu.classList.remove("active");
      menuToggle.classList.remove("active");
    }
  });

  // Close menu when clicking a link
  const navLinks = navMenu.querySelectorAll("a");
  navLinks.forEach((link) => {
    link.addEventListener("click", function () {
      navMenu.classList.remove("active");
      menuToggle.classList.remove("active");
    });
  });
}

// ==================== FORM VALIDATION ====================
function initFormValidation() {
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          showFieldError(field, "This field is required");
        } else {
          clearFieldError(field);
        }
      });

      // Email validation
      const emailFields = form.querySelectorAll('input[type="email"]');
      emailFields.forEach((field) => {
        if (field.value && !isValidEmail(field.value)) {
          isValid = false;
          showFieldError(field, "Please enter a valid email address");
        }
      });

      if (!isValid) {
        e.preventDefault();
      }
    });

    // Real-time validation
    const inputs = form.querySelectorAll("input, textarea, select");
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        if (this.hasAttribute("required") && !this.value.trim()) {
          showFieldError(this, "This field is required");
        } else if (
          this.type === "email" &&
          this.value &&
          !isValidEmail(this.value)
        ) {
          showFieldError(this, "Please enter a valid email address");
        } else {
          clearFieldError(this);
        }
      });

      input.addEventListener("input", function () {
        if (this.value.trim()) {
          clearFieldError(this);
        }
      });
    });
  });
}

function showFieldError(field, message) {
  clearFieldError(field);

  const errorDiv = document.createElement("div");
  errorDiv.className = "field-error-message";
  errorDiv.textContent = message;
  errorDiv.style.cssText =
    "color: #ef4444; font-size: 0.875rem; margin-top: 0.25rem; font-weight: 500;";

  field.style.borderColor = "#ef4444";
  field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
  const errorMsg = field.parentNode.querySelector(".field-error-message");
  if (errorMsg) {
    errorMsg.remove();
  }
  field.style.borderColor = "";
}

function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// ==================== PASSWORD TOGGLE ====================
function initPasswordToggle() {
  const passwordFields = document.querySelectorAll('input[type="password"]');

  passwordFields.forEach((field) => {
    const wrapper = document.createElement("div");
    wrapper.style.position = "relative";
    field.parentNode.insertBefore(wrapper, field);
    wrapper.appendChild(field);

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.innerHTML = "👁️";
    toggleBtn.className = "password-toggle-btn";
    toggleBtn.style.cssText = `
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            border: none;
            background: none;
            cursor: pointer;
            font-size: 1.2rem;
            opacity: 0.6;
            transition: opacity 0.3s;
        `;

    wrapper.appendChild(toggleBtn);

    toggleBtn.addEventListener("mouseenter", function () {
      this.style.opacity = "1";
    });

    toggleBtn.addEventListener("mouseleave", function () {
      this.style.opacity = "0.6";
    });

    toggleBtn.addEventListener("click", function () {
      if (field.type === "password") {
        field.type = "text";
        this.innerHTML = "🙈";
      } else {
        field.type = "password";
        this.innerHTML = "👁️";
      }
    });
  });
}

// ==================== CHARACTER COUNT ====================
function initCharacterCount() {
  const textareas = document.querySelectorAll("textarea[maxlength]");

  textareas.forEach((textarea) => {
    const maxLength = textarea.getAttribute("maxlength");

    const counter = document.createElement("div");
    counter.className = "char-counter";
    counter.style.cssText =
      "text-align: right; font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;";

    textarea.parentNode.appendChild(counter);

    function updateCounter() {
      const remaining = maxLength - textarea.value.length;
      counter.textContent = `${textarea.value.length} / ${maxLength} characters`;

      if (remaining < 50) counter.style.color = "#f59e0b";
      if (remaining < 20) counter.style.color = "#ef4444";
      if (remaining > 50) counter.style.color = "#6b7280";
    }

    updateCounter();
    textarea.addEventListener("input", updateCounter);
  });
}

// ==================== AUTO-HIDE MESSAGES ====================
function initAutoHideMessages() {
  const messages = document.querySelectorAll(".message");

  messages.forEach((message) => {
    // Add close button
    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.style.cssText = `
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: inherit;
            opacity: 0.7;
            transition: opacity 0.3s;
        `;

    message.style.position = "relative";
    message.appendChild(closeBtn);

    closeBtn.addEventListener("mouseenter", function () {
      this.style.opacity = "1";
    });

    closeBtn.addEventListener("mouseleave", function () {
      this.style.opacity = "0.7";
    });

    closeBtn.addEventListener("click", function () {
      message.style.animation = "slideOut 0.3s ease-out";
      setTimeout(() => message.remove(), 300);
    });

    // Auto-hide after 5 seconds
    setTimeout(() => {
      message.style.animation = "fadeOut 0.5s ease-out";
      setTimeout(() => message.remove(), 500);
    }, 5000);
  });
}

// Add animations
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
    }
`;
document.head.appendChild(style);

// ==================== CONFIRM DIALOGS ====================
function initConfirmDialogs() {
  const deleteButtons = document.querySelectorAll("[data-confirm]");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const message = this.getAttribute("data-confirm");
      if (!confirm(message || "Are you sure?")) {
        e.preventDefault();
      }
    });
  });
}

// ==================== SMOOTH SCROLL ====================
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href === "#") return;

      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// ==================== BACK TO TOP BUTTON ====================
function initBackToTop() {
  const backToTopBtn = document.createElement("button");
  backToTopBtn.innerHTML = "↑";
  backToTopBtn.className = "back-to-top";
  backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s;
    `;

  document.body.appendChild(backToTopBtn);

  window.addEventListener("scroll", function () {
    if (window.pageYOffset > 300) {
      backToTopBtn.style.display = "block";
    } else {
      backToTopBtn.style.display = "none";
    }
  });

  backToTopBtn.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  backToTopBtn.addEventListener("mouseenter", function () {
    this.style.transform = "scale(1.1)";
    this.style.boxShadow = "0 6px 16px rgba(0,0,0,0.2)";
  });

  backToTopBtn.addEventListener("mouseleave", function () {
    this.style.transform = "scale(1)";
    this.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
  });
}

// ==================== IMAGE PREVIEW ====================
// ==================== IMAGE PREVIEW & LABEL ====================
function initImagePreview() {
  const imageInputs = document.querySelectorAll(
    'input[type="file"][accept*="image"]'
  );

  imageInputs.forEach((input) => {
    const wrapper = input.parentNode;
    let label = wrapper.querySelector(".file-input-label");

    // Create label if not exists
    if (!label) {
      label = document.createElement("label");
      label.className = "file-input-label";
      label.textContent = "Upload Company Logo";
      label.style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem;
        border: 2px dashed #e2e8f0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
        margin-top: 0.5rem;
      `;
      wrapper.appendChild(label);
      label.appendChild(input); 
    }

    // Create image preview element
    let preview = wrapper.querySelector(".image-preview-img");
    if (!preview) {
      preview = document.createElement("img");
      preview.className = "image-preview-img";
      preview.style.cssText = `
        max-width: 200px;
        max-height: 200px;
        margin-top: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      `;
      wrapper.appendChild(preview);
      preview.style.display = "none"; // hide initially
    }

    // Update preview and label on file select
    input.addEventListener("change", function () {
      const file = input.files[0];

      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.src = e.target.result;
          preview.style.display = "block"; // show preview
        };
        reader.readAsDataURL(file);

        label.textContent = file.name;
        label.classList.add("has-file");
      } else {
        // Reset if no file
        preview.src = "";
        preview.style.display = "none";
        label.textContent = "Upload Company Logo";
        label.classList.remove("has-file");
      }
    });
  });
}


// ==================== UTILITY FUNCTIONS ====================
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: ${
          type === "success"
            ? "#10b981"
            : type === "error"
            ? "#ef4444"
            : "#2563eb"
        };
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
    `;

  const styleSheet = document.createElement("style");
  styleSheet.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
  document.head.appendChild(styleSheet);

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOutRight 0.3s ease-out";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

console.log("CareerConnect JS loaded successfully! 🚀");
console.log("Mobile menu: Only visible on screens < 768px");
