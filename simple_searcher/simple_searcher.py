from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([''])
