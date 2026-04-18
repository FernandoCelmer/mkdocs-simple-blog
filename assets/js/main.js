document.addEventListener('click', (event) => {
  const collapseTrigger = event.target.closest('[data-bs-toggle="collapse"]');
  if (collapseTrigger) {
    const selector = collapseTrigger.getAttribute('data-bs-target');
    const target = selector && document.querySelector(selector);
    if (target) {
      target.classList.toggle('show');
      collapseTrigger.setAttribute(
        'aria-expanded',
        target.classList.contains('show')
      );
      event.preventDefault();
      return;
    }
  }

  const dropdownTrigger = event.target.closest('[data-bs-toggle="dropdown"]');
  if (dropdownTrigger) {
    const parent = dropdownTrigger.parentElement;
    const menu = parent && parent.querySelector('.menu__dropdown');
    if (menu) {
      document.querySelectorAll('.menu__dropdown.show').forEach((other) => {
        if (other !== menu && !menu.contains(other) && !other.contains(menu)) {
          other.classList.remove('show');
        }
      });
      menu.classList.toggle('show');
      event.preventDefault();
    }
    return;
  }

  if (!event.target.closest('.menu__dropdown') && !event.target.closest('.menu__item')) {
    document
      .querySelectorAll('.menu__dropdown.show')
      .forEach((menu) => menu.classList.remove('show'));
  }
});
