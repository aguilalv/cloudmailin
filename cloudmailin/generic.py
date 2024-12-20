from flask import Blueprint
from flask import request
from flask import jsonify

bp = Blueprint('generic', __name__, url_prefix='/generic')

@bp.route('/new',methods=['POST'])
def new_generic_email():
    data_received = request.get_json()
   
    email_received = {'sender'    : data_received['envelope']['from'],
                      'recipient' : data_received['envelope']['to'],
                      'subject'   : data_received['headers']['subject'],
                     }

    return jsonify(email_received)
