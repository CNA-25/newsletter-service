from fastapi import APIRouter, Depends, HTTPException
from models import NewsletterRequest
from services import get_subscribers, get_featured_products, send_email
from auth import verify_jwt
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/newsletter/test-products") #Test för att hämta produkter från API
def test_fetch_products():
    """
    Fetch featured products from the products API.
    """
    try:
        products = get_featured_products()
        return {"message": "Products fetched successfully", "products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")


@router.get("/newsletter/test-users") #Test att hämta användare från API
def test_fetch_users():
    """
    Fetch subscribers from the users API.
    """
    try:
        subscribers = get_subscribers()
        return {"message": "Subscribers fetched successfully", "subscribers": subscribers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscribers: {str(e)}")

@router.get("/newsletter/preview", response_class=HTMLResponse) #Preview utav newsletter
def preview_newsletter():
    """
    Returns a preview of the newsletter in HTML format.
    """
    sample_products = get_featured_products()
    email_preview = send_email("test@example.com", "Newsletter Preview", "This is a preview of the newsletter.", sample_products)
    return email_preview["message"]

@router.post("/newsletter/send") #Skickar newsletter
def send_newsletter(newsletter: NewsletterRequest, user=Depends(verify_jwt)):
    """
    Sends a newsletter to all registered subscribers.
    """
    subscribers = get_subscribers()
    products = get_featured_products()

    for subscriber in subscribers:
        send_email(subscriber['email'], newsletter.subject, newsletter.message, products)

    return {"message": "Newsletter sent successfully", "recipients": len(subscribers)}
