import asyncio
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from queryengine import query_response, initialize_cache_sync, create_context_parquet

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


@app.route('/searchfast', methods=['POST', 'GET'])
async def searchfast():
    search_term = request.args.get('q', '')
    print(search_term)

    results = await create_context_parquet(search_term)
    # print(results)

    return jsonify(results)


@app.route('/search', methods=['POST', 'GET'])
async def search():
    if request.method == 'POST':
        data = request.get_json()
        search_term = data.get('q', '')
        context = data.get('context', '')
    else:
        search_term = request.args.get('q', '')
        context = request.args.get('context', '')
    # print(search_term)

    results = await query_response(search_term, context=context)
    # print(results)

    return jsonify(results)


if __name__ == '__main__':
    app.run()




