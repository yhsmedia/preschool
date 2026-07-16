document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('lesson-search');
  const status = document.getElementById('lesson-search-status');
  const resultsContainer = document.getElementById('lesson-search-results');

  if (!input || !status || !resultsContainer) {
    return;
  }

  const normalize = function (value) {
    return (value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[^\w\s]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  };

  const fetchIndex = function () {
    return fetch('lessons-search-index.json').then(function (response) {
      if (!response.ok) {
        throw new Error('Unable to load lesson search index');
      }
      return response.json();
    });
  };

  const getSnippet = function (lesson, query) {
    const searchableFields = [
      lesson.title,
      lesson.quarter,
      lesson.season,
      lesson.description,
      lesson.theme,
      lesson.memory_verse,
      lesson.page,
      lesson.content,
    ];

    const matchedField = searchableFields.find(function (field) {
      return field && normalize(field).includes(query);
    });

    if (!matchedField) {
      return '';
    }

    const text = matchedField.replace(/\s+/g, ' ').trim();
    const start = Math.max(0, text.toLowerCase().indexOf(query));
    const end = Math.min(text.length, start + 140);
    const snippetStart = start > 40 ? start - 40 : 0;
    const snippetEnd = end < text.length ? end + 40 : text.length;
    let snippet = text.slice(snippetStart, snippetEnd).trim();

    if (snippetStart > 0) {
      snippet = '…' + snippet;
    }
    if (snippetEnd < text.length) {
      snippet = snippet + '…';
    }

    return snippet;
  };

  const renderResults = function (lessons, query) {
    const list = document.createElement('ul');
    list.style.listStyle = 'none';
    list.style.padding = '0';
    list.style.margin = '0';

    lessons.forEach(function (lesson) {
      const item = document.createElement('li');
      item.style.marginBottom = '0.75rem';
      item.style.padding = '0.75rem 0';
      item.style.borderBottom = '1px solid #eee';

      const title = document.createElement('a');
      title.href = lesson.path.replace(/\.md$/, '.html');
      title.textContent = lesson.title;
      title.style.fontWeight = '600';
      item.appendChild(title);

      const meta = document.createElement('div');
      meta.style.color = '#555';
      meta.style.fontSize = '0.95rem';
      meta.style.marginTop = '0.2rem';
      meta.textContent = [lesson.quarter, lesson.season, lesson.week ? 'Week ' + lesson.week : ''].filter(Boolean).join(' • ');
      item.appendChild(meta);

      const snippet = getSnippet(lesson, query);
      if (snippet) {
        const excerpt = document.createElement('div');
        excerpt.style.marginTop = '0.25rem';
        excerpt.style.color = '#444';
        excerpt.style.fontSize = '0.95rem';
        excerpt.textContent = snippet;
        item.appendChild(excerpt);
      } else if (lesson.description) {
        const desc = document.createElement('div');
        desc.style.marginTop = '0.25rem';
        desc.style.color = '#444';
        desc.textContent = lesson.description;
        item.appendChild(desc);
      }

      list.appendChild(item);
    });

    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(list);

    if (!query) {
      status.textContent = 'Showing all lessons.';
    } else if (lessons.length === 0) {
      status.textContent = 'No lessons matched your search.';
    } else {
      status.textContent = 'Showing ' + lessons.length + ' lesson' + (lessons.length === 1 ? '' : 's') + ' that match your search.';
    }
  };

  const updateResults = function () {
    const query = normalize(input.value);

    fetchIndex().then(function (records) {
      const filtered = records.filter(function (lesson) {
        const searchableText = [
          lesson.title,
          lesson.quarter,
          lesson.season,
          lesson.description,
          lesson.theme,
          lesson.memory_verse,
          lesson.page,
          lesson.content,
        ].join(' ');

        return !query || normalize(searchableText).includes(query);
      });

      renderResults(filtered, query);
    }).catch(function () {
      status.textContent = 'Search is unavailable right now.';
    });
  };

  input.addEventListener('input', updateResults);
  updateResults();
});
