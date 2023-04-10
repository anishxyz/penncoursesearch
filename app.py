import asyncio
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from queryengine import query_response, cache_embeddings, initialize_cache_sync

app = Flask(__name__, static_folder='frontend/build/', static_url_path='')
CORS(app)

initialize_cache_sync()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/search', methods=['POST', 'GET'])
async def search():
    search_term = request.args.get('q', '')
    print(search_term)

    results = await query_response(search_term)
    print(results)

    return jsonify(results)


if __name__ == '__main__':
    app.run()




