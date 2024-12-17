from flask import Flask, request
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

# App Initialization
app = Flask(__name__)

# Firebase Initialization - Runs only once
def init_firestore():
    """Initialize Firestore Client."""
    if not firebase_admin._apps:  # Prevent re-initialization
        cred = credentials.Certificate('sandbox-08051982-750a9f98bb70.json')
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firestore()  # Initialize Firestore client globally

# Pydantic Model for Email
class Email(BaseModel):
    sender: str
    subject: str

# Flask Route
@app.route('/email', methods=['POST'])
def store_email():
    """Store email data into Firestore."""
    data_received = request.get_json()

    email_received = Email(
        sender=data_received['envelope']['from'],
        subject=data_received['headers']['subject']
    )

    emails_ref = db.collection('emails')
    emails_ref.add(email_received.dict())  # Pydantic objects need to be converted to dict

    return f"Received: {email_received}"

