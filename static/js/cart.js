/* cart.js — Cart quantity controls & auto-submit */

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss flash messages after 5s
  document.querySelectorAll('.alert').forEach(alert => {
    const close = alert.querySelector('.alert-close');
    if (close) close.addEventListener('click', () => alert.remove());
    setTimeout(() => alert.remove(), 5000);
  });

  // Quantity +/- buttons in cart
  document.querySelectorAll('.qty-control').forEach(control => {
    const input   = control.querySelector('.qty-input');
    const minusBtn= control.querySelector('[data-action="minus"]');
    const plusBtn = control.querySelector('[data-action="plus"]');
    const form    = control.closest('form');

    if (minusBtn) {
      minusBtn.addEventListener('click', () => {
        const val = parseInt(input.value) - 1;
        input.value = val < 1 ? 1 : val;
        if (form) form.submit();
      });
    }
    if (plusBtn) {
      plusBtn.addEventListener('click', () => {
        const max = parseInt(input.dataset.max || 99);
        const val = parseInt(input.value) + 1;
        input.value = val > max ? max : val;
        if (form) form.submit();
      });
    }
  });
});
