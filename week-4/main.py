import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel

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