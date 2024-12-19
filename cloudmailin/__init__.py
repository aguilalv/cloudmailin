import os

from flask import Flask
from flask import request

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/email', methods=['POST'])
    def login():
        data_received = request.get_json()
    
        f = data_received['envelope']['from']
        s = data_received['headers']['subject']

        return f"Message from {f} about {s}"

    return app
