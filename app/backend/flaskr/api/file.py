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
        # return rp_file.get_file(address)

        if address:
            return Iresponse.create_response("No address", 404)
    else:
        return Iresponse.create_response("No address", 404)
