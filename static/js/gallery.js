/* gallery.js — Facebook-Style Lightbox Gallery */

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('lightbox-modal');
  if (!modal) return;

  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');
  
  const collageItems = document.querySelectorAll('.collage-item');
  let currentIndex = 0;
  
  // Images array is loaded from detail.html via window.galleryImages
  const images = window.galleryImages || [];

  function openLightbox(index) {
    if (images.length === 0) return;
    currentIndex = index;
    updateLightbox();
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  }

  function closeLightbox() {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }

  function updateLightbox() {
    const imgData = images[currentIndex];
    modalImg.src = imgData.url;
    modalCaption.textContent = imgData.caption || `Image ${currentIndex + 1} of ${images.length}`;
  }

  function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    updateLightbox();
  }

  function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateLightbox();
  }

  // Event Listeners for Collage Grid
  collageItems.forEach(item => {
    item.addEventListener('click', function() {
      const index = parseInt(this.getAttribute('data-index'));
      openLightbox(index);
    });
  });

  // Modal Controls
  closeBtn.addEventListener('click', closeLightbox);
  nextBtn.addEventListener('click', (e) => { e.stopPropagation(); nextImage(); });
  prevBtn.addEventListener('click', (e) => { e.stopPropagation(); prevImage(); });
  
  // Close when clicking outside the image
  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target.classList.contains('lightbox-content-wrapper')) {
      closeLightbox();
    }
  });

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (modal.style.display === 'block') {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextImage();
      if (e.key === 'ArrowLeft') prevImage();
    }
  });
});
