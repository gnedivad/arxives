# arXivES
This directory contains the production version of `arXivES`, which searches `arXiv` with Elasticsearch. As of Jan 10, 2017, I have indexed publications from Jan to Mar 2015 in production.

This README will explain how to get `arXivES` running on your local machine.

## Installing Dependencies

Install [Elasticsearch](http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/_installation.html) and start it.

Install Python 2.7. I use [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) but vanilla [virtualenv](https://pypi.python.org/pypi/virtualenv) works as well.

In the virtual environment (called `arxivesenv` here), install the project dependencies:

```bash
(arxivesenv) $ cd arxives/; pip install -r requirements.txt
```

## Seeding Publications

The publications need to be indexed in Elasticsearch in order for search to work. I've compressed ~25k publications from Jan to Mar 2015 in `arxives.tar.gz`. You can extract the data from this file to get started immediately:

```bash
(arxivesenv) $ cd bin/; tar -xvzf arxives.tar.gz
```

Or you can generate the data (and more months) yourself:

```bash
(arxivesenv) $ cd bin/; ./fetch_publications.py
```

Then, index the data in Elasticsearch:

```bash
(arxivesenv) $ ./bin/index_publications.py
```

## Running arXivES
You're ready to run the Flask app!

```bash
(arxivesenv) $ python run.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser!
