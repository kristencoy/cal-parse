from flask import Flask
from markupsafe import escape
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['GET', 'OPTIONS'])
def hello_world():
    return {
        'greeting': 'hello'
    }

# route to post search for keywords/dates in calendar
@app.route("", methods=['POST', 'OPTIONS'])
def submit_search():
    return "search submitted"