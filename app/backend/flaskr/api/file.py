from flask import request
from . import apiBluePrint
from flask_hashfs import FlaskHashFS
from flaskr.models.ticket import *
from flaskr.models.Message import *
from flaskr.request_processing import file as rp_file
from flaskr import Iresponse
from flask_jwt import jwt_required


@apiBluePrint.route('/file/download', methods=['POST'])
@jwt_required()
def download_file():
    """ Download a file from server (check rights in future)"""
    json_data = request.get_json()
    if 'address' in json_data:
        address = json_data['address']
        print("ASDFASDFASDF")
        if not address:
            return Iresponse.create_response("No address", 404)
        return Iresponse.create_response(rp_file.get_file(address),201)

    else:
        return Iresponse.create_response("No address", 404)
