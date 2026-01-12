// ===================================
// CareerConnect - Main JavaScript
// Interactive Features & Functionality
// ===================================

document.addEventListener("DOMContentLoaded", function () {
  // ===================================
  // Mobile Navigation Toggle
  // ===================================
  const createMobileMenu = () => {
    const navbar = document.querySelector(".navbar");
    const navMenu = document.querySelector(".nav-menu");

    if (!navbar || !navMenu) return;

    // Create hamburger button
    const hamburger = document.createElement("button");
    hamburger.className = "mobile-menu-toggle";
    hamburger.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
    hamburger.setAttribute("aria-label", "Toggle navigation menu");

    // Insert hamburger before nav menu
    navbar.insertBefore(hamburger, navMenu);

    // Toggle menu on click
    hamburger.addEventListener("click", () => {
      navMenu.classList.toggle("active");
      hamburger.classList.toggle("active");
      document.body.classList.toggle("menu-open");
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
      if (!navbar.contains(e.target)) {
        navMenu.classList.remove("active");
        hamburger.classList.remove("active");
        document.body.classList.remove("menu-open");
      }
    });
  };

  // Only create mobile menu on small screens
  if (window.innerWidth <= 768) {
    createMobileMenu();
  }

  window.addEventListener("resize", () => {
    if (window.innerWidth <= 768) {
      if (!document.querySelector(".mobile-menu-toggle")) {
        createMobileMenu();
      }
    }
  });

  // ===================================
  // Form Validation & Enhancement
  // ===================================
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    const inputs = form.querySelectorAll("input, textarea, select");

    inputs.forEach((input) => {
      // Add focus animation
      input.addEventListener("focus", function () {
        this.parentElement.classList.add("focused");
      });

      input.addEventListener("blur", function () {
        this.parentElement.classList.remove("focused");
        if (this.value) {
          this.parentElement.classList.add("filled");
        } else {
          this.parentElement.classList.remove("filled");
        }
      });

      // Real-time validation
      input.addEventListener("input", function () {
        validateField(this);
      });
    });

    // Form submission validation
    form.addEventListener("submit", function (e) {
      let isValid = true;

      inputs.forEach((input) => {
        if (!validateField(input)) {
          isValid = false;
        }
      });

      if (!isValid) {
        e.preventDefault();
        showNotification("Please fix the errors in the form", "error");
      }
    });
  });

  // Field validation function
  function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute("required");
    let isValid = true;
    let errorMessage = "";

    // Remove previous error
    removeFieldError(field);

    if (required && !value) {
      isValid = false;
      errorMessage = "This field is required";
    } else if (value) {
      switch (type) {
        case "email":
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = "Please enter a valid email address";
          }
          break;

        case "password":
          if (value.length < 8) {
            isValid = false;
            errorMessage = "Password must be at least 8 characters";
          }
          break;

        case "tel":
          const phoneRegex = /^[\d\s\-\+\(\)]+$/;
          if (!phoneRegex.test(value)) {
            isValid = false;
            errorMessage = "Please enter a valid phone number";
          }
          break;

        case "url":
          try {
            new URL(value);
          } catch {
            isValid = false;
            errorMessage = "Please enter a valid URL";
          }
          break;
      }
    }

    // Check password confirmation
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
    field.classList.add("error");

    // Check if error message already exists
    let errorDiv = field.parentElement.querySelector(".field-error");
    if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.className = "field-error";
      field.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
  }

  function removeFieldError(field) {
    field.classList.remove("error");
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
    setTimeout(() => {
      message.style.animation = "slideOut 0.5s ease-out";
      setTimeout(() => {
        message.remove();
      }, 500);
    }, 5000);

    // Add close button
    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.className = "message-close";
    closeBtn.onclick = () => {
      message.style.animation = "slideOut 0.5s ease-out";
      setTimeout(() => message.remove(), 500);
    };
    message.appendChild(closeBtn);
  });

  // ===================================
  // File Input Enhancement
  // ===================================
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    const label = document.createElement("label");
    label.className = "file-input-label";
    label.innerHTML = `
            <span class="file-icon">📎</span>
            <span class="file-text">Choose file</span>
            <span class="file-name"></span>
        `;

    input.parentElement.insertBefore(label, input.nextSibling);

    input.addEventListener("change", function () {
      const fileName = this.files[0]?.name || "No file chosen";
      label.querySelector(".file-name").textContent = fileName;
      label.classList.add("has-file");
    });
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
  // Search Form Enhancement
  // ===================================
  const searchForm = document.querySelector(".search-form");
  if (searchForm) {
    const inputs = searchForm.querySelectorAll("input, select");

    inputs.forEach((input) => {
      input.addEventListener(
        "input",
        debounce(() => {
          // You can add auto-search functionality here if needed
        }, 300)
      );
    });
  }

  // ===================================
  // Job Cards Animation on Scroll
  // ===================================
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "0";
        entry.target.style.transform = "translateY(20px)";

        setTimeout(() => {
          entry.target.style.transition = "all 0.6s ease-out";
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }, 100);

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe job cards and other cards
  const cards = document.querySelectorAll(".job-card, .card");
  cards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 0.1}s`;
    observer.observe(card);
  });

  // ===================================
  // Table Responsive Enhancement
  // ===================================
  const tables = document.querySelectorAll("table");
  tables.forEach((table) => {
    if (!table.parentElement.classList.contains("table")) {
      const wrapper = document.createElement("div");
      wrapper.className = "table-responsive";
      table.parentElement.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
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
  // Character Counter for Textareas
  // ===================================
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach((textarea) => {
    const maxLength = textarea.getAttribute("maxlength");
    if (maxLength) {
      const counter = document.createElement("div");
      counter.className = "char-counter";
      counter.textContent = `0 / ${maxLength}`;
      textarea.parentElement.appendChild(counter);

      textarea.addEventListener("input", function () {
        const count = this.value.length;
        counter.textContent = `${count} / ${maxLength}`;

        if (count > maxLength * 0.9) {
          counter.style.color = "var(--danger-color)";
        } else {
          counter.style.color = "var(--gray-color)";
        }
      });
    }
  });

  // ===================================
  // Dynamic Search/Filter
  // ===================================
  const filterForm = document.querySelector(".filters form");
  if (filterForm) {
    const filterInputs = filterForm.querySelectorAll("input, select");

    filterInputs.forEach((input) => {
      input.addEventListener(
        "change",
        debounce(() => {
          // Auto-submit form on filter change
          // Uncomment if you want auto-filtering:
          // filterForm.submit();
        }, 500)
      );
    });
  }

  // ===================================
  // Notification System
  // ===================================
  window.showNotification = function (message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `message message-${type}`;
    notification.textContent = message;

    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "×";
    closeBtn.className = "message-close";
    closeBtn.onclick = () => notification.remove();
    notification.appendChild(closeBtn);

    const container = document.querySelector(".container");
    if (container) {
      container.insertBefore(notification, container.firstChild);

      setTimeout(() => {
        notification.style.animation = "slideOut 0.5s ease-out";
        setTimeout(() => notification.remove(), 500);
      }, 5000);
    }
  };

  // ===================================
  // Password Visibility Toggle
  // ===================================
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach((input) => {
    const wrapper = document.createElement("div");
    wrapper.className = "password-wrapper";
    input.parentElement.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "password-toggle";
    toggleBtn.innerHTML = "👁️";
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
  // Loading State for Forms
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

  // ===================================
  // Utility Functions
  // ===================================
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

  // ===================================
  // Back to Top Button
  // ===================================
  const createBackToTop = () => {
    const button = document.createElement("button");
    button.className = "back-to-top";
    button.innerHTML = "↑";
    button.setAttribute("aria-label", "Back to top");
    document.body.appendChild(button);

    window.addEventListener("scroll", () => {
      if (window.pageYOffset > 300) {
        button.classList.add("visible");
      } else {
        button.classList.remove("visible");
      }
    });

    button.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  };

  createBackToTop();

  // ===================================
  // Print Functionality
  // ===================================
  window.printPage = function () {
    window.print();
  };

  // ===================================
  // Copy to Clipboard
  // ===================================
  window.copyToClipboard = function (text) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        showNotification("Copied to clipboard!", "success");
      })
      .catch(() => {
        showNotification("Failed to copy", "error");
      });
  };

  // ===================================
  // Initialize Tooltips (if needed)
  // ===================================
  const tooltipElements = document.querySelectorAll("[data-tooltip]");
  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", function () {
      const tooltip = document.createElement("div");
      tooltip.className = "tooltip";
      tooltip.textContent = this.getAttribute("data-tooltip");
      document.body.appendChild(tooltip);

      const rect = this.getBoundingClientRect();
      tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
      tooltip.style.left = `${
        rect.left + rect.width / 2 - tooltip.offsetWidth / 2
      }px`;

      this._tooltip = tooltip;
    });

    element.addEventListener("mouseleave", function () {
      if (this._tooltip) {
        this._tooltip.remove();
        this._tooltip = null;
      }
    });
  });

  console.log("✅ CareerConnect JavaScript initialized successfully!");
});


