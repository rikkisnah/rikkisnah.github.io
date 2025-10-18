// Force light theme as default
(function() {
  'use strict';
  
  // Override the theme detection and force light mode
  const forceLightTheme = () => {
    const html = document.documentElement;
    const body = document.body;
    
    // Remove dark class if present
    html.classList.remove('dark');
    
    // Force light theme styles
    html.style.setProperty('color-scheme', 'light');
    body.style.setProperty('background-color', '#ffffff');
    body.style.setProperty('color', '#1a202c');
    
    // Override localStorage to always use light theme
    localStorage.setItem('dark', 'false');
  };
  
  // Run immediately
  forceLightTheme();
  
  // Run after DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', forceLightTheme);
  }
  
  // Run after window is loaded
  window.addEventListener('load', forceLightTheme);
  
  // Override any theme toggle buttons
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-dark') || 
        e.target.closest('.btn-dark')) {
      e.preventDefault();
      e.stopPropagation();
      forceLightTheme();
      return false;
    }
  });
  
  // Monitor for any dark class additions and remove them
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'attributes' && 
          mutation.attributeName === 'class' && 
          mutation.target.classList.contains('dark')) {
        mutation.target.classList.remove('dark');
        forceLightTheme();
      }
    });
  });
  
  // Start observing
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  });
  
})();
