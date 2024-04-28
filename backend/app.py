import asyncio
import os
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS, cross_origin
from queryengine import courses,courses_embeddings,query_response, create_context,reset_embeddings
app = Flask(__name__, static_folder='frontend/build/', static_url_path='')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

#Resets & loads course embeddings into memory; password protected
@app.route('/reset',methods = ['POST'])
async def reset():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password','')
    if (username != os.environ["PCS_USERNAME"] or password != os.environ["PCS_PASSWORD"]):
        return{"error":"invalid credentials"}
    await reset_embeddings()
    return {"message":"reset successful"}


#Gets k nearest context or matches exact course is provided
@app.route('/searchfast', methods=['POST', 'GET'])
async def searchfast():
    if request.method == 'POST':
        data = request.get_json()
        search_term = data.get('q', '')
    else:
        search_term = request.args.get('q', '')
    results = await create_context(search_term,10)
    return jsonify(results)


#Gets chatgpt to summarize results
@app.route('/search', methods=['POST', 'GET'])
async def search():
    if request.method == 'POST':
        data = request.get_json()
        search_term = data.get('q', '')
        context = data.get('context', '')
    else:
        search_term = request.args.get('q', '')
        context = request.args.get('context', '')
    results = await query_response(search_term, context=context)
    return jsonify(results)


if __name__ == '__main__':
    #initialize courses & courses_embeddings
    if (len(courses) == 0 or len(courses_embeddings) == 0):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(reset_embeddings())

    app.run(port=8000,debug=False)




