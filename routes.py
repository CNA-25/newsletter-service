from fastapi import APIRouter, Depends, HTTPException
from models import NewsletterRequest
from services import get_subscribers, get_featured_products, send_email
from auth import verify_jwt
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.post("/newsletter/send")
def send_newsletter(newsletter: NewsletterRequest, user=Depends(verify_jwt)):
    """
    Sends a newsletter to all registered subscribers.
    """
    subscribers = get_subscribers()
    products = get_featured_products()

    for subscriber in subscribers:
        send_email(subscriber['email'], newsletter.subject, newsletter.message, products)

    return {"message": "Newsletter sent successfully", "recipients": len(subscribers)}

@router.get("/newsletter/preview", response_class=HTMLResponse)
def preview_newsletter():
    """
    Returns a preview of the newsletter in HTML format.
    """
    sample_products = get_featured_products()
    email_preview = send_email("test@example.com", "Newsletter Preview", "This is a preview of the newsletter.", sample_products)
    return email_preview["message"]