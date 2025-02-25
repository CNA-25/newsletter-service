from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer
import jwt
from config import JWT_SECRET

security = HTTPBearer()

def verify_jwt(request: Request):
    token = request.headers.get("Authorization")
    
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        token = token.split(" ")[1]  #Tar bort "Bearer" prefix
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        if decoded.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admins only")
        
        return decoded
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
