from flask import Flask
from flask import request

from pydantic import BaseModel

app = Flask(__name__)

class Email(BaseModel):
    f: str
    s: str


@app.route('/email', methods=['POST'])
def login():
    data_received = request.get_json()
    
    email_received = Email(
        f = data_received['envelope']['from'],
        s = data_received['headers']['subject']
    )

    return f"received: {email_received}"
