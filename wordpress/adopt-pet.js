(() => {
  const initialize = () => {
    document.querySelectorAll('.nap-wp').forEach((section) => {
      if (section.dataset.napInitialized === 'true') return;
      section.dataset.napInitialized = 'true';

      const gallery = section.querySelector('[data-nap-gallery]');
      const slides = [...gallery.querySelectorAll('.nap-wp__slide')];
      const previous = section.querySelector('[data-nap-prev]');
      const next = section.querySelector('[data-nap-next]');
      const count = section.querySelector('[data-nap-count]');
      let updateFrame;

      const currentIndex = () => {
        if (gallery.scrollLeft >= gallery.scrollWidth - gallery.clientWidth - 2) {
          return slides.length - 1;
        }
        const galleryLeft = gallery.getBoundingClientRect().left;
        let closestIndex = 0;
        let closestDistance = Infinity;
        slides.forEach((slide, index) => {
          const distance = Math.abs(slide.getBoundingClientRect().left - galleryLeft);
          if (distance < closestDistance) {
            closestDistance = distance;
            closestIndex = index;
          }
        });
        return closestIndex;
      };

      const update = () => {
        const index = currentIndex();
        count.textContent = `${index + 1} / ${slides.length}`;
        previous.disabled = index === 0;
        next.disabled = index === slides.length - 1;
      };

      const goTo = (index) => {
        const target = slides[Math.max(0, Math.min(index, slides.length - 1))];
        gallery.scrollTo({
          left: target.offsetLeft - slides[0].offsetLeft,
          behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
        });
      };

      previous.addEventListener('click', () => goTo(currentIndex() - 1));
      next.addEventListener('click', () => goTo(currentIndex() + 1));
      gallery.addEventListener('scroll', () => {
        cancelAnimationFrame(updateFrame);
        updateFrame = requestAnimationFrame(update);
      }, { passive: true });
      window.addEventListener('resize', update);
      update();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();
