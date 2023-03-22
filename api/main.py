# import the necessary modules and libraries
import json

import pymongo
from bson import json_util
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from flask_restx import Api, Namespace, Resource, reqparse

# used to authenticate access to the API
auth_db = {
    "topsecretproject"
}

# connection string to the MongoDB database
user = "" # to add
passw = "" # to add
host = "" # to add


conn_str = "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority".format(user, passw, host)

# Set up a request parser for the limit argument
limit_parser = reqparse.RequestParser()
limit_parser.add_argument('limit', type=int, default=100)

# create a Flask application instance and an API instance
app = Flask(__name__)
CORS(app)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': ''' 
        Please insert "Bearer <your_token>"
        ''',
    }
}

api = Api(app, version = '1.0',
    title = 'H&M API',
    description = """
    API endpoints used to communicate between MongoDB database and Streamlit.
    """,
    contact = "",
    endpoint = "/api",
    authorizations=authorizations,
    
)

# create a namespace for the API. This namespace will contain the endpoints for accessing the data.
customers = Namespace(
    'Customers',
    description = 'API endpoint for customers data',
    path='/api',)

api.add_namespace(customers)

# HTTP endpoints for accessing the data
@customers.route("/customers")
class get_all_users(Resource):
    @customers.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint that gets all the customers data (default limit of 100 items), 
             ''')
    def get(self):
        return check_auth_get_data('customer')
    
# create a namespace for the API. This namespace will contain the endpoints for accessing the data.
articles = Namespace(
    'Articles',
    description = 'API endpoint for articles data',
    path='/api')

api.add_namespace(articles)

@articles.route("/articles")
class get_all_articles(Resource):
    @articles.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint that gets all the articles data (default limit of 100 items), 
             ''')
    def get(self):
        response = check_auth_get_data('article')
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# create a namespace for the API. This namespace will contain the endpoints for accessing the data.
transactions = Namespace(
    'Transactions',
    description = 'API endpoint for transactions data',
    path='/api')

api.add_namespace(transactions)

@transactions.route("/transactions")
class get_all_transactions(Resource):
    @transactions.doc(parser=limit_parser,
             security='Bearer Auth',
             description='''
             API endpoint that gets all the transactions data (default limit of 100 items), 
             ''')
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
     
     if 'Authorization' not in request.headers:
        return make_response(jsonify({"error": "Token is missing"}), 401)
     
     else:
        header = request.headers['Authorization']
        token = header.split()

        if len(token) == 2 and token[1] in auth_db:
            args = limit_parser.parse_args()
            limit = args['limit']
            with pymongo.MongoClient(conn_str) as client:
                db = client["management"]
                collection_transactions = db[collection]
                query = {}
                result = list(collection_transactions.find(query).limit(limit))
                return make_response(jsonify({'result': [dict(row) for row in parse_json(result)]}), 200)
        else:
            return make_response(jsonify({"error": "Invalid token"}), 401)
     



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug=True)

