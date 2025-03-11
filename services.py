import requests
from config import USERS_API_URL, PRODUCTS_API_URL, EMAIL_API_URL, EMAIL_API_KEY
from fastapi import HTTPException

#def get_subscribers():
 #   response = requests.get(f"{USERS_API_URL}/users")  #Hämtar alla användare

 #   if response.status_code != 200:
  #      raise Exception("Failed to fetch users")

   # users = response.json().get("users", [])  #Extract user list

    #Filtrerar users som har "subscribed": 1 i "data"
    #subscribed_users = [
     #   user for user in users if user.get("data", {}).get("subscribed") == 1
    #]

    #return subscribed_users

def get_subscribers():
    response = requests.get(f"{USERS_API_URL}/users")  # Fetch all users

    if response.status_code != 200:
        print("Failed to fetch users:", response.status_code)
        print("Response:", response.text)
        return []

    users = response.json().get("users", [])  # Extract user list
    print(f"✅ Successfully fetched {len(users)} users")

    return users

# Run the function if the script is executed directly
if __name__ == "__main__":
    users = get_subscribers()
    print("Fetched Users:", users)

def get_featured_products():
    response = requests.get(f"{PRODUCTS_API_URL}/products")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch products")

    products = response.json().get("products", [])

    #Filtrerar efter produkter i lager
    featured_products = [p for p in products if p.get("stock", 0) > 0]

    return featured_products[:5]  #Anger antalet produkter i newsletter

def generate_email_html(subject: str, message: str, products: list) -> str:
    product_html = "".join([
        f"""
        <tr>
            <td><img src="{p['image']}" alt="{p['name']}" width="100"></td>
            <td>
                <strong>{p['name']}</strong><br>
                {p['category']} - {p['price']}€<br>
                <small>{p['description']}</small>
            </td>
        </tr>
        """ for p in products
    ])

    email_html = f"""
    <html>
    <body>
        <h2>{subject}</h2>
        <p>{message}</p>
        <table>{product_html}</table>
    </body>
    </html>
    """
    return email_html

def send_email(recipient: str, subject: str, message: str, products: list):
    #Formaterar produkt sektionen
    product_html = "".join([
        f"""
        <tr>
            <td><img src="{p['image']}" alt="{p['name']}" width="100"></td>
            <td>
                <strong>{p['name']}</strong><br>
                {p['category']} - {p['price']}€<br>
                <small>{p['description']}</small>
            </td>
        </tr>
        """
        for p in products
    ])

    email_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #333;">{subject}</h2>
                <p style="font-size: 16px; color: #555;">{message}</p>
                
                <h3 style="color: #444;">🔥 Featured Craft Beers</h3>
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

    payload = {
        "recipient": recipient,
        "subject": subject,
        "message": email_html,  #Skickar som HTML
        "content_type": "text/html"  #säkerställer email API vet att de är HTML
    }

    headers = {
    "Authorization": f"Bearer {EMAIL_API_KEY}",  #Använder API KEY
    "Content-Type": "application/json"
    }

    response = requests.post(f"{EMAIL_API_URL}/send", json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return response.json()
