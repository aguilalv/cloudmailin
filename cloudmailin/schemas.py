from typing import Dict
from pydantic import BaseModel, EmailStr, model_validator, Field
from datetime import datetime

class Email(BaseModel):
    sender: EmailStr = Field(default=..., description="Email address of the sender")
    recipient: EmailStr = Field(default=..., description="Email address of the recipient")
    subject: str = Field(default=..., description="Subject line of the email")
    date: datetime = Field(default=..., description="Date the email was sent")
    plain_body: str = Field(default=..., description="Body of the email in plain text format")

    @staticmethod
    def flatten_payload(values: dict) -> dict:
        if not isinstance(values, dict):
            raise ValueError("Input must be a dictionary")

        envelope = values.get("envelope", {})
        headers = values.get("headers", {})
        body = values.get("body", {})

        return {
            "sender": envelope.get("from"),
            "recipient": envelope.get("to"),
            "subject": headers.get("subject"),
            "plain_body": body.get("plain"),
            "date": headers.get("date"),
        }

    @model_validator(mode="before")
    @classmethod
    def preprocess_payload(cls, values):
        """Flatten nested payload and ensure required fields exist."""
        flattened = cls.flatten_payload(values)
        
        # Explicit check for required fields
        required_fields = ("sender", "recipient", "subject", "date", "plain_body")
        missing_fields = [field for field in required_fields if not flattened.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Parse the date
        try:
            flattened["date"] = datetime.strptime(flattened["date"], "%a, %d %b %Y %H:%M:%S %z")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {flattened.get('date')}")
        
        return flattened

    @classmethod
    def from_flat_data(
            cls, sender: str, recipient: str, subject: str, date: str, plain_body: str
    ) -> "Email":
        """Factory method for cleaner test initialization."""
        return cls(
            envelope={"from": sender, "to": recipient},
            headers={"subject": subject, "date": date},
            body={"plain": plain_body},
        )
