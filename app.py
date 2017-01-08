from flask import Flask, jsonify, render_template, request

from search import Search

app = Flask(__name__, static_folder="public")
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
  return render_template("index.html", subjects_ids=Search.SUBJECTS_IDS)

@app.route("/search")
def search():
  params = request.args
  filters = Search.extract_filters(params)
  page = int(params.get("page")) if params.get("page") else 0
  results = Search.match(params.get("query"), filters, page)
  publications = map(lambda r: r["_source"], results)
  
  for publication in publications:
    publication["arxiv_url"] = "https://arxiv.org/abs/" + publication["arxiv_id"]

  return jsonify(publications)
