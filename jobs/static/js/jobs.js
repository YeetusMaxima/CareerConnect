// ===================================
// CareerConnect - Main JavaScript
// Interactive Features & Functionality
// ===================================

document.addEventListener("DOMContentLoaded", function () {
  // ===================================
  // Mobile Navigation Toggle
  // ===================================
  function initMobileMenu() {
    const navbar = document.querySelector(".navbar");
    const navMenu = document.querySelector(".nav-menu");

    if (!navbar || !navMenu) return;

    // Only add mobile menu on small screens
    if (window.innerWidth <= 768) {
      createMobileMenuButton();
    }

    window.addEventListener("resize", function () {
      const toggle = document.querySelector(".mobile-menu-toggle");
      if (window.innerWidth <= 768 && !toggle) {
        createMobileMenuButton();
      } else if (window.innerWidth > 768 && toggle) {
        toggle.remove();
        navMenu.classList.remove("active");
      }
    });

    function createMobileMenuButton() {
      if (document.querySelector(".mobile-menu-toggle")) return;

      const hamburger = document.createElement("button");
      hamburger.className = "mobile-menu-toggle";
      hamburger.setAttribute("aria-label", "Toggle menu");
      hamburger.innerHTML = "<span></span><span></span><span></span>";

      navbar.insertBefore(hamburger, navMenu);

      hamburger.addEventListener("click", function (e) {
        e.stopPropagation();
        navMenu.classList.toggle("active");
        this.classList.toggle("active");
      });

      document.addEventListener("click", function (e) {
        if (!navbar.contains(e.target)) {
          navMenu.classList.remove("active");
          hamburger.classList.remove("active");
        }
      });
    }
  }

  initMobileMenu();

  // ===================================
  // Form Validation
  // ===================================
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input, textarea, select");

    // Real-time validation
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        validateField(this);
      });

      input.addEventListener("input", function () {
        if (this.value) {
          clearFieldError(this);
        }
      });
    });

    // Form submission
    form.addEventListener("submit", function (e) {
      let isValid = true;

      inputs.forEach((input) => {
        if (!validateField(input)) {
          isValid = false;
        }
      });

      if (!isValid) {
        e.preventDefault();
      }
    });
  });

  function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute("required");
    let isValid = true;
    let errorMessage = "";

    clearFieldError(field);

    if (required && !value) {
      isValid = false;
      errorMessage = "This field is required";
    } else if (value) {
      if (type === "email") {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          isValid = false;
          errorMessage = "Please enter a valid email address";
        }
      } else if (type === "password" && value.length < 8) {
        isValid = false;
        errorMessage = "Password must be at least 8 characters";
      }
    }

    // Password confirmation
    if (field.name === "password2" || field.id === "id_password2") {
      const password1 = document.querySelector(
        'input[name="password1"], input[id="id_password1"]'
      );
      if (password1 && value !== password1.value) {
        isValid = false;
        errorMessage = "Passwords do not match";
      }
    }

    if (!isValid) {
      showFieldError(field, errorMessage);
    }

    return isValid;
  }

  function showFieldError(field, message) {
    field.style.borderColor = "#ef4444";

    let errorDiv = field.parentElement.querySelector(".field-error");
    if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.className = "field-error";
      errorDiv.style.cssText =
        "color: #ef4444; font-size: 0.875rem; margin-top: 0.25rem;";
      field.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
  }

  function clearFieldError(field) {
    field.style.borderColor = "";
    const errorDiv = field.parentElement.querySelector(".field-error");
    if (errorDiv) {
      errorDiv.remove();
    }
  }

  // ===================================
  // Auto-hide Messages
  // ===================================
  const messages = document.querySelectorAll(".message");
  messages.forEach((message) => {
    // Add close button
    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.className = "message-close";
    closeBtn.style.cssText =
      "background: none; border: none; color: inherit; font-size: 1.5rem; cursor: pointer; margin-left: auto; padding: 0 0.5rem;";
    closeBtn.onclick = () => {
      message.style.animation = "slideOut 0.5s ease-out";
      setTimeout(() => message.remove(), 500);
    };
    message.appendChild(closeBtn);

    // Auto-hide after 5 seconds
    setTimeout(() => {
      message.style.animation = "slideOut 0.5s ease-out";
      setTimeout(() => message.remove(), 500);
    }, 5000);
  });

  // ===================================
  // File Input Display Name
  // ===================================
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const fileName = this.files[0]?.name;
      if (fileName) {
        // Show filename next to input
        let fileNameDisplay =
          this.parentElement.querySelector(".file-name-display");
        if (!fileNameDisplay) {
          fileNameDisplay = document.createElement("div");
          fileNameDisplay.className = "file-name-display";
          fileNameDisplay.style.cssText =
            "margin-top: 0.5rem; font-size: 0.875rem; color: #10b981;";
          this.parentElement.appendChild(fileNameDisplay);
        }
        fileNameDisplay.textContent = "✓ " + fileName;
      }
    });
  });

  // ===================================
  // Image Preview for File Inputs
  // ===================================
  const imageInputs = document.querySelectorAll(
    'input[type="file"][accept*="image"]'
  );
  imageInputs.forEach((input) => {
    input.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.onload = function (event) {
          let preview = input.parentElement.querySelector(".image-preview");

          if (!preview) {
            preview = document.createElement("img");
            preview.className = "image-preview";
            preview.style.cssText =
              "max-width: 200px; max-height: 200px; margin-top: 1rem; border-radius: 8px; border: 2px solid #e5e7eb;";
            input.parentElement.appendChild(preview);
          }

          preview.src = event.target.result;
        };

        reader.readAsDataURL(file);
      }
    });
  });

  // ===================================
  // Password Visibility Toggle
  // ===================================
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach((input) => {
    const wrapper = document.createElement("div");
    wrapper.style.position = "relative";
    input.parentElement.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.innerHTML = "👁️";
    toggleBtn.style.cssText =
      "position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 1.2rem;";
    toggleBtn.setAttribute("aria-label", "Toggle password visibility");

    wrapper.appendChild(toggleBtn);

    toggleBtn.addEventListener("click", function () {
      if (input.type === "password") {
        input.type = "text";
        toggleBtn.innerHTML = "🙈";
      } else {
        input.type = "password";
        toggleBtn.innerHTML = "👁️";
      }
    });
  });

  // ===================================
  // Character Counter for Textareas
  // ===================================
  const textareas = document.querySelectorAll("textarea[maxlength]");
  textareas.forEach((textarea) => {
    const maxLength = textarea.getAttribute("maxlength");

    const counter = document.createElement("div");
    counter.className = "char-counter";
    counter.style.cssText =
      "text-align: right; font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;";
    textarea.parentElement.appendChild(counter);

    function updateCounter() {
      const count = textarea.value.length;
      counter.textContent = `${count} / ${maxLength}`;

      if (count > maxLength * 0.9) {
        counter.style.color = "#ef4444";
      } else {
        counter.style.color = "#6b7280";
      }
    }

    updateCounter();
    textarea.addEventListener("input", updateCounter);
  });

  // ===================================
  // Smooth Scroll
  // ===================================
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href !== "#") {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }
    });
  });

  // ===================================
  // Confirmation Dialogs
  // ===================================
  const deleteButtons = document.querySelectorAll(
    'a[href*="delete"], button[type="submit"][class*="danger"]'
  );
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      if (
        !confirm(
          "Are you sure you want to delete this? This action cannot be undone."
        )
      ) {
        e.preventDefault();
      }
    });
  });

  // ===================================
  // Back to Top Button
  // ===================================
  const backToTopBtn = document.createElement("button");
  backToTopBtn.className = "back-to-top";
  backToTopBtn.innerHTML = "↑";
  backToTopBtn.setAttribute("aria-label", "Back to top");
  backToTopBtn.style.cssText = `
        position: fixed;
        bottom: -50px;
        right: 20px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 999;
    `;

  document.body.appendChild(backToTopBtn);

  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      backToTopBtn.style.bottom = "20px";
    } else {
      backToTopBtn.style.bottom = "-50px";
    }
  });

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  // ===================================
  // Loading State for Submit Buttons
  // ===================================
  const submitButtons = document.querySelectorAll('button[type="submit"]');
  submitButtons.forEach((button) => {
    const form = button.closest("form");
    if (form) {
      form.addEventListener("submit", function () {
        button.disabled = true;
        button.classList.add("loading");
        const originalText = button.textContent;
        button.textContent = "Processing...";

        // Re-enable after 10 seconds as fallback
        setTimeout(() => {
          button.disabled = false;
          button.classList.remove("loading");
          button.textContent = originalText;
        }, 10000);
      });
    }
  });

  console.log("✅ CareerConnect JavaScript initialized successfully!");
});

// ===================================
// Add necessary animations
// ===================================
const style = document.createElement("style");
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
