from flask import Flask, request, jsonify, render_template
from helper import MilvusHelper, PARAGRAPH_SCHEMA, COLLECTION_NAME
import json

app = Flask(__name__)
db = MilvusHelper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_data():
    query = request.args.get('query')
    top_k = int(request.args.get('top_k', 10))
    results = db.search(COLLECTION_NAME, query, top_k)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=6969)
