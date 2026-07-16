document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('lesson-search');
  const status = document.getElementById('lesson-search-status');

  if (!input || !status) {
    return;
  }

  const sections = Array.from(document.querySelectorAll('h2'));
  const lessonItems = Array.from(document.querySelectorAll('li'));

  const normalize = function (value) {
    return (value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[^\w\s]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  };

  const updateResults = function () {
    const query = normalize(input.value);
    let visibleCount = 0;

    sections.forEach(function (section) {
      const sectionHeading = section;
      let sectionHasVisibleItems = false;
      let nextElement = sectionHeading.nextElementSibling;

      while (nextElement && nextElement.tagName !== 'H2') {
        if (nextElement.tagName === 'LI') {
          const text = normalize(nextElement.textContent);
          const isVisible = !query || text.includes(query);
          nextElement.style.display = isVisible ? '' : 'none';
          if (isVisible) {
            sectionHasVisibleItems = true;
            visibleCount += 1;
          }
        }
        nextElement = nextElement.nextElementSibling;
      }

      sectionHeading.style.display = sectionHasVisibleItems || !query ? '' : 'none';
    });

    if (!query) {
      status.textContent = 'Showing all lessons.';
    } else if (visibleCount === 0) {
      status.textContent = 'No lessons matched your search.';
    } else {
      status.textContent = 'Showing ' + visibleCount + ' lesson' + (visibleCount === 1 ? '' : 's') + ' that match your search.';
    }
  };

  input.addEventListener('input', updateResults);
  updateResults();
});
