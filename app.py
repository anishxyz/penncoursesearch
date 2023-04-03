import os

import queryengine
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from queryengine import query_response


app = Flask(__name__)
CORS(app)

# df = queryengine.load_df()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



@app.route('/search', methods=['GET'])
async def search():
    search_term = request.args.get('q', '')
    # Implement your search logic here, using search_term
    # For example, you can filter a list of courses based on the search term:
    # results = await query_response(search_term, df)
    print("got it!")
    return jsonify("hello")


if __name__ == '__main__':
    app.run()

