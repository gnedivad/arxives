(function(window, document, undefined) {
  var ABSTRACT_CONDENSED_LENGTH = 175;
  var NUMBER_REGEX = /^\d+$/;

  var publicationsTemplate = document.getElementsByClassName('publications-template')[0];
  var renderPublications = _.template(publicationsTemplate.innerHTML);

  var mid = document.querySelector('mid');
  var results = document.getElementsByClassName('results')[0];
  var searchBox = document.querySelector('input[type="text"]');
  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
  var loading = document.getElementsByClassName('loading')[0];

  var oldQuery = null;
  var oldFilters = null;
  var noMorePages = false;
  var page = 1;

  /* Returns the active filters based on checked checkboxes */
  function getFilters() {
    var filters = {};

    SearchModel.FILTER_CATEGORIES.forEach(function(category) {
      var filterCheckboxes = document.querySelectorAll(
        '.' + category + ' input[type="checkbox"]');
      var values = [];

      // collect values from all checked checkboxes
      Array.prototype.forEach.call(filterCheckboxes, function(checkbox) {
        if (checkbox.checked) {
          var value = checkbox.value;
          if (NUMBER_REGEX.test(value)) {
            value = parseInt(value, 10);
          }

          values.push(value);
        }
      });

      if (values.length > 0) {
        filters[category] = values;
      }
    });
    return filters;
  }

  /* Searches based on the inputted query and filters. advancePage specifies
   * whether to advance to the next page of search results. If advancePage is
   * false, this function begins a new search with the latest user input. */
  function search(advancePage) {
    var query;
    var filters;

    if (advancePage) {
      query = oldQuery;
      filters = oldFilters;

      // can't advance if there aren't any more pages
      if (noMorePages) {
        return;
      }

      page += 1
    } else {
      query = searchBox.value;
      filters = getFilters();

      // don't update if results won't change
      if (query === oldQuery && _.isEqual(filters, oldFilters)) {
        return;
      }

      oldQuery = query;
      oldFilters = filters;
      page = 0;
      noMorePages = false;
    }

    if (!query && _.isEmpty(filters)) {
      // nothing is being searched for
      results.innerHTML = renderPublications({
        publications: [],
        appendResults: false,
        noSearch: true
      });
      return;
    }

    // perform search
    loading.classList.add('active');
    SearchModel.match(query, filters, page, function(publications) {
      loading.classList.remove('active');

      updateSearchResults(publications, advancePage);
      noMorePages = publications.length == 0;
    });
  }

  function updateSearchResults(publications, appendResults) {
    console.log(publications);
    // limit length of abstracts
    publications.forEach(function(publication) {
      if (publication.abstract.length > ABSTRACT_CONDENSED_LENGTH) {
        var i = ABSTRACT_CONDENSED_LENGTH;
        while (publication.abstract[i] !== " " && i > 0) {
          i -= 1;
        }
        publication.condensedAbstract = publication.abstract.substring(0, i);
      } else {
        publication.condensedAbstract = publication.abstract;
      }
    });

    var publicationsHTML = renderPublications({
      publications: publications,
      appendResults: appendResults,
      noSearch: false
    });

    if (appendResults) {
      results.innerHTML += publicationsHTML;
    } else {
      results.innerHTML = publicationsHTML;
    }

    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
  }

  /* Begins a new search with the latest user input. */
  function beginSearch() {
    search(false);
  }
  
  searchBox.addEventListener('keyup', _.debounce(beginSearch, 250));

  // infinite scroll: update search results when user scrolls to bottom
  window.addEventListener('scroll', _.debounce(function() {
    var scrollY = window.scrollY || document.body.scrollTop;

    if (window.innerHeight + scrollY >= mid.offsetHeight) {
      search(true);
    }
  }, 100));

  // expand/collapse elements that have a toggle button
  window.addEventListener('click', function(event) {
    // event delegation: find .toggle element that was clicked
    var target = event.target;
    while (target instanceof HTMLElement &&
        !target.classList.contains('toggle')) {
      target = target.parentNode;
    }

    if (!(target instanceof HTMLElement)) {
      return;
    }

    // target is a .toggle element
    var toggleButton = target;
    var publication = toggleButton.parentNode.parentNode.parentNode;

    // toggle .active class and change text
    if (publication.classList.contains('active')) {
      publication.classList.remove('active');
    } else {
      publication.classList.add('active');
    }
  });

  search(false);
})(this, this.document);
