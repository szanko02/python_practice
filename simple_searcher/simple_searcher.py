import csv
from flask import Flask, jsonify, request, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

index_name = "my_index"
index_config = {
    "mappings": {
        "properties": {
            "iD": {"type": "keyword"},
            "text": {"type": "text"},
            "rubrics": {"type": "keyword"},
            "created_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"}
        }
    }
}

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index {index_name} deleted")
else:
    print(f"Index {index_name} does not exist")

@app.route("/index_data", methods=["POST"])
def index_data():
    with open('./posts.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            es.index(index=index_name, document=row)
    return jsonify({"message": "Data indexed successfully"})

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = search_documents(query)
    else:
        results = []
    return render_template("search.html", results=results)

def search_documents(query):
    search_query = {
        "query": {
            "match": {
                "text": query
            }
        },
        "sort": {
            "created_date": "desc"
        },
        "size": 20
    }
    results = es.search(index=index_name, body=search_query["query"], sort=search_query["sort"], size=search_query["size"])
    hits = results["hits"]["hits"]
    return hits


@app.route("/delete/<doc_id>")
def delete_docs_handler():
    pass

if __name__ == "__main__":
    es.indices.create(index=index_name, body=index_config)
    app.run()

#print(es.info().body)

#es.indices.create(index='documents', ignore=400)
"""
with open('posts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        
        es.index(index='documents', id=row['id'], body={
            'id': row['id'],
            'text': row['text'],
            'rubrics': row['rubrics'].split(','),
            'created_date': row['created_date']
        })
"""