from flask import Blueprint
from flask import request

bp = Blueprint('generic', __name__, url_prefix='/generic')

@bp.route('/new',methods=['POST'])
def new_generic_email():
    data_received = request.get_json()
    
    sender = data_received['envelope']['from']
    subject = data_received['headers']['subject']

    return f"Message from {sender} about {subject}"
