import requests
from config import USERS_API_URL, PRODUCTS_API_URL, EMAIL_API_URL, EMAIL_API_KEY
from fastapi import HTTPException

def get_subscribers():
    response = requests.get(f"{USERS_API_URL}/users")  #Hämtar alla användare

    if response.status_code != 200:
        raise Exception("Failed to fetch users")

    users = response.json().get("users", [])  #Extract user list

    #Filtrerar users som har "subscribed": 1 i "data"
    subscribed_users = [
        user for user in users if user.get("data", {}).get("subscribed") == 1
    ]

    return subscribed_users

def get_featured_products():
    response = requests.get(f"{PRODUCTS_API_URL}/products")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch products")

    products = response.json().get("products", [])

    #Filtrerar efter produkter i lager
    featured_products = [p for p in products if p.get("stock", 0) > 0]

    return featured_products[:5]  #Anger antalet produkter i newsletter

def generate_email_html(subject: str, message: str, products: list) -> str:
    """
    Genererar HTML-innehållet för nyhetsbrevet.
    """
    #Skapa HTML-kod för varje produkt i listan
    product_html = "".join([
        f"""
        <tr>
            <td><img src="{p['image']}" alt="{p['name']}" width="100"></td>
            <td>
                <strong>{p['name']}</strong><br>
                {p['category']} - {p['price']} SEK<br>
                <small>{p['description']}</small>
            </td>
        </tr>
        """ for p in products
    ])

    #Bygg hela e-postmeddelandet som HTML
    email_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px #ccc;">
            <h2 style="color: #333;">{subject}</h2>
            <p style="font-size: 16px; color: #555;">{message}</p>

            <h3 style="color: #444;">Featured Craft Beers</h3>
            <table style="width: 100%; border-collapse: collapse;">
                {product_html}
            </table>

            <p style="font-size: 14px; color: #888; margin-top: 20px;">
                🍻 Cheers,<br>
                <strong>Craft Beer Newsletter Team</strong>
            </p>
        </div>
    </body>
    </html>
    """
    return email_html  # Returnerar HTML-innehållet för vidare användning

def send_email(recipient: str, subject: str, message: str, products: list):
    """
    Skickar ett e-postmeddelande via den externa e-posttjänsten.
    """
    # Generera e-postens HTML-innehåll
    email_html = generate_email_html(subject, message, products)

    # Skapa payload för API-anropet
    payload = {
        "to": recipient,      # Mottagarens e-postadress
        "subject": subject,   # Ämnesrad för e-postmeddelandet
        "body": email_html    # Själva e-postinnehållet i HTML-format
    }

    #Skapa headers för API-anropet (inklusive API-nyckel för autentisering)
    headers = {
        "Authorization": f"Bearer {EMAIL_API_KEY}",  # Använder API-nyckel för autentisering
        "Content-Type": "application/json"  # Säkerställer att datan skickas i JSON-format
    }

    #Skicka POST-förfrågan till e-posttjänstens API
    response = requests.post(f"{EMAIL_API_URL}/send", json=payload, headers=headers)

    #Kontrollera om e-postmeddelandet skickades korrekt
    if response.status_code != 200:
        raise Exception(f"Misslyckades med att skicka e-post: {response.text}")

    return response.json()  #Returnerar API-svaret för debugging/logging
