(function(window, document, undefined) {
  var SearchModel = {};

  SearchModel.FILTER_CATEGORIES = ['subjects_ids'];

  /* Searches for publications that match the given query and filters. Calls
   * the given callback with an array of matching publications.
   *
   * Inputs:
   * - query: A string
   * - filters: An object with key "subjects_ids" and value array of strings
   *   that filter the key e.g. { subjects_ids: ["cs.IT", "math.DS"] } limits
   *   the subjects_ids to either Computer Science (Information Theory) or
   *   Mathematics (Dynamical Systems).
   * - page: An int that represents which page to return (0-indexed).
   */
  SearchModel.match = function(query, filters, page, callback) {
    // add query to querystring
    var qs = 'page=' + encodeURIComponent(page) + '&query=' +
      encodeURIComponent(query);

    // add each filter to querystring
    this.FILTER_CATEGORIES.forEach(function(category) {
      if (filters[category] && _.isArray(filters[category])) {
        qs += '&' + category + '=' +
          encodeURIComponent(JSON.stringify(filters[category]));
      }
    });

    // query for new results
    var request = new XMLHttpRequest();
    request.addEventListener('load', function() {
      if (request.status === 200) {
        var publications = JSON.parse(request.responseText);
        callback(publications);
      }
    });

    request.open('GET', '/search?' + qs, true);
    request.send();
  } 

  window.SearchModel = SearchModel;
})(this, this.document);
