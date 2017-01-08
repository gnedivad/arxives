from elasticsearch import Elasticsearch


class Search():
  SUBJECTS_IDS = []

  ES_INDEX_NAME = "arxives"
  ES_TYPE_NAME = "publication"

  FILTERS = {
    "subjects_ids": SUBJECTS_IDS,
  }

  RESULTS_PER_PAGE = 10

  ES_CLIENT = Elasticsearch()

  # Extracts filters from the user-inputted search parameters. Returns a hash
  # of filters to be passed to match() below.
  @classmethod
  def extract_filters(cls, params):
    filters = {}

    for key, value in cls.FILTERS.iteritems():
      try:
        terms = params[key]
      except:
        continue
      else:
        # This will break
        terms = JSON.parse(params[key])
        filters[key] = filter(terms, lambda term: term in value)

    return filters
 
  # Returns an array of courses that match the given query and filters
  # page specifies which page of results to return (0-indexed)
  @classmethod
  def match(cls, query, filters, page):
    if not query:
      # we're just filtering so match all
      multi_match_query = {"match_all": {}}
    else:
      multi_match_query = {
        "multi_match": {
          "query": query,
          "fields": ["abstract", "author^1.5", "title^2"],
        }
      }
    
    if not filters:
      body = {"query": multi_match_query}
    else:
      body = {}

    start_page = page * cls.RESULTS_PER_PAGE
    results = cls.ES_CLIENT.search(
      index="arxives", body=body, from_=start_page)
    hits = results["hits"]["hits"]

    return hits
