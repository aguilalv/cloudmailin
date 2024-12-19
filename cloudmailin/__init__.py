import os

from flask import Flask
from flask import request

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/email', methods=['POST'])
    def login():
        data_received = request.get_json()
    
        f = data_received['envelope']['from']
        s = data_received['headers']['subject']

        return f"Message from {f} about {s}"

    return app
