# import the necessary modules and libraries
import json

import bson.json_util as json_util
import pymongo
from flask import Flask, jsonify, make_response, request
from flask_restx import Api, Namespace, Resource

# used to authenticate access to the API
auth_db = {
    "topsecretproject"
}

# connection string to the MongoDB database
user = ""
passw = ""
host = ""
conn_str = "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority".format(user, passw, host)

# create a Flask application instance and an API instance
app = Flask(__name__)
api = Api(app, version = '1.0',
    title = 'H&M API',
    description = """
    API endpoints used to communicate between MongoDB database and Streamlit.
    """,
    contact = "",
    endpoint = "/api"
)

# create a namespace for the API. This namespace will contain the endpoints for accessing the data.
data = Namespace(
    'data',
    description = 'All the data',
    path='/api')
api.add_namespace(data)

# HTTP endpoints for accessing the data
@data.route("/customers")
class get_all_users(Resource):
    def get(self):
        return check_auth_get_data('customer')
    
@data.route("/articles")
class get_all_articles(Resource):
    def get(self):
        return check_auth_get_data('article')

@data.route("/transactions")
class get_all_transactions(Resource):
    def get(self):
        return check_auth_get_data('transaction')
    


def parse_json(data):
    """
    Parses MongoDB documents into JSON format

    Args:
    data: A list of MongoDB documents.

    Returns:
    Returns the parsed JSON-formatted data as a list.
    """
    return json.loads(json_util.dumps(data))

def check_auth_get_data(collection):
     """
     Function to check authorization and get data from a specified MongoDB collection.

     Args:
     collection (str): The name of the MongoDB collection to retrieve data from.

     Returns:
     If successful, it returns a JSON response with the retrieved data from the specified collection. Otherwise, it returns an error message.
     """

     if "Authorization" not in request.headers:
            return make_response(jsonify({"error": "Unauthorized"}), 401)
     else:
        header = request.headers['Authorization']
        token = header.split()[1]

        if token in auth_db:
            with pymongo.MongoClient(conn_str) as client:
                db = client["management"]
                collection_transactions = db[collection]
                query = {}
                result = list(collection_transactions.find(query).limit(7000))
                return make_response(jsonify({'result': [dict(row) for row in parse_json(result)]}), 200)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug=True)

