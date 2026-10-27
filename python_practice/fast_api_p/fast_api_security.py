from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.responses import FileResponse
from datetime import datetime, timedelta, timezone
import jwt

from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPBasic,
    APIKeyHeader,
    APIKeyCookie,
    APIKeyQuery,
)

app= FastAPI()

#------------------ id and password login or by access token-----------------------

SECRET_KEY = "replace-with-a-long-random-secret"
ALGORITHM = "HS256"

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login_pass")

@app.get("/")
def home():
    return FileResponse("security.html")

@app.post("/login")
def login():
    payload={
        "sub":"ritesh",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":token,"token_type":"bearer"}

def validate_user(userid,password):
    if userid=="123":
        if password=="123":
            return True
    
    return False

def validate_with_response(userid,password):
    if validate_user(userid,password): # here we can check with db hashed password and currnet hashed password if both are same then only we can merge
        payload={
                "sub":userid,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            }
        token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
        return {"access_token":token,"token_type":"bearer"}
    
    return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )()

@app.post("/login_pass")
def login_pass(req_form_data:OAuth2PasswordRequestForm=Depends()):
    print(req_form_data.username,req_form_data.password)
    response=validate_with_response(req_form_data.username,req_form_data.password)
    return  response

def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload["sub"]
    except (jwt.InvalidTokenError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/profile")
def get_profile(username:str = Depends(get_current_user)):
    return {"response":"Welcome"+ username}


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port = 8001)