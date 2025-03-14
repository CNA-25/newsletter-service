from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config import USERS_API_URL, EMAIL_API_URL, PRODUCTS_API_URL

app = FastAPI()

from routes import router
# Register the API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

#Tillåter request från Users API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[USERS_API_URL, EMAIL_API_URL, PRODUCTS_API_URL], #API URL
    allow_credentials=True,
    allow_methods=["*"],  #Tillåter alla HTTP metoder (GET, POST, osv.)
    allow_headers=["*"],  #Tillåter alla headers
)
