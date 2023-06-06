from flask import Flask,  request, jsonify
from elasticsearch import Elasticsearch
import pandas as pd
import psycopg2

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
print(es.info().body)

df = pd.read_csv("simple_searcher\posts.csv")
print(df)
#if __name__ == '__main__':
#    app.run(debug=True)

