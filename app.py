import queryengine
from flask import Flask, request, jsonify
from flask_cors import CORS
from queryengine import query_response


app = Flask(__name__)
CORS(app)

# df = queryengine.load_df()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/search', methods=['GET'])
async def search():
    search_term = request.args.get('q', '')
    # Implement your search logic here, using search_term
    # For example, you can filter a list of courses based on the search term:
    results = await query_response(search_term, df)
    print("got it!")
    return jsonify(results)


if __name__ == '__main__':
    app.run()
