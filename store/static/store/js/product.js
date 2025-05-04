document.addEventListener('DOMContentLoaded', function() {

    var formElements = document.querySelectorAll('form input[type="text"], form textarea');
    formElements.forEach(function(element) {
      element.classList.add('form-control');
    });
  });