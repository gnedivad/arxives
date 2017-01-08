#!/usr/bin/env python
import json
import os

from elasticsearch import Elasticsearch


def main():
  client = Elasticsearch()

  # configures index for searching
  indices = client.indices
  if indices.exists(index="arxives"):
    indices.delete(index="arxives") 
  
  indices.create(
    index="arxives",
    body={
      "settings": {
        "number_of_shards": 1,
        "analysis": {
          "filter": {
            "autocomplete_filter": {
              "type": "edge_ngram",
              "min_gram": 1,
              "max_gram": 20,
            }
          },
          "analyzer": {
            "autocomplete": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "autocomplete_filter"
              ]
            }
          }
        }
      },
      "mappings": {
        "publication": {
          "properties": {
            "abstract": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "standard",
            },
            "arxiv_id": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "standard",
            },
            "authors": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "standard",
            },
            "pdf_url": {
              "type": "keyword",
              "index": "not_analyzed",
            },
            "subjects_ids": {
              "type": "keyword",
              "index": "not_analyzed",
            },
            "submission_date": {
              "type": "date",
              "index": "not_analyzed",
            },
            "title": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "standard",
            },
          }
        }
      }
    })

  publications = []
  for filename in os.listdir("out"):
    with open("out/" + filename) as f:
      data = json.load(f)
    publications.extend(data) 

  for i, publication in enumerate(publications):
    try:
      data = client.index(
        index="arxives", doc_type="publication", body=publication)
      # do something with `data`?
    except Exception as e:
      # hops into the debugger; should not happen
      import pdb; pdb.set_trace()

if __name__ == "__main__":
  main()
