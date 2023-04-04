import os

import queryengine
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from queryengine import query_response


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

df = queryengine.load_df()


@app.route('/')
@cross_origin()
def serve():
    print("here at route")
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/search', methods=['GET'])
@cross_origin()
async def search():
    search_term = request.args.get('q', '')
    # Implement your search logic here, using search_term
    # For example, you can filter a list of courses based on the search term:
    results = await query_response(search_term, df)
    print("got it!")
    return jsonify(results)


if __name__ == '__main__':
    app.run()

