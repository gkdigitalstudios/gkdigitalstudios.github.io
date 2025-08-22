// Simple form handler
function submitForm(event) {
  event.preventDefault();
  alert("Thank you for contacting GK Digital Studios! We'll get back to you soon.");
  return false;
}

// Smooth scrolling for nav links
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    target.scrollIntoView({ behavior: 'smooth' });
  });
});
