import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import Request
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

class UserCredentials(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=201)
def signup(creds: UserCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    try:
        res = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        return res.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", status_code=200)
def login(creds: UserCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    try:
        res = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        return {"access_token": res.session.access_token, "refresh_token": res.session.refresh_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

@app.get("/public/info", status_code=200)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile", status_code=200)
def protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = auth_header.split(" ")[1]
    try:
        # This network call verifies the signature and expiration
        user_res = supabase.auth.get_user(token)
        return {
            "id": user_res.user.id, 
            "email": user_res.user.email, 
            "created_at": str(user_res.user.created_at)
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# 1. The Reusable Guard (Dependency)
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    token = auth_header.split(" ")[1]
    try:
        return supabase.auth.get_user(token).user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# 2. Update existing profile route to use the guard
@app.get("/protected/profile", status_code=200)
def protected_profile(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "created_at": str(user.created_at)}

# 3. Add logout route
@app.post("/auth/logout", status_code=204)
def logout(user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return

# 4. Add a second protected route to prove reuse works
@app.get("/protected/dashboard", status_code=200)
def dashboard(user = Depends(get_current_user)):
    return {"message": f"Welcome to your private dashboard, {user.email}"}

security = HTTPBearer()

# Update the guard to use HTTPBearer
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials # FastAPI automatically extracts the token string
    try:
        return supabase.auth.get_user(token).user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")