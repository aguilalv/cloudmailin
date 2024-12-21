from pydantic import BaseModel, EmailStr, model_validator

class Email(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    subject: str

    @model_validator(mode='before')
    @classmethod
    def flatten_payload(cls, values):
        """
        Flatten the incoming nested payload to match the model structure.
        """
        if not isinstance(values, dict):
            raise ValueError("Input must be a dictionary")

        envelope = values.get("envelope", {})
        headers = values.get("headers", {})

        return {
            "sender": envelope.get("from"),
            "recipient": envelope.get("to"),
            "subject": headers.get("subject")
        }
