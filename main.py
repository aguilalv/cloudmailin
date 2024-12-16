from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/email', methods=['POST'])
def login():
    data_received = request.get_json()
    
    f = data_received['envelope']['from']

    return f
