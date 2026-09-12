/* gallery.js — Laptop detail image gallery switcher */

document.addEventListener('DOMContentLoaded', () => {
  const mainImg = document.getElementById('main-gallery-img');
  const thumbs  = document.querySelectorAll('.gallery-thumb');

  if (!mainImg || thumbs.length === 0) return;

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      // Update main image with fade
      mainImg.style.opacity = '0';
      setTimeout(() => {
        mainImg.src = thumb.dataset.full || thumb.src;
        mainImg.style.opacity = '1';
      }, 150);

      // Update active thumb
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

  // Smooth opacity transition
  mainImg.style.transition = 'opacity .15s ease';
});
