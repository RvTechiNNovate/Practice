from fastapi import FastAPI, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import uvicorn
from fastapi import FastAPI, Response, Cookie, HTTPException

from fastapi.responses import FileResponse
from pathlib import Path



app = FastAPI(title="Cookie Consent Engine")

BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

# ✅ Strict Cross-Origin Configuration for independent frontends
ORIGINS = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,    
    allow_credentials=True,  # Mandatory to allow browsers to accept/send cookies cross-origin
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/init")
async def initialize_app(
    cookie_consent: Annotated[str | None, Cookie()] = None,
    ai_tracker: Annotated[str | None, Cookie()] = None
):
    """Checks the cookie state of the inbound cross-origin browser."""
    if not cookie_consent or cookie_consent != "true":
        return {
            "needs_consent_banner": True,
            "analytics_active": False,
            "ai_profile": "Anonymous (Guest Mode)"
        }
        
    return {
        "needs_consent_banner": False, 
        "analytics_active": True, 
        "ai_profile": ai_tracker or "Missing tracker details"
    }

@app.post("/api/v1/accept-cookies")
async def accept_cookies(response: Response):
    """Sets the cookies explicitly containing path='/' for cross-origin consistency."""
    # cookie_consent (httponly=False so JS can verify it locally if needed)
    response.set_cookie(
        key="cookie_consent", 
        value="true", 
        max_age=31536000, 
        httponly=False,
        samesite="lax",
        path="/"
    )
    # ai_tracker (httponly=True for backend-only database security verification)
    response.set_cookie(
        key="ai_tracker", 
        value="ai_user_metric_98721", 
        max_age=2592000, 
        httponly=True,
        samesite="lax",
        path="/"
    )
    return {"status": "Success", "message": "Consent logged. Cookies deployed successfully."}

@app.post("/login")
def login(response: Response):
    # Demo only: real app mein credentials verify karna
    response.set_cookie(
        key="session_id",
        value="user_123_session",
        httponly=True,
        samesite="lax",
        secure=False,  # Local HTTP development only
        path="/"
    )
    return {"message": "Login successful"}

@app.get("/profile")
def profile(session_id: str | None = Cookie(default=None)):
    if session_id != "user_123_session":
        raise HTTPException(status_code=401, detail="Not logged in")

    return {"user": session_id, "message": "Welcome!"}

if __name__ == "__main__":
    # ✅ Explicitly launches on port 8001
    uvicorn.run("fast_api_cookies:app", host="127.0.0.1", port=8001, reload=True)
