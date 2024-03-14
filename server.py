from flask import Flask, request
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/", methods=['GET'])
def hello_world():
    return {
        'greeting': 'hello'
    }

# route to post search for keywords/dates in calendar
@app.route("/search", methods=['POST'])
def submit_search():
    data = request.json
    print(data)
    return {
        "response": "search submitted"}

if __name__ == '__main__':
    logging.getLogger('flask_cors').level = logging.DEBUG
    app.run(debug = True, threaded=False)
