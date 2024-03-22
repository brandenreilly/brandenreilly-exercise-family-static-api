"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def handle_post():
    request_body = request.json
    members = jackson_family.add_member(request_body)
    response_body = {
        "status": "method created",
        "family": members
     
    }
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete(id):
    del_member = jackson_family.delete_member(id)
    response_body = {
        "status": "member deleted",
        "deleted member": del_member, 
        "remaining family": jackson_family.get_all_members()
     
    }
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['PUT'])
def handle_put(id):
    request_body = request.json
    updated_member = jackson_family.update_member(id, request_body)          
    response_body = {
        "status": "member updated",
        "updated member": updated_member, 
        "current family": jackson_family.get_all_members()
     
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)