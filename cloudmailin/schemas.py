from typing import Dict
from pydantic import BaseModel, EmailStr, model_validator, Field
from datetime import datetime


class Email(BaseModel):
    sender: EmailStr = Field(default=..., description="Email address of the sender")
    recipient: EmailStr = Field(
        default=..., description="Email address of the recipient"
    )
    subject: str = Field(default=..., description="Subject line of the email")
    date: datetime = Field(default=..., description="Date the email was sent")

    @model_validator(mode="before")
    @classmethod
    def flatten_payload(cls, values):
        if not isinstance(values, dict):
            raise ValueError("Input must be a dictionary")

        envelope = values.get("envelope", {})
        headers = values.get("headers", {})

        date_str = headers.get("date")
        if not date_str:
            raise ValueError("Date header is required and cannot be empty")

        try:
            parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")

        return {
            "sender": envelope.get("from"),
            "recipient": envelope.get("to"),
            "subject": headers.get("subject"),
            "date": parsed_date,
        }

    @classmethod
    def from_flat_data(
        cls, sender: str, recipient: str, subject: str, date: str
    ) -> "Email":
        """Factory method for cleaner test initialization."""
        return cls(
            envelope={"from": sender, "to": recipient},
            headers={"subject": subject, "date": date},
        )
