import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from queryengine import query_response


app = Flask(__name__, static_folder='frontend/build/', static_url_path='')
CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("here at route")
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/search', methods=['POST', 'GET'])
async def search():
    print("search gotten")
    search_term = request.args.get('q', '')
    print(search_term)
    # Implement your search logic here, using search_term
    # For example, you can filter a list of courses based on the search term:
    results = await query_response(search_term)
    print("got it!")
    print(results)
    return jsonify(results)


if __name__ == '__main__':
    app.run()



