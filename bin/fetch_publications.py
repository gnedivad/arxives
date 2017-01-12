#!/usr/bin/env python
"""
This script fetches publications from arxiv.org and writes them to a directory
called `out/`.
"""
import json
import os
import re
import sys
import time
import urllib2
from bs4 import BeautifulSoup


MONTHS_TO_NUMBERS = {
  "Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5", "Jun": "6",
  "Jul": "7", "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12",
}

def get_arxiv_id_from_soup(soup):
  raw_text = soup.find(class_="arxivid").get_text()
  extracted_text = re.match("arXiv:(.+) (?:.+)", raw_text).group(1)
  return extracted_text

def get_title_from_soup(soup):
  raw_text = soup.find(class_="title").get_text()
  extracted_text = re.match("Title:\n(.+)", raw_text).group(1)
  return extracted_text

def get_authors_from_soup(soup):
  a_tags = soup.find(class_="authors").find_all("a")
  return map(lambda a_tag: a_tag.get_text(), a_tags)

def get_submission_date_from_soup(soup):
  raw_text = soup.find(class_="dateline").get_text()
  extracted_text = re.match("\(Submitted on (.+?)(?: \(.+\))?\)", raw_text).group(1)

  l = extracted_text.split(" ")  # e.g. ['29', 'Dec', '2014']
  l[0] = l[0].zfill(2)
  l[1] = MONTHS_TO_NUMBERS[l[1]].zfill(2)  # e.g. ['29', '12', '2014']

  cleaned_text = "-".join(l[::-1])  # e.g. '2014-12-29'
  return cleaned_text

def get_abstract_from_soup(soup):
  raw_text = soup.find(class_="abstract").get_text()
  extracted_text = re.match(
    "Abstract: (.+)", raw_text.replace("\n", " ").strip()).group(1)
  return extracted_text

def get_subjects_ids_from_soup(soup):
  raw_text = soup.find(class_="subjects").get_text()
  subjects = raw_text.split(";")
  subjects_ids = map(
    lambda s: re.match("(?:.+) \((.+)\)", s).group(1),
    subjects)
  return subjects_ids

def get_pdf_url_from_soup(soup):
  a_tag = soup.find(class_="full-text").find("a")
  pdf_url = "https://arxiv.org" + a_tag['href']
  return pdf_url

def main():
  if len(sys.argv) < 2:
    print("Usage: ./fetch_publications.py <Month> <Year>")
    print("- Month: The first three letters of the month to be fetched")
    print("  e.g. 'Jan', 'Feb', etc.")
    print("- Year: The full year to be fetched e.g. '2016'")
    print("There's no explicit error checking, so plz follow directions.")
    return

  month_str = MONTHS_TO_NUMBERS[sys.argv[1]].zfill(2)
  year_str = sys.argv[2][-2:]

  read_files = set([])

  i = 1
  batch_size = 1000

  if not os.path.exists("out"):
    os.makedirs("out")

  while True:
    try:
      html = urllib2.urlopen(
        "https://arxiv.org/abs/%s%s.%05d" % (year_str, month_str, i)
      ).read()
    except urllib2.HTTPError as error:
      print "Stopped short of %s%s.%05d" % (year_str, month_str, i)
      return
    soup = BeautifulSoup(html, "html.parser")

    # Reads from file if it exists the first time the filename appears; else
    # appends to the existing value of data
    filename = "out/%s%s_%03d.json" % (year_str, month_str, i / batch_size)
    if filename not in read_files:
      read_files.add(filename)
      try:
        with open(filename) as f:
          data = json.load(f)
      except:
        data = []

    arxiv_id = get_arxiv_id_from_soup(soup)
    title = get_title_from_soup(soup)  
    authors = get_authors_from_soup(soup)
    submission_date = get_submission_date_from_soup(soup)
    abstract = get_abstract_from_soup(soup)
    subjects_ids = get_subjects_ids_from_soup(soup)
    pdf_url = get_pdf_url_from_soup(soup)

    data.append({
      "arxiv_id": arxiv_id,
      "title": title,
      "authors": authors,
      "submission_date": submission_date,
      "abstract": abstract,
      "subjects_ids": subjects_ids,
      "pdf_url": pdf_url,
    })

    with open(filename, "w") as f:
      json.dump(data, f, indent=2, separators=(",", ": "))

    time.sleep(0.1)
    if i % 10 == 0:
      print "Finished %s%s.%05d" % (year_str, month_str, i)
    i += 1

if __name__ == "__main__":
  main()
