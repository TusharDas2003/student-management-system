// Smooth animations on page load
document.addEventListener('DOMContentLoaded', function() {
  // Animate stats cards on home page
  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.6s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });

  // Animate table rows
  const tableRows = document.querySelectorAll('tbody tr');
  tableRows.forEach((row, index) => {
    row.style.opacity = '0';
    setTimeout(() => {
      row.style.transition = 'opacity 0.3s ease';
      row.style.opacity = '1';
    }, index * 50);
  });

  // Add active state to nav links
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar .nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath || currentPath.startsWith(link.getAttribute('href'))) {
      link.classList.add('active');
    }
  });

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bootstrapAlert = new bootstrap.Alert(alert);
      bootstrapAlert.close();
    }, 5000);
  });
});

// Toast notification utility
function showToast(message, type = 'info') {
  const alertHTML = `
    <div class="alert alert-${type} alert-dismissible fade show shadow-sm border-0" role="alert">
      <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;
  
  const alertContainer = document.querySelector('main');
  if (alertContainer) {
    const wrapper = document.createElement('div');
    wrapper.className = 'container mt-3';
    wrapper.innerHTML = alertHTML;
    alertContainer.insertBefore(wrapper, alertContainer.firstChild);
  }
}

// Form validation
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', function(e) {
    if (!form.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    form.classList.add('was-validated');
  }, false);
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
  // Ctrl/Cmd + K to focus search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault();
    const searchInput = document.querySelector('input[placeholder*="Search"]');
    if (searchInput) {
      searchInput.focus();
    }
  }
});

// Lazy load images
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('loaded');
        imageObserver.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}

// Disable form submissions if there are no changes
document.querySelectorAll('form').forEach(form => {
  const inputs = form.querySelectorAll('input, textarea, select');
  const initialValues = {};
  
  inputs.forEach(input => {
    initialValues[input.name] = input.value;
  });

  form.addEventListener('submit', function(e) {
    let hasChanges = false;
    inputs.forEach(input => {
      if (input.value !== initialValues[input.name]) {
        hasChanges = true;
      }
    });

    if (!hasChanges && !form.classList.contains('allow-empty-submit')) {
      // Form already filled or not changed
    }
  });
});

// Mobile menu close on link click
document.querySelectorAll('.navbar-collapse .nav-link').forEach(link => {
  link.addEventListener('click', function() {
    const navbarToggle = document.querySelector('.navbar-toggler');
    if (navbarToggle && !navbarToggle.classList.contains('collapsed')) {
      navbarToggle.click();
    }
  });
});

// Scroll to top button
window.addEventListener('scroll', function() {
  if (window.pageYOffset > 100) {
    // Show scroll-to-top button if exists
    const scrollBtn = document.getElementById('scrollToTop');
    if (scrollBtn) scrollBtn.style.display = 'block';
  } else {
    const scrollBtn = document.getElementById('scrollToTop');
    if (scrollBtn) scrollBtn.style.display = 'none';
  }
});

// Add loading state to form submissions
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', function() {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
    }
  });
});

// Accessibility: Ensure focus management
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.activeElement.blur();
  }
});
