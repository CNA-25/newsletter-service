# Newsletter Service - Cloud Native E-Commerce

This API manages the sending of newsletters to registered users. The service retrieves information from the user and product APIs, generates an HTML-formatted newsletter, and sends it via email.

## Functionality
- Retrieves subscribers from the user API
- Fetches current products from the product API
- Formats the newsletter in HTML
- Sends emails via the email API
- Authentication with JWT token

## Endpoints

### Send Newsletter
**POST /newsletter/send**
- **Description:** Sends a newsletter to all registered users.
- **Request Example:**

```
{
    "subject": "News and Offers",
    "message": "Here are the latest products in our store!"
}
```

**Response Example:**
```
{
    "message": "Newsletter sent",
    "recipients": 100
}
```

### Preview Newsletter
**GET /newsletter/preview**
- **Description:** Retrieves a preview of the newsletter in HTML format.
- **Response Example:** Displays the HTML version of the newsletter in the browser.

## Technical Documentation

### Installation and Configuration
1. Clone the repository:
   ```sh
   git clone https://github.com/CNA-25/newsletter-service.git
   cd newsletter-service
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```
3. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file and configure API URLs and email settings.

### Start the Service Locally
```sh
uvicorn main:app --reload
```
Open the API documentation:
```
http://127.0.0.1:8000/docs
```

## API Integrations
- **User API:** Retrieves subscribers
- **Product API:** Fetches products
- **Email API:** Sends newsletters

## Deployment
1. Push the latest code:
   ```sh
   git add .
   git commit -m "Deploying newsletter service"
   git push origin main
   ```
2. Deploy the service on a cloud platform such as Rahti and configure environment variables.

## Testing
To verify functionality, use the `/newsletter/preview` endpoint to review the HTML formatting of the newsletter before sending it.
