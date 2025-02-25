from pydantic import BaseModel

class NewsletterRequest(BaseModel):
    subject: str
    message: str
